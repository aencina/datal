# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

from core.choices import StatusChoices
from core.daos.activity_stream import ActivityStreamDAO
from core.exceptions import IllegalStateException
from core.lib.datastore import *
from core.models import User
from core.cache import Cache
from django.db.models import F, Max
from django.db import transaction
from redis import Redis

from core.choices import ActionStreams, StatusChoices
from core.exceptions import IllegalStateException, ParentNotPublishedException

logger = logging.getLogger(__name__)

class AbstractLifeCycleManager():
    """ Manage a Resource Life Cycle"""

    __metaclass__ = ABCMeta

    CREATE_ALLOWED_STATES = [StatusChoices.DRAFT, StatusChoices.PENDING_REVIEW, StatusChoices.PUBLISHED]
    PUBLISH_ALLOWED_STATES = [StatusChoices.DRAFT, StatusChoices.PENDING_REVIEW, StatusChoices.APPROVED, StatusChoices.PUBLISHED]
    UNPUBLISH_ALLOWED_STATES = [StatusChoices.PUBLISHED]
    SEND_TO_REVIEW_ALLOWED_STATES = [StatusChoices.DRAFT]
    ACCEPT_ALLOWED_STATES = [StatusChoices.PENDING_REVIEW]
    REJECT_ALLOWED_STATES = [StatusChoices.PENDING_REVIEW]
    REMOVE_ALLOWED_STATES = [StatusChoices.DRAFT, StatusChoices.APPROVED, StatusChoices.PUBLISHED ]
    EDIT_ALLOWED_STATES = [StatusChoices.DRAFT, StatusChoices.APPROVED, StatusChoices.PUBLISHED]

    def get_children_queryset(self, last=True, publish=True):
        """ Returns a queryset of children """
        pass

    def get_parents_list(self):
        """ Returns a list of parents """
        return []

    @abstractmethod
    def get_revisions_queryset(self):
        """ Returns a queryset with all resource revisions """
        pass

    def get_queryset(self):
        """ Returns base queryset for this resource """
        if hasattr(self, 'revision_model'):
            return self.revision_model.objects
        raise NotImplementedError()

    def get_search_dao(self):
        """ Returns a search factory for the resource """
        if hasattr(self, 'search_model'):
            return self.search_model()
        raise NotImplementedError()

    def get_children(self, statuses=None, last=True, publish=False, for_update=False):
        queryset = self.get_children_queryset(last, publish)
        
        if statuses and queryset:
            queryset = queryset.filter(status__in=statuses)

        if for_update:
            queryset = queryset.select_for_update()

        return queryset

    def get_children_not_published(self, for_update=False):
        return self.get_children(
            statuses=[StatusChoices.DRAFT, StatusChoices.PENDING_REVIEW ],
            publish=True
        )

    def get_children_for_publishing(self, for_update=False):
        return self.get_children(
            statuses=[StatusChoices.APPROVED, StatusChoices.PUBLISHED],
            publish=True)

    def get_parents(self, statuses=None):
        answer = []
        for parent in self.get_parents_list():
            if parent.last_revision and parent.last_revision.status in statuses:
                answer.append(parent)
        return answer

    def get_child_lifecycle(self, resource):
        if hasattr(self, 'child_lifecycle_model'):
            return self.child_lifecycle_model(user=self.user, resource=resource)

    def can_accept(self, allowed_states):
        logger.info('[%s] Puedo Aceptar Rev. %s.' % (type(self).__name__, self.revision.id))
        if self.revision.status not in allowed_states:
            raise IllegalStateException(
                from_state=self.revision.status,
                to_state=StatusChoices.APPROVED,
                allowed_states=allowed_states
            )

        return True

    def accept(self, allowed_states=ACCEPT_ALLOWED_STATES):
        if self.can_accept(allowed_states):
            logger.info('[%s] Acepto Rev. %s.' % (type(self).__name__, self.revision.id))
            self.revision.status = StatusChoices.APPROVED
            self.revision.save()

            self._log_activity(ActionStreams.ACCEPT)



    def accept_children(self, allowed_states):
        logger.info('[%s] Acepto Children Rev. %s.' % (type(self).__name__, self.revision.id))
        queryset = self.get_children_not_published()
        if queryset:
            for child in queryset.all():
                lifecycle = self.get_child_lifecycle(child)
                lifecycle.accept(allowed_states=allowed_states)

    def can_publish_bof_parents(self):
        parents = self.get_parents(statuses=[StatusChoices.DRAFT, StatusChoices.PENDING_REVIEW, StatusChoices.APPROVED])
        if len(parents) > 0:
            raise ParentNotPublishedException(parents[0].last_revision)
        return True

    def can_publish_bof_children(self, allowed_states=PUBLISH_ALLOWED_STATES, accept_children=False):
        children_not_published = self.get_children_not_published()
        if children_not_published and children_not_published.exists():
            raise ChildNotApprovedException(self.revision, self.child_type)

        children_for_publishing = self.get_children_for_publishing()
        if children_for_publishing:
            for resource in children_for_publishing.all():
                self.get_child_lifecycle(resource).can_publish_bof_children(allowed_states, accept_children)
        return True

    def can_publish(self, allowed_states=PUBLISH_ALLOWED_STATES, accept_children=False):
        logger.info('[%s] Puedo Publicar Rev. %s.' % (
            type(self).__name__, self.revision.id))
        if self.revision.status not in allowed_states:
            raise IllegalStateException(
                    from_state=self.revision.status,
                    to_state=StatusChoices.PUBLISHED,
                    allowed_states=allowed_states)

        try:
            self.can_publish_bof_parents()
        except ParentNotPublishedException:
            self.revision.status = StatusChoices.APPROVED
            self.revision.save()
            transaction.commit()
            raise

        if not accept_children:
            self.can_publish_bof_children(allowed_states, accept_children)

        return True

    def publish(self, allowed_states=PUBLISH_ALLOWED_STATES, parent_status=None, accept_children=False):
        if self.can_publish(allowed_states, accept_children):
            logger.info('[%s] Publico Rev. %s.' % (type(self).__name__, self.revision.id))
            
            if accept_children:
                self.accept_children(allowed_states)

            self.revision.status = StatusChoices.PUBLISHED
            self.revision.save()

            self._update_last_revisions()

            with transaction.atomic():
                queryset = self.get_children_for_publishing()
                if queryset:
                    for child in queryset.all():
                        lifecycle = self.get_child_lifecycle(child)
                        try:
                            lifecycle.publish(allowed_states=allowed_states, 
                                parent_status=parent_status, 
                                accept_children=accept_children)
                        except IllegalStateException:
                            raise ChildNotApprovedException(child, lifecycle.child_type)

            # This two lines must be deleted beacause we repeat them on the 
            # _update_last_revision, but as they do no harm i leave them
            search_dao = self.get_search_dao().create(self.revision)
            search_dao.add()

            self._log_activity(ActionStreams.PUBLISH)

    def _update_last_revisions(self):
        last_revision_id = self.get_revisions_queryset().aggregate(Max('id'))['id__max']

        if last_revision_id:
            self.resource.last_revision = self.get_queryset().get(pk=last_revision_id)
            last_published_revision_id = self.get_revisions_queryset().filter(
                status=StatusChoices.PUBLISHED).aggregate(Max('id'))['id__max']
            if last_published_revision_id:
                self.resource.last_published_revision = self.get_queryset().get(
                    pk=last_published_revision_id)
                search_dao = self.get_search_dao().create(self.resource.last_published_revision)
                search_dao.add()
            else:
                self.resource.last_published_revision = None
            
            self.resource.save()
        else:
            if self.resource.id:
                self.resource.delete()
            self.resource.last_revision_id = last_revision_id

    @abstractmethod
    def create(self, allowed_states=CREATE_ALLOWED_STATES, **fields):
        pass

    @abstractmethod
    def unpublish(self, killemall=False, allowed_states=UNPUBLISH_ALLOWED_STATES):
        pass


    @abstractmethod
    def _unpublish_all(self):
        pass

    @abstractmethod
    def send_to_review(self, allowed_states=SEND_TO_REVIEW_ALLOWED_STATES):
        pass

    @abstractmethod
    def _send_childs_to_review(self):
        pass

    @abstractmethod
    def reject(self, allowed_states=REJECT_ALLOWED_STATES):
        pass

    @abstractmethod
    def remove(self, killemall=False, allowed_states=REMOVE_ALLOWED_STATES):
        pass

    @abstractmethod
    def _remove_all(self):
        pass

    @abstractmethod
    def edit(self, allowed_states=EDIT_ALLOWED_STATES, changed_fields=None, **fields):
        pass

    @abstractmethod
    def _move_childs_to_status(self, status=StatusChoices.PENDING_REVIEW):
        pass

    @abstractmethod
    def save_as_status(sef,status=StatusChoices.DRAFT):
        pass

    @abstractmethod
    def _log_activity(self, action_id, resource_id, resource_type, revision_id, resource_title, resource_category):
        return ActivityStreamDAO().create(account_id=self.user.account.id, user_id=self.user.id,
                                          resource_id=resource_id, 
                                          revision_id=revision_id, 
                                          resource_type=resource_type,
                                          resource_title=resource_title, 
                                          action_id=action_id, 
                                          resource_category=resource_category)

    def clean_cache(self):
        """Elimina el recurso de redis
        :param fields:
        :return:
        """
        reader = Redis(host=settings.REDIS_READER_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
        writer = Redis(host=settings.REDIS_WRITER_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
        
        try:
            writer.delete(self.revision.id)
        except:
            if settings.DEBUG: logger.warning("_clean_cache: no existe id: %s" % self.revision.id)
        else:
            if settings.DEBUG: logger.info("_clean_cache: cleaned id: %s" % self.revision.id)

        keys = reader.keys(str(self.revision.id)+"::*")
        for key in keys:
            try:
                writer.delete(key)
            except:
                if settings.DEBUG: logger.warning("_clean_cache: no existe key: %s" % key)
            else:
                if settings.DEBUG: logger.info("_clean_cache: cleaned key: %s" % key)

    def __init__(self, user, language):
        self.user = type(user) is not int and user or User.objects.get(pk=user)
        self.language = language

    def _delete_cache(self, cache_key, cache_db=0):
        """ limpiar un cache específico
        cache_db=0 es el cache principal (CACHE_DATABASES)
        usado para actualizar luego de modificar recursos que requieren actualización rápida"""
        c = Cache(db=cache_db)
        c.delete(cache_key)
