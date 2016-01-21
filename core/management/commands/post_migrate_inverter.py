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
                    aux = imp['chart']['headerSelection']

                    if imp['chart']['labelSelection'] == ":":
                        imp['chart']['headerSelection'] = ""
                    else:
                        imp['chart']['headerSelection'] = imp['chart']['labelSelection']

                    if aux:
                        imp['chart']['labelSelection'] = aux
                    else:
                        imp['chart']['labelSelection'] = ":"

                    rev.impl_details = json.dumps(imp)
                
                    if imp['chart']['headerSelection'] and  imp['chart']['labelSelection'] != ":":
                        print "[InvertedAxis True] Account ID: %s; Revision ID: %s; headerSelection: %s; labelSelection: %s" %(self.account.id, rev.id, imp['chart']['headerSelection'], imp['chart']['labelSelection'])
                        rev.save()

