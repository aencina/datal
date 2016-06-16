# -*- coding: utf-8 -*-
import logging
from django.db.models import F, Max
from django.conf import settings
from django.db import transaction


from core.daos.visualizations import VisualizationSearchDAOFactory, VisualizationDBDAO
from core.models import VisualizationRevision, Visualization, VisualizationI18n
from core.choices import StatusChoices, ActionStreams
from core.exceptions import VisualizationNotFoundException, IllegalStateException, ParentNotPublishedException, VisualizationParentNotPublishedException
from .resource import AbstractLifeCycleManager

logger = logging.getLogger(__name__)

CREATE_ALLOWED_STATES = [
    StatusChoices.DRAFT,
    StatusChoices.PENDING_REVIEW,
    StatusChoices.APPROVED,
    StatusChoices.PUBLISHED
]
PUBLISH_ALLOWED_STATES = [
    StatusChoices.DRAFT,
    StatusChoices.PENDING_REVIEW,
    StatusChoices.APPROVED,
    StatusChoices.PUBLISHED
]
UNPUBLISH_ALLOWED_STATES = [
    StatusChoices.DRAFT,
    StatusChoices.PUBLISHED
]
SEND_TO_REVIEW_ALLOWED_STATES = [
    StatusChoices.DRAFT
]
ACCEPT_ALLOWED_STATES = [
    StatusChoices.PENDING_REVIEW
]
REJECT_ALLOWED_STATES = [
    StatusChoices.PENDING_REVIEW
]
REMOVE_ALLOWED_STATES = [
    StatusChoices.DRAFT,
    StatusChoices.APPROVED,
    StatusChoices.PUBLISHED
]
EDIT_ALLOWED_STATES = [
    StatusChoices.DRAFT,
    StatusChoices.APPROVED,
    StatusChoices.PUBLISHED
]


class VisualizationLifeCycleManager(AbstractLifeCycleManager):
    """ Manage a visualization Life Cycle"""
    revision_model = VisualizationRevision
    model = Visualization
    search_model = VisualizationSearchDAOFactory
    dao_model = VisualizationDBDAO

    def __init__(self, user, resource=None, language=None, visualization_id=0, visualization_revision_id=0):
        super(VisualizationLifeCycleManager, self).__init__(user, language)
        # Internal used resources (optional). You could start by resource or revision
        try:
            if type(resource) == Visualization:
                self.visualization = resource
                self.visualization_revision = VisualizationRevision.objects.select_related().get(
                    pk=self.visualization.last_revision_id
                )
            elif type(resource) == VisualizationRevision:
                self.visualization_revision = resource
                self.visualization = resource.visualization
            elif visualization_id > 0:
                self.visualization = Visualization.objects.get(pk=visualization_id)
                self.visualization_revision = VisualizationRevision.objects.select_related().get(
                    pk=self.visualization.last_revision_id)
            elif visualization_revision_id > 0:
                self.visualization_revision = VisualizationRevision.objects.select_related().get(pk=visualization_revision_id)
                self.visualization = self.visualization_revision.visualization
            else:
                self.visualization_revision = None
                self.visualization = None
        except Visualization.DoesNotExist, VisualizationRevision.DoesNotExist:
            raise VisualizationNotFoundException()

        self.visualizationi18n = None
        if self.visualization and self.visualization_revision:
            self.visualizationi18n = VisualizationI18n.objects.get(
                visualization_revision=self.visualization_revision,
                language=self.visualization.user.language
            )

        self.resource=self.visualization
        self.revision=self.visualization_revision

    def get_parents_list(self):
        return [self.resource.datastream, self.resource.datastream.last_revision.dataset]

    def get_revisions_queryset(self):
        return VisualizationRevision.objects.filter(visualization=self.visualization )

    def create(self, datastream_rev=None, language=None, **fields):
        """ Create a new Visualization """

        self.visualization, self.visualization_revision = VisualizationDBDAO().create(
            datastream_rev=datastream_rev,
            user=self.user,
            language=language,
            **fields
        )

        self.resource = self.visualization
        self.revision = self.visualization_revision

        self._log_activity(ActionStreams.CREATE)
        self._update_last_revisions()
        return self.visualization_revision

    def edit(self, allowed_states=EDIT_ALLOWED_STATES, changed_fields=None, **fields):
        """
        Actualiza una visualizacion

        :param allowed_states:
        :param changed_fields:
        :param fields:
        :return: VisualizationRevision Model Object
        """
        old_status = self.visualization_revision.status
        
        if self.visualization_revision.status not in allowed_states:
            raise IllegalStateException(
                from_state=self.visualization_revision.status,
                to_state=self.visualization_revision.status,
                allowed_states=allowed_states
            )

        if self.visualization_revision.status in [StatusChoices.PUBLISHED, StatusChoices.APPROVED]:
            self.visualization, self.visualization_revision = VisualizationDBDAO().create(
                visualization=self.visualization,
                datastream_rev=self.visualization_revision.datastream.last_revision,
                user=self.visualization_revision.user,
                status=fields.pop('status', StatusChoices.DRAFT),
                **fields
            )
            self._update_last_revisions()
        else:
            # Actualizo sin el estado
            self.visualization_revision = VisualizationDBDAO().update(
                self.visualization_revision,
                status=fields.pop('status', old_status), 
                changed_fields=changed_fields,
                **fields
            )
        
        self._log_activity(ActionStreams.EDIT)
        return self.visualization_revision


    def reject(self, allowed_states=REJECT_ALLOWED_STATES):
        """ reject a visualization revision """

        if self.visualization_revision.status not in allowed_states:
            raise IllegalStateException(
                from_state=self.visualization_revision.status,
                to_state=StatusChoices.DRAFT,
                allowed_states=allowed_states
            )

        self.visualization_revision.status = StatusChoices.DRAFT
        self.visualization_revision.save()
        self._log_activity(ActionStreams.REJECT)

    def _send_childs_to_review(self):
        """
        No implementado ya que las visualizaciones no tienen hijos
        :return:
        """
        pass

    def _move_childs_to_status(self, status=StatusChoices.PENDING_REVIEW):
        pass


    def save_as_status(self, status=StatusChoices.DRAFT):
        self.visualization_revision.clone(status)
        self._update_last_revisions()

    def clone(self):
        vzr = self.visualization_revision.clone(self.visualization_revision.status)
        if vzr.status == StatusChoices.PUBLISHED:
            VisualizationSearchDAOFactory().create(vzr).add()
        self._update_last_revisions()
        return vzr

    def _remove_all(self):
        self.visualization.delete()
        self._log_activity(ActionStreams.DELETE)
        if settings.DEBUG: logger.info('Clean Caches')
        self._delete_cache(cache_key='my_total_visualizations_%d' % self.visualization.user.id)
        self._delete_cache(cache_key='account_total_visualization_%d' % self.visualization.user.account.id)

    def _log_activity(self, action_id):
        if not self.visualizationi18n:
            self.visualizationi18n = self.visualization_revision.visualizationi18n_set.all()[0] # TODO at at DAO

        title = self.visualizationi18n.title
        resource_category = self.visualization_revision.datastream.last_revision.category.categoryi18n_set.all()[0] # todo add language
        
        return super(VisualizationLifeCycleManager, self)._log_activity(
            action_id,
            self.visualization_revision.visualization.id,
            settings.TYPE_VISUALIZATION,
            self.visualization_revision.id,
            title,
            resource_category
        )

    def _unpublish_all(self, to_status=StatusChoices.DRAFT):
        """
        Despublica todas las revisiones de la visualizacion y la de todos sus hijos en cascada
        No se implementa ya que visualizaciones no tiene modelos hijo
        """
        VisualizationRevision.objects.filter(
            visualization__id=self.visualization.id,
            status=StatusChoices.PUBLISHED)\
        .update(status=to_status)

    def remove(self, killemall=False, allowed_states=REMOVE_ALLOWED_STATES):
        """ Elimina una revision o todas las revisiones de un visualizacion """

        if self.visualization_revision.status not in allowed_states:
            raise IllegalStateException(
                from_state=self.visualization_revision.status,
                to_state=None,
                allowed_states=allowed_states
            )

        if killemall:
            self._remove_all()
        else:
            revcount = VisualizationRevision.objects.filter(
                visualization=self.visualization.id,
                status=StatusChoices.PUBLISHED
            ).count()

            if revcount == 1:
                # Si la revision a eliminar es la unica publicada entonces despublicar todas las visualizaciones
                # en cascada
                self._unpublish_all()

            # Fix para evitar el fallo de FK con las published revision. Luego la funcion update_last_revisions
            # completa el valor correspondiente.
            self.visualization.last_published_revision=None
            self.visualization.save()

            self.visualization_revision.delete()

        self._update_last_revisions()

        self._log_activity(ActionStreams.DELETE)
        self._delete_cache(cache_key='my_total_visualizations_%d' % self.visualization.user.id)
        self._delete_cache(cache_key='account_total_visualization_%d' % self.visualization.user.account.id)

    def unpublish(self, killemall=False, allowed_states=UNPUBLISH_ALLOWED_STATES, to_status=StatusChoices.DRAFT):
        """ Despublica la revision de un dataset """
        if self.visualization_revision.status not in allowed_states:
            raise IllegalStateException(
                from_state=self.visualization_revision.status,
                to_state=StatusChoices.DRAFT,
                allowed_states=allowed_states
            )

        if killemall:
            self._unpublish_all(to_status=to_status)
        else:
            revcount = VisualizationRevision.objects.filter(
                visualization=self.visualization.id,
                status=StatusChoices.PUBLISHED
            ).count()

            if revcount == 1:
                self._unpublish_all()
            else:
                self.visualization_revision.status = to_status
                self.visualization_revision.save()

        search_dao = VisualizationSearchDAOFactory().create(self.visualization_revision)
        search_dao.remove()

        self._update_last_revisions()

        self._log_activity(ActionStreams.UNPUBLISH)

    def send_to_review(self, allowed_states=SEND_TO_REVIEW_ALLOWED_STATES):
        """ Envia a revision un datastream """

        if self.visualization_revision.status not in allowed_states:
            raise IllegalStateException(
                from_state=self.visualization_revision.status,
                to_state=StatusChoices.PENDING_REVIEW,
                allowed_states=allowed_states)

        self._send_childs_to_review()

        self.visualization_revision.status = StatusChoices.PENDING_REVIEW
        self.visualization_revision.save()
        self._log_activity(ActionStreams.REVIEW)
