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

            # FAIL
            if 'getType' in imp['chart']:
                imp['chart']['geoType'] = 'traces'
                imp['chart'].pop("getType", None)

            if 'traceSelection' in imp['chart'] and imp['chart']['traceSelection']:
                imp['chart']['geoType'] = 'traces'

            if 'latitudSelection' in imp['chart'] and 'longitudSelection' in imp['chart'] and imp['chart']['latitudSelection'] and imp['chart']['longitudSelection']:
                imp['chart']['geoType'] = 'points'

            rev.impl_details = json.dumps(imp)
            rev.save()

            print('Se agrego geoType a la Revision Nro: {}'.format(rev.id))
