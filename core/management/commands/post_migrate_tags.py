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
            f = open('/tmp/{}/tag.json'.format(options['account']), 'r')
            tag_fixtures = json.load(f)
            f.close()
            fixed_tags = []
            for tag_fixture in tag_fixtures:
                try:
                    tag = Tag.objects.get(name=tag_fixture['fields']['name'])
                    old_id = tag_fixture['pk']
                except:
                    fixed_tags.append(tag_fixture)
                    continue

                # Verifico los tagDatastream
                f = open('/tmp/{}/tagdatastream.json'.format(options['account']), 'r')
                tagdatastream_fixtures = json.load(f)
                f.close()
                fixed_fixtures = []

                for tagdatastreamfixture in tagdatastream_fixtures:
                    if tagdatastreamfixture['fields']['tag'] == old_id:
                        tagdatastreamfixture['fields']['tag'] = tag.id
                        print "FIX DE TAG DATASTREAM: ID {}".format(old_id)
                    fixed_fixtures.append(tagdatastreamfixture)

                f = open('/tmp/{}/tagdatastream.json'.format(options['account']), 'w')
                json.dump(fixed_fixtures, f)
                f.close()

                # Verifico los tagDashboards
                f = open('/tmp/{}/tagdashboard.json'.format(options['account']), 'r')
                tagdashboard_fixtures = json.load(f)
                f.close()
                fixed_fixtures = []

                for tagdashboardfixture in tagdashboard_fixtures:
                    if tagdashboardfixture['fields']['tag'] == old_id:
                        tagdashboardfixture['fields']['tag'] = tag.id
                        print "FIX DE TAG DASHBOARD: ID {}".format(old_id)
                    fixed_fixtures.append(tagdashboardfixture)

                f = open('/tmp/{}/tagdashboard.json'.format(options['account']), 'w')
                json.dump(fixed_fixtures, f)
                f.close()

            f = open('/tmp/{}/tag.json'.format(options['account']), 'w')
            json.dump(fixed_tags, f)
            f.close()
