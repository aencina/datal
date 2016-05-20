# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError

from optparse import make_option

from django.conf import settings
from elasticsearch import Elasticsearch, NotFoundError, RequestError



class Command(BaseCommand):
    help = "Index datasets."

    option_list = BaseCommand.option_list + (
        make_option('-q', '--query',
            dest='query',
            type="string",
            help='Query'),
        make_option('-r', '--resource',
            dest='resource_id',
            type="int",
            help='resource id'),
        make_option('-e', '--revision',
            dest='revision_id',
            type="int",
            help='revision id'),
        make_option('-T', '--dataset',
            action='store_true',
            dest='dataset',
            default=False,
            help='buscar dataset'),
        make_option('-S', '--datastream',
            action='store_true',
            dest='datastream',
            default=False,
            help='buscar datastream'),
        make_option('-V', '--visualization',
            action='store_true',
            dest='visualization',
            default=False,
            help='buscar visualization'),
        make_option('-D', '--dashboard',
            action='store_true',
            dest='dashboard',
            default=False,
            help='buscar dashboard'),

    )

    def handle(self, *args, **options):
        
        print options

        if options['dataset']:
            resources=["dt"]
        elif options['datastream']:
            resources=["ds"]
        elif options['visualization']:
            resources=["vz"]
        elif options['dashboard']:
            resources=["db"]
        else:
            resources=["dt","ds","db","vz"]

        self.es = Elasticsearch(settings.SEARCH_INDEX['url'])

        if options['resource_id']:
            query={"query": {
                "bool": {
                    "must":[
                        {"match": {"resource_id": options['resource_id']} },
                    ],
                }
            } }


        elif options['revision_id']:
            query={"query": {
                "bool": {
                    "must":[
                        {"match": {"revision_id": options['revision_id']} },
                    ],
                }
            } }

        elif options['query']:
            query= {
                "query": {
                    "filtered": {
                        "query": {
                            "query_string": {
                                "query": options['query'],
                                "fields": ["title", "text"]
                            }
                        },
                        "filter": {
                            "bool": {
                                "must": [{"terms": {"type": resources}}]
                            }
                        }
                    }
                }
            }

        else:
            self.help()
            raise
        
        print query
        self.results = self.es.search(index=settings.SEARCH_INDEX['index'], body=query)
        self.print_resource()

    def help(self):
        print "\n"
        for i in self.option_list:
            if i.action == "store":
                print "\t %s %s\t- %s" % (i.get_opt_string().ljust(10), i.dest.ljust(20), i.help)
            else:
                print "\t %s \t- %s" % (i.get_opt_string().ljust(30), i.help)
        print "\n"

    def print_resource(self):
        import pprint
        pp = pprint.PrettyPrinter(indent=2)
        pp.pprint(self.results)
