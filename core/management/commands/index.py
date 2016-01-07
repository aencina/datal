from django.core.management.base import BaseCommand, CommandError

from optparse import make_option
from core.lib.elastic import ElasticsearchIndex

from core.choices import CollectTypeChoices, SourceImplementationChoices, StatusChoices
from core.models import Dataset, DatasetRevision, DataStream, DataStreamRevision, Visualization, VisualizationRevision
from core.lifecycle.datasets import DatasetLifeCycleManager
from core.lifecycle.datasets import DatasetSearchDAOFactory
from core.lifecycle.visualizations import VisualizationSearchDAOFactory
from core.lifecycle.datastreams import DatastreamSearchDAOFactory
from core.daos.datastreams import DatastreamHitsDAO, DataStreamDBDAO
from core.daos.visualizations import *

from core.plugins_point import DatalPluginPoint



class Command(BaseCommand):
    help = "Index datasets."

    option_list = BaseCommand.option_list + (
        make_option('--re-index',
            action='store_true',
            dest='reindex',
            default=False,
            help='Reindex datasets and datastreams'),
    )

    def handle(self, *args, **options):

        # index resources
        if options['reindex']:

            # destruye el index
            ElasticsearchIndex().flush_index()
            es = ElasticsearchIndex()

            for dataset in Dataset.objects.filter(last_published_revision__status=StatusChoices.PUBLISHED):
                datasetrevision=dataset.last_published_revision
                search_dao = DatasetSearchDAOFactory().create(datasetrevision)
                search_dao.add()

            for vz in Visualization.objects.filter(last_published_revision__status=StatusChoices.PUBLISHED):
                vz_revision=vz.last_published_revision
                search_dao = VisualizationSearchDAOFactory().create(vz_revision)
                search_dao.add()

                h = VisualizationHitsDAO(vz_revision)

                doc={
                    'docid': "VZ::%s" % vz.guid,
                    "type": "vz",
                    "doc": {
                        "fields": {
                            "hits": h.count(),
                            "web_hits": h.count(channel_type=0),
                            "api_hits": h.count(channel_type=1)
                        }
                    }
                }
                try:
                    es.update(doc)
                except:
                    pass

            # TODO Hay que usar el metodo query del DAO
            for datastream in DataStream.objects.filter(last_published_revision__status=StatusChoices.PUBLISHED):
                datastreamrevision=datastream.last_published_revision
                datastream_rev = DataStreamDBDAO().get(
                    datastreamrevision.user.language,
                    datastream_revision_id=datastreamrevision.id,
                    published=True
                )
                search_dao = DatastreamSearchDAOFactory().create(datastreamrevision)
                search_dao.add()

                h = DatastreamHitsDAO(datastream_rev)

                doc={
                    'docid': "DS::%s" % datastreamrevision.datastream.guid,
                    "type": "ds",
                    "doc": {
                        "fields": {
                            "hits": h.count(),
                            "web_hits": h.count(channel_type=0),
                            "api_hits": h.count(channel_type=1)
                        }
                    }
                }
                try:
                    es.update(doc)
                except:
                    pass

        for plugin in DatalPluginPoint.get_active_with_att('reindex'):
            plugin.reindex(es)

