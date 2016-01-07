import logging
import json

from django.db import models
from django.utils.translation import ugettext_lazy
from django.db import IntegrityError
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from django.contrib.auth.models import AnonymousUser
from django.db.models import Q


from core.utils import slugify
from core import choices
from core import managers
from core.cache import Cache
from core.lib.datastore import *


logger = logging.getLogger(__name__)


def add_facets_to_doc(resource, account, doc):

    faceted = account.faceted_fields()
    if resource.meta_text:
        try:
            meta_text = json.loads(resource.meta_text)
        except:
            field_values = []    
            logger.error("BAD FIELDS_VALUES: %s -- %s -- %s" % (repr(resource), str(doc), resource.meta_text))
    
        field_values = meta_text['field_values']
        for fv in field_values:
            # Take only the first key
            key = fv.keys()[0]
            if key in faceted:
                doc['categories'][key] = fv[key]

    return doc


class GuidModel(models.Model):
    _title = ''

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        try:
            value = kwargs.pop('title')
            self.__setattr__('title', value)
        except KeyError:
            pass

        super(GuidModel, self).__init__(*args, **kwargs)

    def save(self, force_insert=False, force_update=False, using=None):
        if not self.id:
            force_random = False
            while not self.id:
                try:
                    self._set_guid(force_random)
                    super(GuidModel, self).save(force_insert, force_update, using)
                except IntegrityError as e:
                    if 'guid' in e.args[1]:
                        force_random = True
                    else:
                        raise
        else:
            super(GuidModel, self).save(force_insert, force_update, using)

    def __setattr__(self, name, value):
        if name == 'title':
            self._title = value
        else:
            super(GuidModel, self).__setattr__(name, value)

    def _set_guid(self, force_random=False):
        #if self._title:
        title_word_list = [ word for word in slugify(self._title).split('-') if word ][:5]

        # killing duplicates?
        if not force_random:
            self.guid = '-'.join(word[:5] for word in title_word_list).upper()
        else:
            import random
            if len(title_word_list) >= 5:
                self.guid = '-'.join(word[:5] for word in title_word_list[:-1] + [str(random.randint(10000, 99999))]).upper()
            else:
                self.guid = '-'.join(word[:5] for word in title_word_list + [str(random.randint(10000, 99999))]).upper()
        #else:
        #    raise Exception('Please set the title before saving it, we need it to compute the guid.')


class AccountLevel(models.Model):
    name        = models.CharField(max_length=30)
    code        = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    objects     = managers.AccountLevelManager()

    class Meta:
        db_table = 'ao_account_levels'

    def __unicode__(self):
        return self.name


class Account(models.Model):

    ACTIVE = 1
    CLOSED = 2
    BLOCKED = 3
    TRIAL = 4

    STATUS_CHOICES = (
        (ACTIVE, 'ACTIVE'),
        (CLOSED, 'CLOSED'),
        (BLOCKED, 'BLOCKED'),
        (TRIAL, 'TRIAL')
    )

    name = models.CharField(max_length=80)
    level = models.ForeignKey('AccountLevel')
    status = models.IntegerField(choices=STATUS_CHOICES, verbose_name=ugettext_lazy('MODEL_STATUS_LABEL'), default=TRIAL)
    meta_data = models.TextField(blank=True, verbose_name=ugettext_lazy('MODEL_METADATA_LABEL'))
    created_at = models.DateTimeField(editable=False, auto_now_add=True, verbose_name=ugettext_lazy('MODEL_CREATED_AT_LABEL'))
    expires_at = models.DateTimeField(verbose_name=ugettext_lazy('MODEL_EXPIRES_AT_LABEL'))
    parent = models.ManyToManyField('Account', null=True, blank=True)

    class Meta:
        db_table = 'ao_accounts'

    def __unicode__(self):
        return self.name

    def get_preference(self, key):
        """ use the preferences class with cache """
        from core.daos.preferences import Preferences
        p = Preferences(account_id=self.id)
        return p[key]
        
    def set_preference(self, key, value):
        """ use the preferences class with cache """
        from core.daos.preferences import Preferences
        p = Preferences(account_id=self.id)
        p[key]=value
        return p[key]

    def get_preferences(self):
        from core.daos.preferences import Preferences
        return Preferences(self.id)

    def faceted_fields(self):
        # Add Metadata if exist
        try:
            fields = json.loads(self.meta_data)['fields']
        except:
            return []
        # The cust- prefix is because key are saved like that
        return ["cust-" + field['name'] for field in fields if field.has_key('faceted') and field.has_key('name') and field.has_key('label')]

    def get_total_datasets(self):
        c = Cache(db=0)
        users = User.objects.filter(account=self)
        total_datasets = c.get('account_total_datasets_' + str(self.id))
        if not total_datasets:
            total_datasets =  Dataset.objects.filter(user__in=users).count()
            if settings.DEBUG: logger.info('get_total_datasets from database %d' % total_datasets)
            if total_datasets > 0:
                c.set('account_total_datasets_' + str(self.id), total_datasets, settings.REDIS_STATS_TTL)
        else:
            if settings.DEBUG: logger.info('get_total_datasets from cache %s' % total_datasets)
            
        return total_datasets

    def get_total_datastreams(self):
        c = Cache(db=0)
        users = User.objects.filter(account=self)
        total_datastreams = c.get('account_total_datastreams_' + str(self.id))
        if not total_datastreams:
            total_datastreams = DataStream.objects.filter(user__in=users).count()
            if total_datastreams > 0:
                c.set('account_total_datastreams_' + str(self.id), total_datastreams, settings.REDIS_STATS_TTL)
        return total_datastreams

    def get_total_visualizations(self):
        c = Cache(db=0)
        users = User.objects.filter(account=self)
        total_visualizations = c.get('account_total_visualizations_' + str(self.id))
        if not total_visualizations:
            total_visualizations =  Visualization.objects.filter(user__in=users).count()
            if total_visualizations > 0:
                c.set('account_total_visualization_' + str(self.id), total_visualizations, settings.REDIS_STATS_TTL)
        return total_visualizations

    @staticmethod
    def get_by_domain(domain, status=ACTIVE):
        """Devuelve el account dependiendo del dominio
            :param: domain: dominio asociado a la preferencia
            :param: status: por default, cuentas activas, en caso de querer las TIRAL, pasarle Account.TRIAL
            :return: instancia Account """

        try:
            return Account.objects.get(
                Q(preference__key='account.api.domain', preference__value=domain) | 
                Q(preference__key='account.domain', preference__value=domain),
                status = status)
        except Account.DoesNotExist:
            # generalmente usamos algo.dev:port
            if settings.DEBUG: logger.info('NO domain (%s)' % domain)

            try:
                if domain.find('.site.demo.junar.com') > -1:
                    account_id = int(domain.split('.')[0])
                    return Account.objects.get(pk=account_id)
                    
                elif domain.split(":")[0][-4:] == ".dev":
                    # obtenemos la primer parte, que en las demos/ambiente de dev
                    # es el ID del Account
                    dom = domain.split(".")[0]
                    if settings.DEBUG: logger.info('API Test domain (%s)' % dom)
    
                    if dom in ("microsites", "api"):
                        return Account.objects.get(pk=1) 
                    else:
                        return Account.objects.get(pk=int(dom)) 
            # en caso de que no le haya pegado a nada, que tire un
            # Account.DoesNotExist
            except:
                pass

        raise Account.DoesNotExist


class AccountAnonymousUser(AnonymousUser):

    def __init__(self, account):
        super(AccountAnonymousUser, self).__init__()
        self.account = account

    def is_authenticated(self):
        return True


class User(models.Model):
    name = models.CharField(max_length=30, verbose_name=ugettext_lazy( 'MODEL_NAME_LABEL' ))
    nick = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=75, unique=True)
    password = models.CharField(max_length=155, verbose_name=ugettext_lazy( 'MODEL-PASSWORD-TEXT' ))
    country = models.CharField(max_length=3, choices=choices.COUNTRY_CHOICES, blank=True, default='US', verbose_name=ugettext_lazy( 'MODEL-COUNTRY-TEXT' ))
    ocupation = models.CharField(max_length=2, choices=choices.OCUPATION_CHOICES, blank=True, verbose_name=ugettext_lazy( 'MODEL-OCUPATION-TEXT' ))
    language = models.CharField(max_length=2, choices=choices.LANGUAGE_CHOICES, verbose_name=ugettext_lazy( 'MODEL-LANGUAGE-TEXT' ))
    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    last_visit = models.DateTimeField(null=True)
    roles = models.ManyToManyField('Role', verbose_name=ugettext_lazy('MODEL-ROLES-TEXT'), db_table='ao_user_role_roles')
    grants = models.ManyToManyField('Privilege', through='Grant', verbose_name=ugettext_lazy('MODEL-USER-GRANTS-TEXT'))
    account = models.ForeignKey('Account', null=True, on_delete=models.PROTECT)

    class Meta:
        db_table = 'ao_users'

    def __unicode__(self):
        return self.nick

    def is_admin(self):
        return True if Role.objects.get(code=AccountRoles.ADMIN) in self.roles.all() else False

    def is_publisher(self):
        return True if Role.objects.get(code=AccountRoles.PUBLISHER) in self.roles.all() else False

    def is_editor(self):
        return True if Role.objects.get(code=AccountRoles.EDITOR) in self.roles.all() else False

    def is_authenticated(self):
        return True

    def get_total_datasets(self):
        c = Cache(db=0)
        total_datasets = c.get('my_total_datasets_' + str(self.id))
        if not total_datasets:
            total_datasets =  Dataset.objects.filter(user=self.id).count()
            if total_datasets > 0:
                c.set('my_total_datasets_' + str(self.id), total_datasets, settings.REDIS_STATS_TTL)
        return total_datasets

    def get_total_datastreams(self):
        c = Cache(db=0)
        total_datastreams = c.get('my_total_datastreams_' + str(self.id))
        if not total_datastreams:
            total_datastreams = DataStream.objects.filter(user=self.id).count()
            if total_datastreams > 0:
                c.set('my_total_datastreams_' + str(self.id), total_datastreams, settings.REDIS_STATS_TTL)
        return total_datastreams

    def get_total_visualizations(self):
        c = Cache(db=0)
        total_visualizations = c.get('my_total_visualizations_' + str(self.id))
        if not total_visualizations:
            total_visualizations = Visualization.objects.filter(user=self.id).count()
            if total_visualizations > 0:
                c.set('my_total_visualizations_' + str(self.id), total_visualizations, settings.REDIS_STATS_TTL)
        return total_visualizations


class DataStream(GuidModel):
    user = models.ForeignKey('User', verbose_name=ugettext_lazy('MODEL_USER_LABEL'), on_delete=models.PROTECT)
    guid = models.CharField(max_length=29, unique=True)
    last_revision = models.ForeignKey('DataStreamRevision', null=True, related_name='last_revision',
                                      on_delete=models.SET_NULL)
    last_published_revision = models.ForeignKey('DataStreamRevision', null=True, related_name='last_published_revision',
                                                on_delete=models.SET_NULL)
    objects = managers.DataStreamManager()

    class Meta:
        db_table = 'ao_datastreams'

    def __unicode__(self):
        return self.guid

    # Returns the current revision
    @property
    def current(self):
        return self.datastreamrevision_set.all()[0]

    @property
    def last_published_revision_date(self):
        return self.last_published_revision.modified_at if self.last_published_revision else None


class RevisionModel(models.Model):
    def get_meta_data_dict(self, metadata):
        answer = {}
        if metadata:
            try:
                meta = json.loads(metadata)
                meta = meta['field_values'] if 'field_values' in meta else []
                for item in meta:
                    answer.update(item)
            except ValueError:
                pass
        return answer

    class Meta:
        abstract = True


class DataStreamRevision(RevisionModel):
    STATUS_CHOICES = choices.STATUS_CHOICES

    datastream = models.ForeignKey('DataStream', verbose_name=ugettext_lazy('MODEL_DATASTREAM_LABEL'))
    dataset = models.ForeignKey('Dataset', verbose_name=ugettext_lazy('MODEL_DATASET_LABEL'))
    user = models.ForeignKey('User', verbose_name=ugettext_lazy('MODEL_USER_LABEL'), on_delete=models.PROTECT)
    category = models.ForeignKey('Category', verbose_name=ugettext_lazy('MODEL_CATEGORY_LABEL'))
    data_source = models.TextField(verbose_name=ugettext_lazy('MODEL_DATASTREAM_REVISION_DATA_SOURCE_LABEL'))
    select_statement = models.TextField(verbose_name=ugettext_lazy('MODEL_DATASTREAM_REVISION_SELECT_STATEMENT_LABEL'))
    status = models.IntegerField(choices=STATUS_CHOICES, verbose_name=ugettext_lazy('MODEL_STATUS_LABEL'))
    meta_text = models.TextField( blank=True, verbose_name=ugettext_lazy('MODEL_META_TEXT_LABEL'))
    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    modified_at = models.DateTimeField(editable=False, auto_now=True)
    rdf_template = models.TextField(blank=True,
                                    verbose_name=ugettext_lazy('MODEL_DATASTREAM_REVISION_RDF_TEMPLATE_LABEL'))
    objects = managers.DataStreamRevisionManager()

    class Meta:
        db_table = 'ao_datastream_revisions'
        ordering = ['-id']
        get_latest_by = 'created_at'

    def __unicode__(self):
        return unicode(self.id)

    def is_pending_review(self):
        return True if self.status == choices.StatusChoices.PENDING_REVIEW else False

    @staticmethod
    def related_to_dataset(dataset):
        """
        traigo todas las revisiones de DataStream asociados a un dataset en particular y su DataStream
        """
        return DataStreamRevision.objects.filter(dataset=dataset)


    def update(self, changed_fields, **fields):
        if changed_fields:
            if 'category' in changed_fields:
                self.category = Category.objects.get(id=fields['category'])
            if 'status' in changed_fields:
                self.status = fields['status']
            if 'data_source' in changed_fields:
                self.data_source = fields['data_source']
            if 'select_statement' in changed_fields:
                self.select_statement = fields['select_statement']
            if 'meta_text' in changed_fields:
                self.meta_text = fields['meta_text']
            if 'rdf_template' in changed_fields:
                self.rdf_template = fields['rdf_template']

        self.save()

    def add_tags(self, tags):
        self.tagdatastream_set.clear()
        for tag_field in tags:
            tag, is_new = Tag.objects.get_or_create(name=tag_field.get('name', ''))

            tag_datastream, is_new = TagDatastream.objects.get_or_create(tag=tag, datastreamrevision=self)
            self.tagdatastream_set.add(tag_datastream)
        self.save()

    def add_sources(self, sources):
        self.sourcedatastream_set.clear()
        
        for source_field in sources:
            source_with_name = Source.objects.filter(name=source_field.get('name', ''))
            if source_with_name.count():
                source = source_with_name[0]
            else:
                source = Source.objects.create(
                    name=source_field.get('name', ''),
                    url=source_field.get('url', '')
                )

            source_datastream, is_new = SourceDatastream.objects.get_or_create(source=source, datastreamrevision=self)
            self.sourcedatastream_set.add(source_datastream)
        self.save()

    def get_sources(self):
        """ return sources """
        return self.sourcedatastream_set.all().values('source__name', 'source__url', 'source__id')

    def add_parameters(self, parameters):
        self.datastreamparameter_set.clear()
        
        for parameter in parameters:
            self.datastreamparameter_set.add(DataStreamParameter.objects.create(name=parameter['name']
                                                                                , position=parameter['position']
                                                                                , default=parameter['default']
                                                                                , description=parameter['description']))

        self.save()

    def get_guid(self):
        return self.datastream.guid

    def get_latest_revision(self):
        return self.datastream.visualizationrevision_set.latest()

    def clone(self, status=choices.StatusChoices.DRAFT):
        datastream_revision = DataStreamRevision(
            datastream=self.datastream,
            dataset=self.dataset,
            user=self.user,
            category=self.category,
            data_source=self.data_source,
            select_statement=self.select_statement,
            meta_text=self.meta_text,
            rdf_template=self.rdf_template,
            status=status
        )

        datastream_revision.save()

        for tag in self.tagdatastream_set.all():
            datastream_revision.tagdatastream_set.add(tag)

        for source in self.sourcedatastream_set.all():
            datastream_revision.sourcedatastream_set.add(source)

        for parameter in self.datastreamparameter_set.all():
            datastream_revision.datastreamparameter_set.create(
                datastream_revision=datastream_revision,
                name=parameter.name,
                default=parameter.default,
                position=parameter.position,
                impl_details=parameter.impl_details,
                description=parameter.description
            )

        for datastreami8n in self.datastreami18n_set.all():
            datastream_revision.datastreami18n_set.create(
                language=datastreami8n.language,
                datastream_revision=datastream_revision,
                title=datastreami8n.title,
                description=datastreami8n.description,
                notes=datastreami8n.notes
            )

        datastream_revision.save()

        return datastream_revision


class DatastreamI18n(models.Model):
    language = models.CharField(
        max_length=2,
        choices=choices.LANGUAGE_CHOICES,
        verbose_name=ugettext_lazy('MODEL_LANGUAGE_LABEL')
    )
    datastream_revision = models.ForeignKey(
        'DataStreamRevision',
        verbose_name=ugettext_lazy('MODEL_DATASTREAM_REVISION_LABEL')
    )
    title = models.CharField(max_length=80, verbose_name=ugettext_lazy('MODEL_TITLE_LABEL'))
    description = models.CharField(max_length=140, blank=True, verbose_name=ugettext_lazy('MODEL_DESCRIPTION_LABEL'))
    notes = models.TextField(blank=True, verbose_name=ugettext_lazy('MODEL_NOTE_LABEL'))
    created_at = models.DateTimeField(editable=False, auto_now_add=True)

    class Meta:
        db_table = 'ao_datastream_i18n'

    def __unicode__(self):
        return self.title

    def update(self, changed_fields, **fields):
        if changed_fields:
            if 'title' in changed_fields:
                self.title = fields['title']
            if 'description' in changed_fields:
                self.description = fields['description']
            if 'notes' in changed_fields:
                self.notes = fields['notes']
        self.save()


class DataStreamParameter(models.Model):
    datastream_revision = models.ForeignKey(
        'DataStreamRevision',
        verbose_name=ugettext_lazy('MODEL_DATASTREAM_REVISION_LABEL'),
        null=True
    )
    name = models.CharField(max_length=30, verbose_name=ugettext_lazy('MODEL_NAME_LABEL'))
    default = models.CharField(max_length=100, verbose_name=ugettext_lazy('MODEL_DEFAULT_LABEL'))
    position = models.PositiveSmallIntegerField()
    impl_details = models.TextField(blank=True, verbose_name=ugettext_lazy('MODEL_IMPLEMENTATION_DETAILS_LABEL'))
    description = models.CharField(max_length=100, blank=True, verbose_name=ugettext_lazy('MODEL_DESCRIPTION_LABEL'))

    class Meta:
        db_table = 'ao_datastream_parameters'
        ordering = ['position']
        unique_together = (("datastream_revision", "name"))

    def __unicode__(self):
        return  unicode(self.id)


class Dataset(GuidModel):
    user = models.ForeignKey('User', verbose_name=ugettext_lazy('MODEL_USER_LABEL'), on_delete=models.PROTECT)
    type = models.IntegerField(choices=choices.COLLECT_TYPE_CHOICES)
    is_dead = models.SmallIntegerField(blank=False, verbose_name=ugettext_lazy('MODEL_IS_DEAD_LABEL'), default=0)
    guid = models.CharField(max_length=29, unique=True)
    last_revision = models.ForeignKey('DatasetRevision', null=True, related_name='last_revision', on_delete=models.SET_NULL)
    last_published_revision = models.ForeignKey('DatasetRevision', null=True, related_name='last_published_revision',
                                                blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    objects = managers.DataSetManager()

    class Meta:
        db_table = 'ao_datasets'

    def __unicode__(self):
        return unicode(self.id)

    @property
    def current(self):
        return self.datasetrevision_set.all()[0]

    @property
    def last_published_revision_date(self):
        return self.last_published_revision.modified_at if self.last_published_revision else None


class DatasetRevision(RevisionModel):
    STATUS_CHOICES = choices.STATUS_CHOICES

    dataset = models.ForeignKey('Dataset', verbose_name=ugettext_lazy('MODEL_DATASET_LABEL'))
    user = models.ForeignKey('User', verbose_name=ugettext_lazy('MODEL_USER_LABEL'), on_delete=models.PROTECT)
    category = models.ForeignKey('Category', verbose_name=ugettext_lazy('MODEL_CATEGORY_LABEL'))
    end_point = models.CharField(max_length=2048, verbose_name=ugettext_lazy('MODEL_END_POINT_LABEL'))
    filename = models.CharField(max_length=2048, verbose_name=ugettext_lazy('MODEL_FILENAME_LABEL'))
    impl_details = models.TextField(blank=True, null=True, verbose_name=ugettext_lazy('MODEL_DATASET_REVISION_IMPL_DETAILS_LABEL'))
    impl_type = models.IntegerField(choices=choices.SOURCE_IMPLEMENTATION_CHOICES,
                                    verbose_name=ugettext_lazy('MODEL_IMPLEMENTATION_TYPE_LABEL'))
    status = models.IntegerField(choices=STATUS_CHOICES, verbose_name=ugettext_lazy('MODEL_STATUS_LABEL'))
    # Just for resources compatibility
    meta_text = models.TextField( blank=True, verbose_name=ugettext_lazy('MODEL_META_TEXT_LABEL'))
    size = models.IntegerField(default=0, verbose_name=ugettext_lazy('MODEL_SIZE_LABEL'))
    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    modified_at = models.DateTimeField(editable=False, auto_now=True)
    license_url = models.TextField(blank=True, verbose_name=ugettext_lazy('MODEL_LICENSE_LABEL'))
    spatial = models.CharField(max_length=80, blank=True, verbose_name=ugettext_lazy('MODEL_SPATIAL_LABEL'))
    frequency = models.TextField(blank=True, verbose_name=ugettext_lazy('MODEL_FREQUENCY_LABEL'))
    mbox = models.TextField(blank=True, verbose_name=ugettext_lazy('MODEL_MBOX_LABEL'))

    class Meta:
        db_table = 'ao_dataset_revisions'
        ordering = ['-id']
        get_latest_by = 'created_at'

    def __unicode__(self):
        return  unicode(self.id)

    def get_endpoint_full_url(self):
        if settings.USE_DATASTORE == 'sftp':
            # We MUST rewrite all file storage logic very SOON
            return '{}/{}/{}'.format(
                settings.SFTP_BASE_URL,
                settings.AWS_BUCKET_NAME,
                self.end_point.replace('file://', '')
            )

        if settings.USE_DATASTORE == 's3':
            return active_datastore.generate_url(settings.AWS_BUCKET_NAME, key=self.end_point.replace('file://', ''))

        return self.end_point

    def is_pending_review(self):
        return True if self.status == choices.StatusChoices.PENDING_REVIEW else False

    def update(self, changed_fields, **fields):
        if 'category' in changed_fields:
            self.category = Category.objects.get(id=fields['category'])
        if 'file_name' in changed_fields:
            self.filename = fields['file_name']
        if 'end_point' in changed_fields:
            self.end_point = fields['end_point']
        if 'impl_type' in changed_fields:
            self.impl_type = fields['impl_type']
        if 'impl_details' in changed_fields:
            self.impl_details = fields['impl_details']
        if 'file_size' in changed_fields:
            self.size = fields['file_size']
        if 'license_url' in changed_fields:
            self.license_url = fields['license_url']
        if 'spatial' in changed_fields:
            self.spatial = fields['spatial']
        if 'frequency' in changed_fields:
            self.frequency = fields['frequency']
        if 'mbox' in changed_fields:
            self.mbox = fields['mbox']
        if 'status' in changed_fields:
            self.status = fields['status']

        self.save()

    def add_tags(self, tags):
        self.tagdataset_set.clear()

        for tag_data in tags:
            if tag_data:
                tag, is_new = Tag.objects.get_or_create(name=tag_data['name'])
                tag_data_set, is_new = TagDataset.objects.get_or_create(tag=tag, datasetrevision=self)
                self.tagdataset_set.add(tag_data_set)
        self.save()

    def add_sources(self, sources):
        self.sourcedataset_set.clear()

        for source_data in sources:
            if source_data:
                if not source_data['url']:
                    source = Source.objects.get(name= source_data['name'])
                else:
                    source = Source.objects.create(name= source_data['name'], url=source_data['url'])

                source_dataset, is_new = SourceDataset.objects.get_or_create(source=source, datasetrevision=self)
                self.sourcedataset_set.add(source_dataset)
        self.save()

    def get_tags(self):
        return self.tagdataset_set.all().values('tag__name', 'tag__status', 'tag__id')

    def get_sources(self):
        """ return sources """
        return self.sourcedataset_set.all().values('source__name', 'source__url', 'source__id')

    def clone(self, status=choices.StatusChoices.DRAFT):

        dataset_revision = DatasetRevision(dataset=self.dataset, user=self.user)
        dataset_revision.category = self.category
        dataset_revision.end_point = self.end_point
        dataset_revision.filename = self.filename
        dataset_revision.impl_details = self.impl_details
        dataset_revision.impl_type = self.impl_type
        dataset_revision.status = status
        dataset_revision.license_url = self.license_url
        dataset_revision.spatial= self.spatial
        dataset_revision.frequency=self.frequency
        dataset_revision.mbox=self.mbox
        dataset_revision.save()

        for tag in self.tagdataset_set.all():
            dataset_revision.tagdataset_set.add(tag)

        for source in self.sourcedataset_set.all():
            dataset_revision.sourcedataset_set.add(source)

        for dataseti18n in self.dataseti18n_set.all():
            dataset_revision.dataseti18n_set.create(
                language = dataseti18n.language,
                dataset_revision = dataset_revision,
                title = dataseti18n.title,
                description = dataseti18n.description,
                notes = dataseti18n.notes
            )

        dataset_revision.save()

        return dataset_revision


class DatasetI18n(models.Model):
    language = models.CharField(max_length=2, choices=choices.LANGUAGE_CHOICES, verbose_name=ugettext_lazy('MODEL_LANGUAGE_LABEL'))
    dataset_revision = models.ForeignKey('DatasetRevision', verbose_name=ugettext_lazy('MODEL_DATASET_REVISION_LABEL'))
    title = models.CharField(max_length=80, verbose_name=ugettext_lazy('MODEL_TITLE_LABEL'))
    description = models.CharField(max_length=140, blank=True, verbose_name=ugettext_lazy('MODEL_DESCRIPTION_LABEL'))
    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    notes = models.TextField(blank=True, verbose_name=ugettext_lazy('MODEL_NOTE_LABEL'))

    class Meta:
        db_table = 'ao_dataset_i18n'

    def __unicode__(self):
        return self.title

    def update(self, changed_fields, **fields):
        if 'title' in changed_fields: self.title = fields['title']
        if 'description' in changed_fields: self.description = fields['description']
        if 'notes' in changed_fields: self.notes = fields['notes']
        self.save()


class Visualization(GuidModel):
    datastream = models.ForeignKey('DataStream')
    guid = models.CharField(max_length=29, unique=True)
    user = models.ForeignKey('User', verbose_name=ugettext_lazy('MODEL_USER_LABEL'), on_delete=models.PROTECT)
    last_revision = models.ForeignKey('VisualizationRevision', null=True, related_name='last_revision',
                                      on_delete=models.SET_NULL)
    last_published_revision = models.ForeignKey('VisualizationRevision', null=True,
                                                related_name='last_published_revision', on_delete=models.SET_NULL)
    objects = managers.VisualizationManager()

    class Meta:
        db_table = 'ao_visualizations'

    def __unicode__(self):
        return  unicode(self.id)

    # Returns the current revision
    @property
    def current(self):
        return self.visualizationrevision_set.all()[0]

    @property
    def last_published_revision_date(self):
        return self.last_published_revision.modified_at if self.last_published_revision else None


class VisualizationRevision(RevisionModel):
    visualization = models.ForeignKey('Visualization', verbose_name=ugettext_lazy('MODEL_VISUALIZATION_LABEL'))

    datastream = models.ForeignKey('DataStream',
                                            verbose_name=ugettext_lazy('MODEL_DATASTREAM_LABEL'))

    user = models.ForeignKey('User', verbose_name=ugettext_lazy('MODEL_USER_LABEL'), on_delete=models.PROTECT)
    lib = models.CharField(max_length=10, choices=choices.VISUALIZATION_LIBS)
    impl_details = models.TextField(blank=True)
    meta_text = models.TextField( blank=True, verbose_name=ugettext_lazy('MODEL_META_TEXT_LABEL'))
    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    modified_at = models.DateTimeField(editable=False, auto_now=True)
    status = models.IntegerField(choices=choices.STATUS_CHOICES, verbose_name=ugettext_lazy('MODEL_STATUS_LABEL'))
    parameters = models.CharField(max_length=2048, verbose_name=ugettext_lazy( 'MODEL-URL-TEXT' ), blank=True)

    class Meta:
        db_table = 'ao_visualizations_revisions'
        ordering = ['-id']
        get_latest_by = 'created_at'

    def __unicode__(self):
        return unicode(self.id)

    def get_guid(self):
        return self.visualization.guid

    def get_latest_revision(self):
        return self.visualization.visualizationrevision_set.latest()

    def clone(self, status=choices.StatusChoices.DRAFT):
        visualization_revision = VisualizationRevision(
            visualization=self.visualization,
            datastream_revision=self.datastream_revision,
            user=self.user,
            lib=self.lib,
            impl_details=self.impl_details,
            meta_text=self.meta_text,
            status=status,
            parameters=self.parameters
        )

        visualization_revision.save()

        for visualizationi18n in self.visualizationi18n_set.all():
            visualization_revision.visualizationi18n_set.create(
                language = visualizationi18n.language,
                visualization_revision = visualization_revision,
                title = visualizationi18n.title,
                description = visualizationi18n.description,
                notes = visualizationi18n.notes
            )

        visualization_revision.save()
        return visualization_revision


class VisualizationI18n(models.Model):
    language = models.CharField(max_length=2, choices=choices.LANGUAGE_CHOICES, verbose_name=ugettext_lazy('MODEL_LANGUAGE_LABEL'))
    visualization_revision = models.ForeignKey('VisualizationRevision', verbose_name=ugettext_lazy('MODEL_VISUALIZATION_REVISION_LABEL'))
    title = models.CharField(max_length=80, verbose_name=ugettext_lazy('MODEL_TITLE_LABEL'))
    description = models.CharField(max_length=140, blank=True, verbose_name=ugettext_lazy('MODEL_DESCRIPTION_LABEL'))
    notes = models.TextField(blank=True, verbose_name=ugettext_lazy('MODEL_NOTE_LABEL'))
    created_at = models.DateTimeField(editable=False, auto_now_add=True)

    class Meta:
        db_table = 'ao_visualizations_i18n'

    def __unicode__(self):
        return self.title


class Category(models.Model):
    account = models.ForeignKey('Account', null=True)
    objects = managers.CategoryManager()

    class Meta:
        db_table = 'ao_categories'

    def __unicode__(self):
        return unicode(self.id)


class CategoryI18n(models.Model):
    language = models.CharField(max_length=2, choices=choices.LANGUAGE_CHOICES, verbose_name=ugettext_lazy('MODEL_LANGUAGE_LABEL'))
    category = models.ForeignKey('Category', verbose_name=ugettext_lazy('MODEL_CATEGORY_LABEL'))
    name = models.CharField(max_length=30, verbose_name=ugettext_lazy('MODEL_TITLE_LABEL'))
    slug = models.SlugField(max_length=30, verbose_name=ugettext_lazy('MODEL_SLUG_LABEL'))
    description = models.CharField(max_length=140, blank=True, verbose_name=ugettext_lazy('MODEL_DESCRIPTION_LABEL'))
    created_at = models.DateTimeField(editable=False, auto_now_add=True)

    class Meta:
        db_table = 'ao_categories_i18n'

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(CategoryI18n, self).save(*args, **kwargs)


class Tag(models.Model):
    name = models.CharField(unique=True, max_length=40, verbose_name=ugettext_lazy('MODEL_TAG_TEXT'))
    status = models.SmallIntegerField(default=0, verbose_name=ugettext_lazy('MODEL_STATUS_LABEL'))

    class Meta:
        db_table = 'ao_tags'

    def __unicode__(self):
        return unicode(self.id)


class TagDataset(models.Model):
    tag = models.ForeignKey('Tag', null=True)
    datasetrevision = models.ForeignKey('DatasetRevision', null=True, verbose_name=ugettext_lazy('MODEL_DATASET_REVISION_LABEL'))

    class Meta:
        db_table = 'ao_tags_dataset'

    def __unicode__(self):
        return unicode(self.id)


class TagDatastream(models.Model):
    tag = models.ForeignKey('Tag', null=True)
    datastreamrevision = models.ForeignKey(
        'DataStreamRevision',
        null=True,
        verbose_name=ugettext_lazy('MODEL_DATASTREAM_REVISION_LABEL')
    )

    class Meta:
        db_table = 'ao_tags_datastream'

    def __unicode__(self):
        return unicode(self.id)


class TagVisualization(models.Model):
    tag = models.ForeignKey('Tag', null=True)
    visualizationrevision = models.ForeignKey('VisualizationRevision', null=True, verbose_name=ugettext_lazy('MODEL_VISUALIZATION_REVISION_LABEL'))

    class Meta:
        db_table = 'ao_tags_visualization'

    def __unicode__(self):
        return unicode(self.id)


class Role(models.Model):
    name            = models.CharField(max_length=63, verbose_name=ugettext_lazy('MODEL_NAME_LABEL'))
    code            = models.CharField(max_length=63, verbose_name=ugettext_lazy('MODEL_CODE_LABEL'))
    description     = models.CharField(max_length=100, blank=True, verbose_name=ugettext_lazy('MODEL_DESCRIPTION_LABEL'))
    created_at      = models.DateTimeField(editable=False, auto_now_add=True)
    grants          = models.ManyToManyField('Privilege', through='Grant', verbose_name=ugettext_lazy('MODEL_ROLE_GRANTS_LABEL'))

    class Meta:
        db_table = 'ao_user_roles'

    def __unicode__(self):
        return '%d %s' % (self.id, self.name)


class Privilege(models.Model):
    name            = models.CharField(max_length=63, verbose_name=ugettext_lazy('MODEL_NAME_LABEL'))
    code            = models.CharField(max_length=63, verbose_name=ugettext_lazy('MODEL_CODE_LABEL'))
    description     = models.CharField(max_length=100, blank=True, verbose_name=ugettext_lazy('MODEL_DESCRIPTION_LABEL'))
    created_at      = models.DateTimeField(editable=False, auto_now_add=True)

    class Meta:
        db_table = 'ao_user_privileges'

    def __unicode__(self):
        return '%d %s' % (self.id, self.name)


class Grant(models.Model):
    user            = models.ForeignKey('User', verbose_name=ugettext_lazy('MODEL_USER_LABEL'), null=True, on_delete=models.PROTECT)
    role            = models.ForeignKey('Role', verbose_name=ugettext_lazy('MODEL_ROLE_LABEL'), null=True)
    guest           = models.ForeignKey('Guest', verbose_name=ugettext_lazy('MODEL_GUEST_LABEL'), null=True)
    privilege       = models.ForeignKey('Privilege', verbose_name=ugettext_lazy('MODEL_PRIVILEGE_LABEL'), null=True)
    created_at      = models.DateTimeField(editable=False, auto_now_add=True)

    class Meta:
        db_table = 'ao_user_grants'

    def __unicode__(self):
        return unicode(self.id)

# :TODO: Sin Migrar aun
class ObjectGrant(models.Model):
    grant           = models.ForeignKey('Grant', verbose_name=ugettext_lazy('MODEL_GRANT_LABEL'))
    datastream      = models.ForeignKey('DataStream', null=True, verbose_name=ugettext_lazy('MODEL_DATASTREAM_LABEL'))
    visualization   = models.ForeignKey('Visualization', null=True, verbose_name=ugettext_lazy('MODEL_VISUALIZATION_LABEL'))
    type            = models.CharField(max_length=63, verbose_name=ugettext_lazy('MODEL_TYPE_LABEL'))
    auth_key        = models.CharField( max_length=100, verbose_name=ugettext_lazy('MODEL_AUTH_KEY_LABEL'))
    created_at      = models.DateTimeField(editable=False, auto_now_add=True)
    objects         = managers.ObjectGrantManager()

    class Meta:
        db_table = 'ao_user_object_grants'

    def __unicode__(self):
        return unicode(self.id)


class Guest( models.Model ):
    email       = models.CharField( max_length=100, verbose_name=ugettext_lazy('MODEL_EMAIL_LABEL'))
    grants      = models.ManyToManyField('Privilege', through='Grant', verbose_name=ugettext_lazy('MODEL_GUEST_GRANT_LABEL'))

    class Meta:
        db_table = 'ao_user_guests'

    def __unicode__( self ):
        return unicode(self.id)


class Threshold(models.Model):
    account_level = models.ForeignKey('AccountLevel', null=True, blank=True)
    account       = models.ForeignKey('Account', null=True, blank=True)
    name          = models.CharField(max_length=30, choices=choices.THRESHOLD_NAME_CHOICES)
    description   = models.TextField(blank=True)
    limit         = models.IntegerField(default=0)
    objects       = managers.ThresholdManager()

    class Meta:
        db_table = 'ao_account_thresholds'

    def __unicode__(self):
        return '%s - %s' % (self.account_level, self.name)


class Preference(models.Model):
    account = models.ForeignKey('Account')
    key = models.CharField(max_length=50, choices=choices.ACCOUNT_PREFERENCES_AVAILABLE_KEYS)
    value = models.TextField(blank=True)
    objects = managers.PreferenceManager()

    class Meta:
        db_table = 'ao_account_preferences'

    def __unicode__(self):
        return '%d - %s' % (self.id, self.account)


class Application(models.Model):
    user = models.ForeignKey('User', null=True, blank=True)
    account = models.ForeignKey('Account', null=True, blank=True)
    name = models.CharField(max_length=80, blank=True)
    description = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=40, blank=True)
    locale = models.CharField(max_length=10, blank=True)
    url = models.URLField(max_length=2048, blank=True)
    auth_key = models.CharField(max_length=40)
    public_auth_key = models.CharField(max_length=40)
    domains = models.TextField(blank=True)
    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    expires_at = models.DateTimeField()
    valid = models.SmallIntegerField(default=0)
    type = models.CharField(max_length=2, choices=choices.API_APPLICATION_TYPE_CHOICES)

    class Meta:
        db_table = 'ao_applications'

    def __unicode__(self):
        return self.name

    def human_readable_type(self):
        human_type = {'01': 'Unlimited!'}

        return human_type[self.type]

    def get_name(self):
        return self.name and self.name or 'No name'

    def is_private_auth_key(self, auth_key):
        return self.auth_key == auth_key

    def is_public_auth_key(self, auth_key):
        return self.public_auth_key == auth_key


class Setting(models.Model):
    key = models.CharField(primary_key=True, max_length=40)
    value = models.TextField()
    description = models.CharField(max_length=100, blank=True)

    class Meta:
        db_table = 'ao_settings'

    def __unicode__(self):
        return self.key


class UserPassTickets(models.Model):
    uuid = models.CharField(max_length=38)
    user = models.ForeignKey('User')
    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    type = models.CharField(max_length=38)
    objects = managers.UserPassTicketsManager()

    class Meta:
        db_table = 'ao_user_passtickets'

    def __unicode__(self):
        return unicode(self.id)

# :TODO: Sin Migrar aun
class Source(models.Model):
    name = models.CharField(unique=True, max_length=40, blank=False)
    url = models.CharField(max_length=2048, blank=False)

    class Meta:
        db_table = 'ao_sources'

    def __unicode__(self):
        return unicode(self.id)


class SourceDataset(models.Model):
    source = models.ForeignKey('Source', null=True)
    datasetrevision = models.ForeignKey('DatasetRevision', null=True)

    class Meta:
        db_table = 'ao_sources_dataset_revision'

# :TODO: Sin Migrar aun
class SourceDatastream(models.Model):
    source = models.ForeignKey('Source', null=True)
    datastreamrevision = models.ForeignKey('DataStreamRevision', null=True)

    class Meta:
        db_table = 'ao_sources_datastream_revision'


class VisualizationHits(models.Model):
    visualization = models.ForeignKey('Visualization')
    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    channel_type = models.SmallIntegerField(choices=choices.CHANNEL_TYPES)

    class Meta:
        db_table = 'ao_visualization_hits'

    def __unicode__(self):
        return unicode(self.id)


class DataStreamHits(models.Model):
    datastream = models.ForeignKey('Datastream')
    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    channel_type = models.SmallIntegerField(choices=choices.CHANNEL_TYPES)

    class Meta:
        db_table = 'ao_datastream_hits'

    def __unicode__(self):
        return unicode(self.id)


class DataStreamRank(models.Model):
    datastream = models.ForeignKey('DataStream', verbose_name=ugettext_lazy( 'MODEL-DATASTREAM-TEXT' ))
    position = models.SmallIntegerField(verbose_name=ugettext_lazy( 'MODEL-POSITION-TEXT' ))
    created_at = models.DateTimeField(editable=False, auto_now_add=True)

    class Meta:
        db_table = 'ao_datastream_ranks'

    def __unicode__(self):
        return unicode(self.id)


class DataStreamComment(models.Model):
    datastream = models.ForeignKey('DataStream', verbose_name=ugettext_lazy('MODEL-DATASTREAM-TEXT'))
    user = models.ForeignKey('User', verbose_name=ugettext_lazy('MODEL-USER-TEXT'))
    comment = models.CharField(max_length=500, verbose_name=ugettext_lazy('MODEL-COMMENT-TEXT'))
    created_at = models.DateTimeField(editable=False, auto_now_add=True)

    class Meta:
        db_table = 'ao_datastream_comments'

    def __unicode__(self):
        return unicode(self.id)


class Log(models.Model):
    user = models.ForeignKey('User',  on_delete=models.DO_NOTHING)
    datastream = models.ForeignKey('DataStream', null=True, verbose_name=ugettext_lazy('MODEL_DATASTREAM_LABEL'),
                                   on_delete=models.DO_NOTHING)
    visualization = models.ForeignKey('Visualization', null=True,
                                      verbose_name=ugettext_lazy('MODEL_VISUALIZATION_LABEL'),
                                      on_delete=models.DO_NOTHING)
    content = models.TextField()
    created_at = models.DateTimeField(editable=False, auto_now_add=True)

    class Meta:
        db_table = 'ao_logs'


# Signals

@receiver(pre_delete, sender=DatasetRevision, dispatch_uid="unindex_dataset_revision")
def unindex_dataset_revision(sender, instance, **kwargs):
    # Elimino del indexador todas las revision publicadas cada vez que elimino una revision
    if instance.status == choices.StatusChoices.PUBLISHED:
        from core.daos.datasets import DatasetSearchDAOFactory
        search_dao = DatasetSearchDAOFactory().create(instance)
        search_dao.remove()


@receiver(pre_delete, sender=DataStreamRevision, dispatch_uid="unindex_datastream_revision")
def unindex_datastream_revision(sender, instance, **kwargs):
    # Elimino del indexador todas las revision publicadas cada vez que elimino una revision
    if instance.status == choices.StatusChoices.PUBLISHED:
        from core.daos.datastreams import DatastreamSearchDAOFactory
        search_dao = DatastreamSearchDAOFactory().create(instance)
        search_dao.remove()


@receiver(pre_delete, sender=VisualizationRevision, dispatch_uid="unindex_visualization_revision")
def unindex_visualization_revision(sender, instance, **kwargs):
    # Elimino del indexador todas las revision publicadas cada vez que elimino una revision
    logger.info("VZ ID %s STATUS %s" % (instance.id, instance.status))
    if instance.status == choices.StatusChoices.PUBLISHED:
        from core.daos.visualizations import VisualizationSearchDAOFactory
        search_dao = VisualizationSearchDAOFactory().create(instance)
        search_dao.remove()
