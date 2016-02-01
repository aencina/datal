from django.core.management.base import BaseCommand

from optparse import make_option

from core.models import (User, Grant, VisualizationRevision, Preference, DataStreamRevision, DatasetRevision, Role,
                         VisualizationI18n, DatastreamI18n, Account)
from core.choices import StatusChoices
import json
from django.db.models import Q


class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option('-a', '--account',
            dest='account',
            type="string",
            help='Reindex resources'),
        )


    def handle(self, *args, **options):
        self.account = None

        if options['account']:
            self.account = Account.objects.get(pk=int(options['account']))

            self.visualization_revision_all = VisualizationRevision.objects.filter(user__account=self.account)
        else:
            self.visualization_revision_all = VisualizationRevision.objects.all()

        for rev in self.visualization_revision_all:
            imp = json.loads(rev.impl_details)

            if 'invertedAxis' in imp['format']:
                if imp['format']['invertedAxis'] == 'checked':

                    if 'headerSelection' in imp['chart'].keys():
                        print "[InvertedAxis Pre] Account ID: %s; Revision ID: %s; headerSelection: %s; labelSelection: %s" %(self.account.id, rev.id, imp['chart']['headerSelection'], imp['chart']['labelSelection'])
                    else:
                        print "[InvertedAxis Pre] Account ID: %s; Revision ID: %s; headerSelection: Empty; labelSelection: %s" %(self.account.id, rev.id, imp['chart']['labelSelection'])

                    if imp['chart']['labelSelection'] == ":":
                        imp['chart']['labelSelection'] = ""

                    if 'headerSelection' in imp['chart'].keys() and imp['chart']['headerSelection'] == ":":
                        imp['chart']['headerSelection'] = ""

                    aux = imp['chart']['headerSelection']

                    imp['chart']['headerSelection'] = imp['chart']['labelSelection']
                    imp['chart']['labelSelection'] = aux

                    rev.impl_details = json.dumps(imp)
                
                    print "[InvertedAxis Post] Account ID: %s; Revision ID: %s; headerSelection: %s; labelSelection: %s" %(self.account.id, rev.id, imp['chart']['headerSelection'], imp['chart']['labelSelection'])
                    rev.save()

