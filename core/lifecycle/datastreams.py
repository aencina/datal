# -*- coding: utf-8 -*-
from django.db.models import F, Max
from django.db import transaction
from core.choices import ActionStreams, StatusChoices
from core.models import DatasetRevision, DataStreamRevision, DataStream, DatastreamI18n, VisualizationRevision, Visualization
from core.lifecycle.resource import AbstractLifeCycleManager
from core.lib.datastore import *
from core.exceptions import IllegalStateException, DataStreamNotFoundException
from core.daos.datastreams import DataStreamDBDAO, DatastreamSearchDAOFactory
from .visualizations import VisualizationLifeCycleManager


logger = logging.getLogger(__name__)
CREATE_ALLOWED_STATES = [StatusChoices.DRAFT, StatusChoices.PENDING_REVIEW, StatusChoices.APPROVED,
                         StatusChoices.PUBLISHED]
PUBLISH_ALLOWED_STATES = [StatusChoices.DRAFT, StatusChoices.PENDING_REVIEW, StatusChoices.APPROVED,
                          StatusChoices.PUBLISHED]
UNPUBLISH_ALLOWED_STATES = [StatusChoices.DRAFT, StatusChoices.PUBLISHED]
SEND_TO_REVIEW_ALLOWED_STATES = [StatusChoices.DRAFT]
ACCEPT_ALLOWED_STATES = [StatusChoices.PENDING_REVIEW]
REJECT_ALLOWED_STATES = [StatusChoices.PENDING_REVIEW]
REMOVE_ALLOWED_STATES = [StatusChoices.DRAFT, StatusChoices.APPROVED, StatusChoices.PUBLISHED ]
EDIT_ALLOWED_STATES = [StatusChoices.DRAFT, StatusChoices.APPROVED, StatusChoices.PUBLISHED]

logger = logging.getLogger(__name__)


class DatastreamLifeCycleManager(AbstractLifeCycleManager):
    """ Manage a Datastream revision Life Cycle"""
    revision_model = DataStreamRevision
    model = DataStream
    search_model = DatastreamSearchDAOFactory
    dao_model = DataStreamDBDAO
    child_lifecycle_model = VisualizationLifeCycleManager
    child_type = settings.TYPE_VISUALIZATION
    model_name_plural = 'datastreams'
    model_name = 'datastream'

    def __init__(self, user, resource=None, language=None, datastream_id=0, datastream_revision_id=0):
        super(DatastreamLifeCycleManager, self).__init__(user, language)
        # Internal used resources (optional). You could start by dataset or revision

        try:
            if type(resource) == DataStream:
                self.datastream = resource
                self.datastream_revision = DataStreamRevision.objects.select_related().get(
                    pk=self.datastream.last_revision_id)
            elif type(resource) == DataStreamRevision:
                self.datastream_revision = resource
                self.datastream = resource.datastream
            elif datastream_id > 0:
                self.datastream = DataStream.objects.get(pk=datastream_id)
                self.datastream_revision = DataStreamRevision.objects.select_related().get(
                    pk=self.datastream.last_revision_id)
            elif datastream_revision_id > 0:
                self.datastream_revision = DataStreamRevision.objects.select_related().get(pk=datastream_revision_id)
                self.datastream = self.datastream_revision.datastream
            else:
                self.datastream_revision = None
                self.datastream = None
        except DataStream.DoesNotExist, DataStreamRevision.DoesNotExist:
            raise DataStreamNotFoundException()

        self.datastreami18n = None
        if self.datastream and self.datastream_revision:
            self.datastreami18n = DatastreamI18n.objects.get(
                datastream_revision=self.datastream_revision,
                language=self.datastream.user.language
            )

        # compatibilidad con un lifecycle unico que use internamente
        # las variables resource y revision en vez de especializarse
        # con un tipoderecurso_
        self.resource=self.datastream
        self.revision=self.datastream_revision

    def get_children_revisions_queryset(self, last=True, publish=False):
        queryset = VisualizationRevision.objects.filter(
                visualization__datastream__id=self.datastream.id)

        if last:
            queryset = queryset.filter(
                id=F('visualization__last_revision__id'))

        if publish:
            queryset = queryset.filter(
                visualization__last_published_revision__isnull=False)

        return queryset

    def get_parents_list(self):
        return [self.revision.dataset]

    def get_children_queryset(self):
        return Visualization.objects.filter(visualizationrevision__datastream=self.datastream).distinct()

    def get_revisions_queryset(self):
        return DataStreamRevision.objects.filter(datastream=self.datastream)

    def create(self, allowed_states=CREATE_ALLOWED_STATES, **fields):
        """ Create a new DataStream """

        # Check for allowed states
        status = int(fields.get('status', StatusChoices.DRAFT))

        if int(status) not in allowed_states:
            raise IllegalStateException(
                                    from_state=None,
                                    to_state=status,
                                    allowed_states=allowed_states)

        #language = fields.get('language', self.user.language)
        #category = Category.objects.get(pk=fields['category_id'])
        self.datastream, self.datastream_revision = DataStreamDBDAO().create(
            user=self.user,
            #category=category,
            #language=language,
            **fields
        )

        self.resource = self.datastream
        self.revision = self.datastream_revision

        self.datastreami18n = self.datastream_revision.datastreami18n_set.all()[0]
        
        self._log_activity(ActionStreams.CREATE)

        # permite publicar al crear
        if status == StatusChoices.PUBLISHED:
            self.publish(allowed_states=CREATE_ALLOWED_STATES)
        else:
            self._update_last_revisions()

        return self.datastream_revision

    def unpublish(self, killemall=False, allowed_states=UNPUBLISH_ALLOWED_STATES, to_status=StatusChoices.DRAFT):
        """ Despublica la revision de un dataset """

        if self.datastream_revision.status not in allowed_states:
            raise IllegalStateException(
                                    from_state=self.datastream_revision.status,
                                    to_state=to_status,
                                    allowed_states=allowed_states)

        if killemall:
            self._unpublish_all(to_status=to_status)
        else:
            revcount = DataStreamRevision.objects.filter(datastream=self.datastream.id, status=StatusChoices.PUBLISHED).count()

            if revcount == 1:
                self._unpublish_all()
            else:
                self.datastream_revision.status = to_status
                self.datastream_revision.save()

        search_dao = DatastreamSearchDAOFactory().create(self.datastream_revision)
        search_dao.remove()

        self._update_last_revisions()

        self._log_activity(ActionStreams.UNPUBLISH)

    def _unpublish_all(self, to_status=StatusChoices.DRAFT):
        """ Despublica todas las revisiones del datastream y la de todos sus visualization hijos en cascada """

        DataStreamRevision.objects.filter(datastream=self.datastream.id, status=StatusChoices.PUBLISHED)\
            .update(status=to_status)

        with transaction.atomic():
            visualization_revisions = VisualizationRevision.objects.select_for_update().filter(
                visualization__datastream__id=self.datastream.id,
                id=F('visualization__last_published_revision__id'),
                status=StatusChoices.PUBLISHED)

            for visualization_rev in visualization_revisions:
                VisualizationLifeCycleManager(self.user, visualization_revision_id=visualization_rev.id).unpublish(
                    killemall=True, to_status=to_status
                )

    def send_to_review(self, allowed_states=SEND_TO_REVIEW_ALLOWED_STATES):
        """ Envia a revision un datastream """
        if self.datastream_revision.status not in allowed_states:
            logger.info('[LifeCycle - Datastreams - Send to review] Rev. {} El estado {} no esta entre los estados de edicion permitidos.'.format(
                self.datastream_revision.id, self.datastream_revision.status
            ))
            raise IllegalStateException(
                                    from_state=self.datastream_revision.status,
                                    to_state=StatusChoices.PENDING_REVIEW,
                                    allowed_states=allowed_states)

        self._send_childs_to_review()

        self.datastream_revision.status = StatusChoices.PENDING_REVIEW
        self.datastream_revision.save()
        self._log_activity(ActionStreams.REVIEW)

    def _send_childs_to_review(self):
        """ Envia a revision todos las visualizaciones hijas en cascada """

        with transaction.atomic():
            visualization_revs = VisualizationRevision.objects.select_for_update().filter(
                visualization__datastream__id=self.datastream.id,
                id=F('visualization__last_revision__id'),
                status=StatusChoices.DRAFT)

            for visualization_rev in visualization_revs:
               VisualizationLifeCycleManager(self.user, visualization_revision_id=visualization_rev.id).send_to_review()

    def reject(self, allowed_states=REJECT_ALLOWED_STATES):
        """ reject a dataset revision """

        if self.datastream_revision.status not in allowed_states:
            raise IllegalStateException(
                                    from_state=self.datastream_revision.status,
                                    to_state=StatusChoices.DRAFT,
                                    allowed_states=allowed_states)

        self.datastream_revision.status = StatusChoices.DRAFT
        self.datastream_revision.save()
        self._log_activity(ActionStreams.REJECT)

    def edit(self, allowed_states=EDIT_ALLOWED_STATES, changed_fields=None, **fields):
        """ Create new revision or update it
        :param allowed_states:
        :param changed_fields:
        :param fields:
        :return:
        """
        form_status = None

        if 'status' in fields.keys():
            form_status = int(fields.pop('status', None))
        else:
            form_status = StatusChoices.DRAFT

        old_status = self.datastream_revision.status

        if old_status not in allowed_states:
            # Si el estado fallido era publicado, queda aceptado
            if form_status and form_status == StatusChoices.PUBLISHED:
                self.accept()
            raise IllegalStateException(from_state=old_status, to_state=form_status, allowed_states=allowed_states)

        # al clonar el ds_rev tienen uqe viajar los data_source y selecT_statement
        # no sé por qué, pero en el form llegan vacíos, para prevenir que en algún
        # momento viajen via el form (fields) consulto si estan vacíos.
        if fields['data_source'] == "":
            fields['data_source'] = self.datastream_revision.data_source
        if fields['select_statement'] == "":
            fields['select_statement'] = self.datastream_revision.select_statement
        if fields['parameters'] == "":
            fields['parameters'] = self.datastream_revision.datastreamparameter_set.values()

        # si el status de la version anterior es publicado o aprobado
        # genera revisiones de sus hijos
        if old_status in [StatusChoices.PUBLISHED, StatusChoices.APPROVED]:
            self.datastream, self.datastream_revision = DataStreamDBDAO().create(
                datastream=self.datastream,
                dataset=self.datastream_revision.dataset,
                user=self.datastream_revision.user,
                status=fields.pop('status', StatusChoices.DRAFT),
                **fields
            )

            self._move_childs_to_status()

            if form_status == StatusChoices.DRAFT:
                self.unpublish()
            else:
                self._update_last_revisions()
        else:

            # limpiamos el cache antes de salvar el cambio
            self.clean_cache()

            # Actualizo sin el estado
            self.datastream_revision = DataStreamDBDAO().update(
                self.datastream_revision,
                status=fields.pop('status', old_status), 
                changed_fields=changed_fields,
                **fields
            )

            if form_status == StatusChoices.PUBLISHED:
               # Intento publicar, si falla, queda aceptado

                try:
                    self.publish()
                except:
                    self.accept()
                    raise
            else:
                self.datastream_revision.status = form_status
                self.datastream_revision.save()

        self._log_activity(ActionStreams.EDIT)
        return self.datastream_revision

    def _move_childs_to_status(self, status=StatusChoices.PENDING_REVIEW):

        with transaction.atomic():
            visualizations = VisualizationRevision.objects.select_for_update().filter(
                visualization__datastream__id=self.datastream.id,
                id=F('visualization__last_revision__id'),
                status__in=[StatusChoices.PUBLISHED,StatusChoices.APPROVED])

            for visualization in visualizations:
               VisualizationLifeCycleManager(self.user, visualization_revision_id=visualization.id).save_as_status(status)

    def save_as_status(self, status=StatusChoices.DRAFT):
        self.datastream_revision.clone(status)
        self._update_last_revisions()

    def _clone_childs(self):
        with transaction.atomic():
            visualizations = VisualizationRevision.objects.select_for_update().filter(
                visualization__datastream__id=self.datastream.id,
                id=F('visualization__last_revision__id'))

            for visualization in visualizations:
               VisualizationLifeCycleManager(self.user, visualization_revision_id=visualization.id).clone()

    def clone(self):
        dsr = self.datastream_revision.clone(self.datastream_revision.status)
        if dsr.status == StatusChoices.PUBLISHED:
            DatastreamSearchDAOFactory().create(dsr).add()
        self._update_last_revisions()
        self._clone_childs()
        return dsr

    def _log_activity(self, action_id):
        title = self.datastreami18n.title if self.datastreami18n else ''
        resource_category = self.datastream_revision.category.categoryi18n_set.all()[0].name

        return super(DatastreamLifeCycleManager, self)._log_activity(action_id, self.datastream_revision.dataset.id,
            settings.TYPE_DATASTREAM, self.datastream_revision.id, title, resource_category)