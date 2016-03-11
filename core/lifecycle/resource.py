# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

from core.choices import StatusChoices
from core.daos.activity_stream import ActivityStreamDAO
from core.exceptions import IllegalStateException
from core.lib.datastore import *
from core.models import User
from core.cache import Cache
from redis import Redis


class AbstractLifeCycleManager():
    """ Manage a Resource Life Cycle"""

    __metaclass__ = ABCMeta

    CREATE_ALLOWED_STATES = [StatusChoices.DRAFT, StatusChoices.PENDING_REVIEW, StatusChoices.PUBLISHED]
    PUBLISH_ALLOWED_STATES = [StatusChoices.DRAFT, StatusChoices.PENDING_REVIEW, StatusChoices.APPROVED]
    UNPUBLISH_ALLOWED_STATES = [StatusChoices.PUBLISHED]
    SEND_TO_REVIEW_ALLOWED_STATES = [StatusChoices.DRAFT]
    ACCEPT_ALLOWED_STATES = [StatusChoices.PENDING_REVIEW]
    REJECT_ALLOWED_STATES = [StatusChoices.PENDING_REVIEW]
    REMOVE_ALLOWED_STATES = [StatusChoices.DRAFT, StatusChoices.APPROVED, StatusChoices.PUBLISHED ]
    EDIT_ALLOWED_STATES = [StatusChoices.DRAFT, StatusChoices.APPROVED, StatusChoices.PUBLISHED]

    @abstractmethod
    def create(self, allowed_states=CREATE_ALLOWED_STATES, **fields):
        pass


    @abstractmethod
    def publish(self, allowed_states=PUBLISH_ALLOWED_STATES):
        pass

    @abstractmethod
    def _publish_childs(self):
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
    def accept(self, allowed_states=ACCEPT_ALLOWED_STATES):
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

    @abstractmethod
    def _update_last_revisions(self):
        pass

    def __init__(self, user, language):
        self.user = type(user) is not int and user or User.objects.get(pk=user)
        self.language = language

    def _delete_cache(self, cache_key, cache_db=0):
        """ limpiar un cache específico
        cache_db=0 es el cache principal (CACHE_DATABASES)
        usado para actualizar luego de modificar recursos que requieren actualización rápida"""
        c = Cache(db=cache_db)
        c.delete(cache_key)
