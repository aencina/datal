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
        make_option('--all',
            action='store_true',
            dest='all',
            default=False,
            help='Reindex resources'),
        make_option('--flush',
            action='store_true',
            dest='flush',
            default=False,
            help='flush index'),
        make_option('--only-datasets',
            action='store_true',
            dest='datasets',
            default=False,
            help='reindex datasets'),
        make_option('--only-datastreams',
            action='store_true',
            dest='datastreams',
            default=False,
            help='reindex datastreams'),
         make_option('--only-visualizations',
            action='store_true',
            dest='visualizations',
            default=False,
            help='reindex visualization'),
         make_option('--only-dashboards',
            action='store_true',
            dest='dashboards',
            default=False,
            help='reindex dashboards'),
         make_option('--debug',
            action='store_true',
            dest='debug',
            default=False,
            help='debug'),
    )

    def handle(self, *args, **options):

        if not options['all'] and not options['datasets'] and not options['datastreams'] and not options['visualizations'] and not options['dashboards']:
            print "\nUse: "
            print "\n\treindex --<all|datasets|datastreams|visualizations|dashboards> [--flush] [--debug]\n\n"
            print "\t--all\t\t\treindex all resourses"
            print "\t--only-datasets\t\treindex datasets resourses"
            print "\t--only-datastreams\t\treindex datastreams resourses"
            print "\t--only-visualizations\treindex visualizations resourses"
            print "\t--only-dashboards\t\treindex dashboards resourses"
            print "\t--flush\t\t\tflush index"
            print "\t--debug\t\t\tdebug|verbose"
            print "\n"
            return
        


        if options['debug']:
            print "[Otions]"
            for i in options.keys():
                print "\t",i.ljust(15),": ",options[i]

        if options['flush']:
            # destruye el index
            ElasticsearchIndex().flush_index()

        # conectamos con elastic
        self.es = ElasticsearchIndex()

        # index resources
        if options['all']:
            options['datasets']=True
            options['datastreams']=True
            options['visualizations']=True
            options['dashboards']=True

        self.options=options

        self.index_datasets()
        self.index_datastreams()
        self.index_visualizations()
        self.index_dashboards()



    def index_datasets(self):
        if self.options['datasets']:
            if self.options['debug']: print "[Iniciando datasets]"
            for dataset in Dataset.objects.filter(last_published_revision__status=StatusChoices.PUBLISHED):
                datasetrevision=dataset.last_published_revision
                search_dao = DatasetSearchDAOFactory().create(datasetrevision)
                search_dao.add()

    def index_visualizations(self):
        if self.options['visualizations']:
            if self.options['debug']: print "[Iniciando visualizations]"
            for vz in Visualization.objects.filter(last_published_revision__status=StatusChoices.PUBLISHED):
                vz_revision=vz.last_published_revision
                search_dao = VisualizationSearchDAOFactory().create(vz_revision)
                try:
                    search_dao.add()
                except VisualizationI18n.MultipleObjectsReturned:
                    print "[ERROR vz] VisualizationI18n.MultipleObjectsReturned (vz.id= %s)" % vz.id
                    continue
                except AttributeError:
                    print "[ERROR vz] self.visualization_revision.visualization.datastream.last_published_revision == None (vz.id= %s, ds= %s)" % (vz.id, vz.visualization.datastream.id)
                    continue

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
                    self.es.update(doc)
                except:
                    if self.options['debug']: print "[ERROR]: No se pudo ejecutar: ",doc

    def index_datastreams(self):
        if self.options['datastreams']:
            if self.options['debug']: print "[Iniciando datastreams]"
            for datastream in DataStream.objects.filter(last_published_revision__status=StatusChoices.PUBLISHED):
                datastreamrevision=datastream.last_published_revision
                datastream_rev = DataStreamDBDAO().get(
                    datastreamrevision.user.language,
                    datastream_revision_id=datastreamrevision.id,
                    published=True
                )
                search_dao = DatastreamSearchDAOFactory().create(datastreamrevision)
                try:
                    search_dao.add()
                except DatastreamI18n.MultipleObjectsReturned:
                    print "[ERROR ds] DatastreamI18n.MultipleObjectsReturned (ds.id= %s)" % datastream.id
                    continue

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
                    self.es.update(doc)
                except:
                    if self.options['debug']: print "[ERROR]: No se pudo ejecutar: ",doc

    def index_dashboards(self):
        if self.options['dashboards']:
            if self.options['debug']: print "[Iniciando dashboards]"
            for plugin in DatalPluginPoint.get_active_with_att('reindex'):
                plugin.reindex(self.es)

