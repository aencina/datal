# -*- coding: utf-8 -*-
from django.db.models import F, Max
from django.db import transaction

from core.builders.datasets import DatasetImplBuilderWrapper
from core.choices import ActionStreams, StatusChoices
from core.daos.datasets import DatasetDBDAO, DatasetSearchDAOFactory
from core.exceptions import DatasetNotFoundException, IllegalStateException
from core.lib.datastore import *
from core.lifecycle.resource import AbstractLifeCycleManager
from core.lifecycle.datastreams import DatastreamLifeCycleManager
from core.lifecycle.visualizations import VisualizationLifeCycleManager
from core.models import (DatasetRevision, Dataset, DataStream, DataStreamRevision, DatasetI18n, VisualizationRevision)


CREATE_ALLOWED_STATES = [StatusChoices.DRAFT, StatusChoices.PENDING_REVIEW, StatusChoices.APPROVED,
                         StatusChoices.PUBLISHED]
PUBLISH_ALLOWED_STATES = [StatusChoices.DRAFT, StatusChoices.PENDING_REVIEW, StatusChoices.APPROVED,
                          StatusChoices.PUBLISHED]
UNPUBLISH_ALLOWED_STATES = [StatusChoices.DRAFT, StatusChoices.PUBLISHED]
SEND_TO_REVIEW_ALLOWED_STATES = [StatusChoices.DRAFT]
ACCEPT_ALLOWED_STATES = [StatusChoices.DRAFT, StatusChoices.PENDING_REVIEW]
REJECT_ALLOWED_STATES = [StatusChoices.PENDING_REVIEW]
REMOVE_ALLOWED_STATES = [StatusChoices.DRAFT, StatusChoices.APPROVED, StatusChoices.PUBLISHED]
EDIT_ALLOWED_STATES = [StatusChoices.DRAFT, StatusChoices.APPROVED, StatusChoices.PUBLISHED]

logger = logging.getLogger(__name__)


class DatasetLifeCycleManager(AbstractLifeCycleManager):
    """ Manage a Dataset Life Cycle"""

    def unpublish(self, killemall=False, allowed_states=UNPUBLISH_ALLOWED_STATES):
        """ Despublica la revision de un dataset
        :param allowed_states:
        :param killemall:
        """

        if self.dataset_revision.status not in allowed_states:
            raise IllegalStateException(
                from_state=self.dataset_revision.status,
                to_state=StatusChoices.DRAFT,
                allowed_states=allowed_states
            )

        if killemall:
            self._unpublish_all()
        else:
            revcount = DatasetRevision.objects.filter(dataset=self.dataset.id, status=StatusChoices.PUBLISHED).count()

            if revcount == 1:
                self._unpublish_all()
            else:
                self.dataset_revision.status = StatusChoices.DRAFT
                self.dataset_revision.save()

        search_dao = DatasetSearchDAOFactory().create(self.dataset_revision)
        search_dao.remove()
        self._update_last_revisions()

        self._log_activity(ActionStreams.UNPUBLISH)

    def __init__(self, user, resource=None, language=None, dataset_id=0, dataset_revision_id=0):
        super(DatasetLifeCycleManager, self).__init__(user, language)
        # Internal used resources (optional). You could start by dataset or revision

        try:
            if type(resource) == Dataset:
                self.dataset = resource
                self.dataset_revision = DatasetRevision.objects.select_related().get(pk=self.dataset.last_revision_id)
            elif type(resource) == DatasetRevision:
                self.dataset_revision = resource
                self.dataset=resource.dataset
            elif dataset_id > 0:
                self.dataset = Dataset.objects.get(pk=dataset_id)
                self.dataset_revision = DatasetRevision.objects.select_related().get(pk=self.dataset.last_revision_id)
            elif dataset_revision_id > 0:
                self.dataset_revision = DatasetRevision.objects.select_related().get(pk=dataset_revision_id)
                self.dataset = self.dataset_revision.dataset
            else:
                self.dataset_revision = None
                self.dataset = None
        except Dataset.DoesNotExist, DatasetRevision.DoesNotExist:
            raise DatasetNotFoundException()

        if self.dataset and self.dataset_revision:
            self.dataseti18n = DatasetI18n.objects.get(dataset_revision=self.dataset_revision,
                                                       language=self.dataset.user.language)

    def create(self, collect_type='index', allowed_states=CREATE_ALLOWED_STATES, language=None, **fields):
        """ Create a new Dataset
        :param fields:
        :param language:
        :param allowed_states:
        :param collect_type:
        """
        logger.info('Creating datset')
        
        # Check for allowed states
        status = int(fields.get('status', StatusChoices.DRAFT))

        if status not in allowed_states:
            raise IllegalStateException(
                                    from_state=None,
                                    to_state=status, 
                                    allowed_states=allowed_states)

        language = fields.get('language', language)

        # Process file_data if exists
        file_data = fields.get('file_data', None)
        if file_data is not None:
            fields['file_size'] = file_data.size
            fields['file_name'] = file_data.name
            fields['end_point'] = 'file://' + active_datastore.create(settings.AWS_BUCKET_NAME, file_data.file,
                                                                      self.user.account.id, self.user.id)

        impl_details = DatasetImplBuilderWrapper(**fields).build()

        self.dataset, self.dataset_revision = DatasetDBDAO().create(user=self.user,
            collect_type=collect_type, title=fields['title'], description=fields['description'],
            language=language, status=int(status), category=fields['category'], impl_type=fields['impl_type'],
            file_name=fields['file_name'], end_point=fields['end_point'], file_size=fields.get('file_size', 0),
            notes=fields.get('notes', ''), license_url=fields.get('license_url',''), spatial=fields.get('spatial', ''),
            frequency=fields.get('frequency', ''), mbox=fields.get('mbox', ''), tags=fields.get('tags', []),
            sources=fields.get('sources', []), params=fields.get('params', []), impl_details=impl_details)

        self.dataseti18n = DatasetI18n.objects.get(
            dataset_revision=self.dataset_revision,
            language=self.dataset.user.language
        )

        self._log_activity(ActionStreams.CREATE)

        # En caso de seleccionar que este publicado
        if status == StatusChoices.PUBLISHED:
            self.publish(allowed_states=CREATE_ALLOWED_STATES)
        else:
            self._update_last_revisions()

        return self.dataset_revision

    def publish(self, allowed_states=PUBLISH_ALLOWED_STATES):
        """ Publica una revision de dataset
        :param allowed_states:
        """
        logger.info('[LifeCycle - Dataset - Publish] Publico Rev. {}.'.format(self.dataset_revision.id))

        if self.dataset_revision.status not in allowed_states:
            logger.info('[LifeCycle - Dataset - Edit] Rev. {} El estado {} no esta entre los estados de edicion permitidos.'.format(
                self.dataset_revision.id, self.dataset_revision.status
            ))
            raise IllegalStateException(
                                    from_state=self.dataset_revision.status,
                                    to_state=StatusChoices.PUBLISHED,
                                    allowed_states=allowed_states)

        self.dataset_revision.status = StatusChoices.PUBLISHED
        self.dataset_revision.save()
            
        self._update_last_revisions()

        # si hay DataStreamRevision publicados, no dispara la publicacion en cascada
        if DataStreamRevision.objects.filter(dataset=self.dataset, last_published_revision__isnull=True).exists():
            self._publish_childs()
            
        search_dao = DatasetSearchDAOFactory().create(self.dataset_revision)
        search_dao.add()
            
        self._log_activity(ActionStreams.PUBLISH)

    def _publish_childs(self):
        """ Intenta publicar la ultima revision de los datastreams hijos"""

        with transaction.atomic():
            datastream_revisions = DataStreamRevision.objects.select_for_update().filter(
                dataset=self.dataset.id,
                id=F('datastream__last_revision__id'),
            )
            publish_fail = list()
            for datastream_revision in datastream_revisions:
                logger.info('[LifeCycle - Dataset - Publish Childs] Dataset {} Publico Datastream Rev. hijo {}.'.format(
                    self.dataset.id, datastream_revision.id
                ))
                try:
                    DatastreamLifeCycleManager(user=self.user, datastream_revision_id=datastream_revision.id).publish(
                        allowed_states=[StatusChoices.APPROVED], parent_status=StatusChoices.PUBLISHED
                    )
                except IllegalStateException:
                    # si no tiene ninguna revision publicada, que no lo agregue a la lista de fallas
                    if datastream_revision.last_published_revision.exists():
                        publish_fail.append(datastream_revision)


            ## Aca deberia ir lo mismo que los ds, pero para las vz?

            if publish_fail:
                raise ChildNotApprovedException(self.dataset.last_revision, settings.TYPE_DATASTREAM)

    def _unpublish_all(self):
        """ Despublica todas las revisiones del dataset y la de todos sus datastreams hijos en cascada """

        DatasetRevision.objects.filter(dataset=self.dataset.id, status=StatusChoices.PUBLISHED)\
            .update(status=StatusChoices.DRAFT)

        with transaction.atomic():
            datastream_revisions = DataStreamRevision.objects.select_for_update().filter(
                dataset=self.dataset.id,
                id=F('datastream__last_published_revision__id'),
                status=StatusChoices.PUBLISHED
            )

            for datastream_revision in datastream_revisions:
                DatastreamLifeCycleManager(self.user, datastream_revision_id=datastream_revision.id).unpublish(
                    killemall=True, to_status=StatusChoices.PENDING_REVIEW)

    def send_to_review(self, allowed_states=SEND_TO_REVIEW_ALLOWED_STATES):
        """ Envia a revision un dataset
        :param allowed_states:
        """
        if self.dataset_revision.status not in allowed_states:
            logger.info('[LifeCycle - Dataset - Send to review] Rev. {} El estado {} no esta entre los estados de edicion permitidos.'.format(
                self.dataset_revision.id, self.dataset_revision.status
            ))
            raise IllegalStateException(
                from_state=self.dataset_revision.status,
                to_state=StatusChoices.PENDING_REVIEW,
                allowed_states=allowed_states
            )
        self._send_childs_to_review()

        self.dataset_revision.status = StatusChoices.PENDING_REVIEW
        self.dataset_revision.save()
        self._log_activity(ActionStreams.REVIEW)

    def _send_childs_to_review(self):
        """ Envia a revision todos los datastreams hijos en cascada """
        with transaction.atomic():
            datastreams_revisions = DataStreamRevision.objects.select_for_update().filter(
                dataset=self.dataset.id,
                id=F('datastream__last_revision__id'),
                status=StatusChoices.DRAFT
            )

            for datastream_revision in datastreams_revisions:
                DatastreamLifeCycleManager(self.user, datastream_revision_id=datastream_revision.id).send_to_review()

    def accept(self, allowed_states=ACCEPT_ALLOWED_STATES):
        """ accept a dataset revision
        :param allowed_states:
        """
        if self.dataset_revision.status != StatusChoices.APPROVED:
            if self.dataset_revision.status not in allowed_states:
                raise IllegalStateException(
                                        from_state=self.dataset_revision.status,
                                        to_state=StatusChoices.APPROVED,
                                        allowed_states=allowed_states)

            self.dataset_revision.status = StatusChoices.APPROVED
            self.dataset_revision.save()
            self._log_activity(ActionStreams.ACCEPT)

    def reject(self, allowed_states=REJECT_ALLOWED_STATES):
        """ reject a dataset revision
        :param allowed_states:
        """

        if self.dataset_revision.status not in allowed_states:
            raise IllegalStateException(
                                    from_state=self.dataset_revision.status,
                                    to_state=StatusChoices.DRAFT,
                                    allowed_states=allowed_states)

        self.dataset_revision.status = StatusChoices.DRAFT
        self.dataset_revision.save()
        self._log_activity(ActionStreams.REJECT)

    def remove(self, killemall=False, allowed_states=REMOVE_ALLOWED_STATES):
        """ Elimina una revision o todas las revisiones de un dataset y la de sus datastreams hijos en cascada
        :param allowed_states:
        :param killemall:
        """

        # Tener en cuenta que si es necesario ejecutar varios delete, debemos crear un nuevo objecto LifeCycle
        if settings.DEBUG: logger.info('removing dataset rev %d all:%s' % (self.dataset_revision.id, str(killemall)))
        if self.dataset_revision.status not in allowed_states:
            raise IllegalStateException(
                                    from_state=self.dataset_revision.status,
                                    to_state=None,
                                    allowed_states=allowed_states)

        if not killemall:
            _revisions = DatasetRevision.objects.filter(dataset=self.dataset.id)
            killemall = _revisions.count() == 1

        # si la revision a eliminar es la unica revision
        # elimino todos los recursos asociados a ella
        if killemall:
            self._remove_all()

        else:
            revision_published_count = _revisions.filter(status=StatusChoices.PUBLISHED).count()

            # Si la revision a eliminar es la unica publicada y es la que vamos a eliminar,
            # entonces despublicar todos los datastreams en cascada
            if revision_published_count == 1 and self.dataset.last_published_revision == self.dataset_revision:
                self._unpublish_all()

            # Fix para evitar el fallo de FK con las published revision. Luego la funcion update_last_revisions
            # completa el valor correspondiente.
            self.dataset.last_published_revision = None
            self.dataset.save()

            # Elimino revision del dataset
            self.dataset_revision.delete()

        self._update_last_revisions()
        self._log_activity(ActionStreams.DELETE)
        if settings.DEBUG: logger.info('Clean Caches')
        self._delete_cache(cache_key='my_total_datasets_%d' % self.dataset.user.id)
        self._delete_cache(cache_key='account_total_datasets_%d' % self.dataset.user.account.id)

    def _remove_all(self):
        # Remove all asociated datastreams revisions

        for datastream_revision in DataStreamRevision.objects.filter(dataset=self.dataset.id):
            DatastreamLifeCycleManager(self.user,resource=datastream_revision).remove(killemall=True)

        self.dataset.delete()
        self._log_activity(ActionStreams.DELETE)
        self._delete_cache(cache_key='my_total_datasets_%d' % self.dataset.user.id)
        self._delete_cache(cache_key='account_total_datasets_%d' % self.dataset.user.account.id)

    def edit(self, allowed_states=EDIT_ALLOWED_STATES, changed_fields=None, **fields):
        """ Create new revision or update it """
        old_status = self.dataset_revision.status

        if old_status not in allowed_states:
            logger.info('[LifeCycle - Dataset - Edit] Rev. {} El estado {} no esta entre los estados de edicion permitidos.'.format(
                self.dataset_revision.id, old_status
            ))
            raise IllegalStateException(from_state=old_status, to_state=fields.pop('status', None), allowed_states=allowed_states)

        file_data = fields.get('file_data', None)
        if file_data is not None:
            fields['file_size'] = file_data.size
            fields['file_name'] = file_data.name
            fields['end_point'] = 'file://' + active_datastore.create(settings.AWS_BUCKET_NAME, file_data,
                                                                      self.user.account.id, self.user.id)
            changed_fields += ['file_size', 'file_name', 'end_point']
        else:
            if fields.has_key('end_point') and not fields['end_point']:
                fields['file_size'] = self.dataset_revision.size
                fields['file_name'] = self.dataset_revision.filename
                fields['end_point'] = self.dataset_revision.end_point

        impl_details = DatasetImplBuilderWrapper(**fields).build()

        if old_status == StatusChoices.PUBLISHED:
            logger.info('[LifeCycle - Dataset - Edit] Rev. {} Creo nueva revision por estar PUBLISHED.'.format(
                self.dataset_revision.id
            ))
            self.dataset, self.dataset_revision = DatasetDBDAO().create(
                dataset=self.dataset, user=self.user, 
                status=fields.pop('status', StatusChoices.DRAFT), 
                impl_details=impl_details,
                **fields)
            logger.info('[LifeCycle - Dataset - Edit] Rev. {} Muevo sus hijos a PENDING_REVISION.'.format(
                self.dataset_revision.id
            ))
            self._move_childs_to_status()
            self._update_last_revisions()
        else:
            logger.info('[LifeCycle - Dataset - Edit] Rev. {} Actualizo sin crear nueva revision por su estado {}.'.format(
                self.dataset_revision.id, old_status
            ))

            # Actualizo sin el estado
            self.dataset_revision = DatasetDBDAO().update(
                self.dataset_revision,
                status=fields.pop('status', old_status), 
                changed_fields=changed_fields,
                **fields
            )

        self._log_activity(ActionStreams.EDIT)
        return self.dataset_revision

    def update_file(self, **fields):
        """ Create new revision or update it
        :param fields:
        """
        file_data = fields.get('file_data', None)
        if file_data is not None:
            fields['file_size'] = file_data.size
            fields['file_name'] = file_data.name
            fields['end_point'] = 'file://' + active_datastore.create(settings.AWS_BUCKET_NAME, file_data,
                                                                      self.user.account.id, self.user.id)
            changed_fields = ['file_size', 'file_name', 'end_point']

            # Actualizo sin el estado
            self.dataset_revision = DatasetDBDAO().update(
                self.dataset_revision,
                changed_fields=changed_fields,
                **fields
            )

        self._log_activity(ActionStreams.EDIT)
        return self.dataset_revision

    def _move_childs_to_status(self, status=StatusChoices.PENDING_REVIEW):
        """
        Muevo las vistas y las visualizaciones asociadas a este dataset a status 
        :return:
        """
        with transaction.atomic():
            datastream_revisions = DataStreamRevision.objects.select_for_update().filter(
                dataset=self.dataset.id,
                id=F('datastream__last_revision__id'),
                status=StatusChoices.PUBLISHED
            )

            for datastream_revision in datastream_revisions:
                DatastreamLifeCycleManager(self.user, datastream_revision_id=datastream_revision.id).save_as_status(status)

            visualization_revs = VisualizationRevision.objects.select_for_update().filter(
                visualization__datastream__last_revision__dataset__id=self.dataset.id,
                id=F('visualization__last_revision__id'),
                status=StatusChoices.PUBLISHED
            )

            for revision in visualization_revs:
                VisualizationLifeCycleManager(self.user, visualization_revision_id=revision.id).save_as_status(status)

    def save_as_status(self, status=StatusChoices.DRAFT):
        self.dataset_revision.clone(status)
        self._update_last_revisions()

    def _log_activity(self, action_id):
        resource_category = self.dataset_revision.category.categoryi18n_set.all()[0].name

        return super(DatasetLifeCycleManager, self)._log_activity(action_id, self.dataset.id, 
                                                                  settings.TYPE_DATASET,
                                                                  self.dataset_revision.id, 
                                                                  self.dataseti18n.title,
                                                                  resource_category)

    def _update_last_revisions(self):
        """ update last_revision_id and last_published_revision_id """

        last_revision_id = DatasetRevision.objects.filter(dataset=self.dataset.id).aggregate(Max('id'))['id__max']

        self.dataset.last_revision_id = last_revision_id
        if last_revision_id:
            self.dataset.last_revision = DatasetRevision.objects.get(pk=last_revision_id)
            last_published_revision_id = DatasetRevision.objects.filter(
                dataset=self.dataset.id,
                status=StatusChoices.PUBLISHED).aggregate(Max('id')
            )['id__max']

            # si hay un last_published_revision_id, dejamos ese como ultimo publicado
            # además mandamos al indexador esa version que estaba publicada
            if last_published_revision_id:
                self.dataset.last_published_revision = DatasetRevision.objects.get(pk=last_published_revision_id)                   
                search_dao = DatasetSearchDAOFactory().create(self.dataset.last_published_revision)
                search_dao.add()

                # esto pasa cuando borras un DT rev que no esta publicado
                # al volver a publicar la ultima rev, se ejecutaba el log_activity
                # y fallaba porque self.dataset_revision esta en None (porque fue eliminado)
                # pero ademas, en la actividad se mostraba que se publicaba una revision, que ya estaba publicada
                if not self.dataset_revision:
                    self._log_activity(ActionStreams.PUBLISH)
            else:
                self.dataset.last_published_revision = None

            self.dataset.save()
        else:
            # Si fue eliminado pero falta el commit, evito borrarlo nuevamente
            if self.dataset.id:
                self.dataset.delete()
