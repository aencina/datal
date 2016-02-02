# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError

from optparse import make_option

from core.choices import CollectTypeChoices, SourceImplementationChoices, StatusChoices
from core.models import User,Visualization, VisualizationRevision
from core.daos.visualizations import VisualizationDBDAO
from core.daos.datasets import DatasetDBDAO
from core.daos.datastreams import DataStreamDBDAO


class Command(BaseCommand):
    help = "Index datasets."

    option_list = BaseCommand.option_list + (
        make_option('-u', '--user',
            dest='user_id',
            type="int",
            help='User ID'),
        make_option('-r', '--resource',
            dest='resource_id',
            type="int",
            help='resource id'),
        make_option('-e', '--revision',
            dest='revision_id',
            type="int",
            help='revision id'),
        make_option('-p', '--published',
            action='store_true',
            dest='published',
            default=False,
            help='solo recurso publicado'),
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

    )

    def handle(self, *args, **options):

        if not options['resource_id'] and not options['revision_id']:
            self.help()
            raise CommandError("--resource/-r or --revision/-e obligatorios")

        if not options['dataset'] and not options['datastream'] and not options['visualization']:
            self.help()
            raise CommandError("-T/--dataset|-S/--datastream|-V/--visualization son obligatorios")

        if not options['user_id']:
            self.help()
            raise CommandError("--user/-u obligatorios")


        try:
            self.user = User.objects.get(pk=options['user_id'])

            if options['resource_id']:
                self.resource = VisualizationDBDAO().get(self.user, visualization_id=options['resource_id'],published=options['published'])
            else:
                self.resource = VisualizationDBDAO().get(self.user, visualization_revision_id=options['revision_id'],published=options['published'])

        except User.DoesNotExist:
            raise CommandError(u"Usuario inexistente (administrador: 1647, administrator: 1)")
        except VisualizationRevision.DoesNotExist:
            raise CommandError(u"Revisión inexistente")

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
        pp.pprint(self.resource)
