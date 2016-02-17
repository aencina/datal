from django.core.management.base import BaseCommand, CommandError
from django.db.models.deletion import ProtectedError

from optparse import make_option

from core.models import *


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--delete',
            action='store_true',
            dest='delete',
            default=False,
            help='Delete selected Accounts'),

        make_option('--just-ids',
            dest='just_ids',
            default=[],
            help='Delete just accounts IDs given'),

        make_option('--exclude-ids',
            dest='exclude_ids',
            default=[],
            help='Delete all accounts except IDs given'),
        )

    def handle(self, *args, **options):

        queryset = Account.objects.all()
        retry = []

        if options['just_ids']:
            queryset = queryset.filter(id__in=options['just_ids'].split(','))

        if options['exclude_ids']:
            queryset = queryset.exclude(id__in=options['exclude_ids'].split(','))

        for account in queryset:
            try:
                self.stdout.write('Account ID {}: {}. Parent: {}'.format(account.id, account.name, account.parent))
            except:
                self.stdout.write('Account ID {}.'.format(account.id))


            # Remove users from account
            for user in User.objects.filter(account=account):

                # Remove Visualization
                for visualization in Visualization.objects.filter(user=user):

                    # Remove VisualizationHits
                    for visualizationhits in VisualizationHits.objects.filter(visualization=visualization):
                        self.stdout.write('\tVisualizationHits ID {}.'.format(visualizationhits.id))

                        if options['delete']:
                            visualizationhits.delete()

                    # Remove ObjectGrant
                    for objectgrant in ObjectGrant.objects.filter(visualization=visualization):
                        self.stdout.write('\tObjectGrant ID {}.'.format(objectgrant.id))

                        if options['delete']:
                            objectgrant.delete()

                    # Remove Log
                    for log in Log.objects.filter(visualization=visualization):
                        self.stdout.write('\tLog ID {}.'.format(log.id))

                        if options['delete']:
                            log.delete()

                    self.stdout.write('\tVisualization ID {}.'.format(visualization.id))

                    if options['delete']:
                        visualization.delete()


                # Remove VisualizationRevision
                for visualizationrevision in VisualizationRevision.objects.filter(user=user):

                    # Remove VisualizationI18n
                    for visualizationi18n in VisualizationI18n.objects.filter(visualization_revision=visualizationrevision):
                        self.stdout.write('\tVisualizationI18n ID {}.'.format(visualizationi18n.id))

                        if options['delete']:
                            visualizationi18n.delete()

                    # Remove TagVisualization
                    for tagvisualization in TagVisualization.objects.filter(visualizationrevision=visualizationrevision):
                        self.stdout.write('\tTagVisualization ID {}.'.format(tagvisualization.id))

                        if options['delete']:
                            tagvisualization.delete()

                    self.stdout.write('\tVisualizationRevision ID {}.'.format(visualizationrevision.id))

                    if options['delete']:
                        visualizationrevision.delete()

                # Remove UserPassTickets
                for userpasstickets in UserPassTickets.objects.filter(user=user):
                    try:
                        self.stdout.write('\tUserPassTickets {}.'.format(userpasstickets.type))
                    except:
                        self.stdout.write('\tUserPassTickets ID {}.'.format(userpasstickets.id))

                    if options['delete']:
                        userpasstickets.delete()

                # Remove DataStreamComment
                for datastreamcomment in DataStreamComment.objects.filter(user=user):
                    self.stdout.write('\tDataStreamComment ID {}.'.format(datastreamcomment.id))

                    if options['delete']:
                        datastreamcomment.delete()

                # Remove Dataset
                for dataset in Dataset.objects.filter(user=user):
                    self.stdout.write('\tDataset ID {}.'.format(dataset.id))

                    if options['delete']:
                        dataset.delete()

                # Remove DatasetRevision
                for datasetrevision in DatasetRevision.objects.filter(user=user):

                    # Remove SourceDataset
                    for sourcedataset in SourceDataset.objects.filter(datasetrevision=datasetrevision):
                        self.stdout.write('\tSourceDataset ID {}.'.format(sourcedataset.id))

                        if options['delete']:
                            sourcedataset.delete()

                    # Remove DatasetI18n
                    for dataseti18n in DatasetI18n.objects.filter(dataset_revision=datasetrevision):
                        self.stdout.write('\tDatasetI18n ID {}.'.format(dataseti18n.id))

                        if options['delete']:
                            dataseti18n.delete()

                    # Remove TagDataset
                    for tagdataset in TagDataset.objects.filter(datasetrevision=datasetrevision):
                        self.stdout.write('\tTagDataset ID {}.'.format(tagdataset.id))

                        if options['delete']:
                            tagdataset.delete()


                    self.stdout.write('\tDatasetRevision ID {}.'.format(datasetrevision.id))

                    if options['delete']:
                        datasetrevision.delete()

                # Remove DataStream
                for datastream in DataStream.objects.filter(user=user):

                    # Remove Log
                    for log in Log.objects.filter(datastream=datastream):
                        self.stdout.write('\tLog ID {}.'.format(log.id))

                        if options['delete']:
                            log.delete()

                    # Remove DataStreamHits
                    for dataStreamhits in DataStreamHits.objects.filter(datastream=datastream):
                        self.stdout.write('\tDataStreamHits ID {}.'.format(dataStreamhits.id))

                        if options['delete']:
                            dataStreamhits.delete()

                    # Remove ObjectGrant
                    for objectgrant in ObjectGrant.objects.filter(datastream=datastream):
                        self.stdout.write('\tObjectGrant ID {}.'.format(objectgrant.id))

                        if options['delete']:
                            objectgrant.delete()

                    # Remove DataStreamRank
                    for datastreamrank in DataStreamRank.objects.filter(datastream=datastream):
                        self.stdout.write('\tDataStreamRank ID {}.'.format(datastreamrank.id))

                        if options['delete']:
                            datastreamrank.delete()

                    self.stdout.write('\tDataStream ID {}.'.format(datastream.id))

                    if options['delete']:
                        datastream.delete()

                # Remove DataStreamRevision
                for datastreamrevision in DataStreamRevision.objects.filter(user=user):

                    # Remove SourceDatastream
                    for sourcedatastream in SourceDatastream.objects.filter(datastreamrevision=datastreamrevision):
                        self.stdout.write('\tSourceDatastream ID {}.'.format(sourcedatastream.id))

                        if options['delete']:
                            sourcedatastream.delete()

                    # Remove TagDatastream
                    for tagdatastream in TagDatastream.objects.filter(datastreamrevision=datastreamrevision):
                        self.stdout.write('\tTagDatastream ID {}.'.format(tagdatastream.id))

                        if options['delete']:
                            tagdatastream.delete()

                    # Remove DataStreamParameter
                    for datastreamparameter in DataStreamParameter.objects.filter(datastream_revision=datastreamrevision):
                        self.stdout.write('\tDataStreamParameter ID {}.'.format(datastreamparameter.id))

                        if options['delete']:
                            datastreamparameter.delete()

                    self.stdout.write('\tDataStreamRevision ID {}.'.format(datastreamrevision.id))

                    if options['delete']:
                        datastreamrevision.delete()

                    # Remove DatastreamI18n
                    for datastreami18n in DatastreamI18n.objects.filter(datastream_revision=datastreamrevision):
                        self.stdout.write('\tDatastreamI18n ID {}.'.format(datastreami18n.id))

                        if options['delete']:
                            datastreami18n.delete()

                # Remove Log
                for log in Log.objects.filter(user=user):
                    self.stdout.write('\tLog ID {}.'.format(log.id))

                    if options['delete']:
                        log.delete()

                # Remove Grant
                for grant in Grant.objects.filter(user=user):
                    self.stdout.write('\tGrant ID {}.'.format(grant.id))

                    if options['delete']:
                        grant.delete()

                try:
                    self.stdout.write('\tUser {}.'.format(user.name))
                except:
                    self.stdout.write('\tUser ID {}.'.format(user.id))

                if options['delete']:
                    user.delete()

            # Remove categories and CategoryI18n from Account
            for category in Category.objects.filter(account=account):
                for categoryi18n in CategoryI18n.objects.filter(category=category):

                    try:
                        self.stdout.write('\tCategoryI18N {}.'.format(categoryi18n.name))
                    except:
                        self.stdout.write('\tCategoryI18N ID {}.'.format(categoryi18n.id))

                    if options['delete']:
                        categoryi18n.delete()

                self.stdout.write('\tCategory ID {}.'.format(category.id))

                if options['delete']:
                    category.delete()

            # Remove Thresholds
            for threshold in Threshold.objects.filter(account=account):
                try:
                    self.stdout.write('\tThresholds {}.'.format(threshold.name))
                except:
                    self.stdout.write('\tThresholds ID {}.'.format(threshold.id))

                if options['delete']:
                    threshold.delete()


            # Remove Preferences
            for preference in Preference.objects.filter(account=account):
                try:
                    self.stdout.write('\tPreference {}.'.format(preference.key))
                except:
                    self.stdout.write('\tPreference ID {}.'.format(preference.id))

                if options['delete']:
                    preference.delete()


            # Remove Application
            for application in Application.objects.filter(account=account):
                try:
                    self.stdout.write('\tApplication {}.'.format(application.key))
                except:
                    self.stdout.write('\tApplication ID {}.'.format(application.id))

                if options['delete']:
                    application.delete()


            # Remove account
            if options['delete']:
                try:
                    account.delete()
                except ProtectedError:
                    retry.append(account)

        # Remove protected accounts
        for account in retry:
            try:
                self.stdout.write('Retried account {}.'.format(account.name))
            except:
                self.stdout.write('Retried account ID {}.'.format(account.id))
            account.delete()
