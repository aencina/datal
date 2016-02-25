from django.core.management.base import BaseCommand

from optparse import make_option

from core.models import (Account, Tag, TagDataset, TagDatastream, TagVisualization)
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
        if options['account']:
            guids = []

            f = open('/tmp/{}/dataset.json'.format(options['account']), 'r')
            fixtures = json.load(f)
            f.close()
            new_fixtures = []
            for fixture in fixtures:
                if fixture['fields']['guid'] not in guids:
                    guids.append(fixture['fields']['guid'])
                else:
                    print "VIEJO GUID: {}".format(fixture['fields']['guid'])
                    partes = fixture['fields']['guid'].split('-')
                    partes[4] = str(int(partes[4]) + 1)
                    new_guid = '-'.join(partes)
                    print "NUEVO GUID: {}".format(new_guid)
                    guids.append(new_guid)
                    fixture['fields']['guid'] = new_guid
                new_fixtures.append(fixture)
            f = open('/tmp/{}/dataset.json'.format(options['account']), 'w')
            json.dump(new_fixtures, f)
            f.close()
