from django.core.management.base import BaseCommand
from django.utils import translation

from core.models import DataStreamRevision, DatasetRevision, VisualizationRevision
from core.lifecycle.datasets import DatasetLifeCycleManager
from core.lifecycle.datastreams import DatastreamLifeCycleManager
from core.lifecycle.visualizations import VisualizationLifeCycleManager
from core.choices import ActionStreams


class Command(BaseCommand):
    help = "Crear logs de actividades de datos existentes."

    def handle(self, *args, **options):
        # OH SI, Hardcodeo el idioma
        # en realidad deberia cambiar el loc

        for dataset_rev in DatasetRevision.objects.all():
            try:
                translation.activate(dataset_rev.user.language)
                lifecycle = DatasetLifeCycleManager(dataset_rev.user, dataset_revision_id=dataset_rev.id)
                lifecycle._log_activity(ActionStreams.CREATE)
            except:
                pass
            finally:
                translation.deactivate()

        for datastream_rev in DataStreamRevision.objects.all():
            try:
                translation.activate(datastream_rev.user.language)
                lifecycle = DatastreamLifeCycleManager(datastream_rev.user, datastream_revision_id=datastream_rev.id)
                lifecycle._log_activity(ActionStreams.CREATE)
            except:
                pass
            finally:
                translation.deactivate()

        #for visualization_rev in VisualizationRevision.objects.all():
        #    translation.activate(visualization_rev.user.language)
        #    lifecycle = VisualizationLifeCycleManager(
        #        visualization_rev.user,
        #        visualization_revision_id=visualization_rev.id
        #    )
        #    lifecycle._log_activity(ActionStreams.CREATE)
        #    translation.deactivate()
