# -*- coding: utf-8 -*-
import operator
import time
import logging
import json

from django.db.models import Q, F, Count
from django.db import IntegrityError
from django.core.serializers.json import DjangoJSONEncoder
from django.db import connection
from django.utils.timezone import now


from datetime import timedelta

from core.primitives import PrimitiveComputer
from core.utils import slugify
from core.cache import Cache
from core.daos.resource import AbstractDataStreamDBDAO
from django.conf import settings
from core.exceptions import SearchIndexNotFoundException, DataStreamNotFoundException
from django.core.exceptions import FieldError

from core.choices import STATUS_CHOICES, StatusChoices, ChannelTypes, CollectTypeChoices
from core.models import DatastreamI18n, DataStream, DataStreamRevision, Category, VisualizationRevision, DataStreamHits, Setting, DataStreamParameter

from core.lib.elastic import ElasticsearchIndex

from django.core.urlresolvers import reverse
from core import helpers

logger = logging.getLogger(__name__)

try:
    from core.lib.searchify import SearchifyIndex
except ImportError:
#    logger.warning("ImportError: No module named indextank.client.")
    pass

class DataStreamDBDAO(AbstractDataStreamDBDAO):
    """ class for manage access to datastreams' database tables """
    def __init__(self):
        pass

    def create(self, user, datastream=None, **fields):
        """create a new datastream if needed and a datastream_revision"""

        if datastream is None:
            # Create a new datastream (TITLE is for automatic GUID creation)
            datastream = DataStream.objects.create(user=user, title=fields['title'])

        if isinstance(fields['category'], int) or isinstance(fields['category'], long):
            fields['category'] = Category.objects.get(id=fields['category'])

        datastream_revision = DataStreamRevision.objects.create(
            datastream=datastream,
            user=user,
            dataset=fields['dataset'],
            status=fields['status'],
            category=fields['category'],
            data_source=fields['data_source'],
            meta_text=fields['meta_text'],
            select_statement=fields['select_statement']
        )

        DatastreamI18n.objects.create(
            datastream_revision=datastream_revision,
            language=fields['language'],
            title=fields['title'].strip().replace('\n', ' '),
            description=fields['description'].strip().replace('\n', ' '),
            notes=fields['notes'].strip() if 'notes' in fields and fields['notes'] else ''
        )

        if 'tags' in fields:
            datastream_revision.add_tags(fields['tags'])
        if 'sources' in fields:
            datastream_revision.add_sources(fields['sources'])
        if 'parameters' in fields:
            datastream_revision.add_parameters(fields['parameters'])

        return datastream, datastream_revision

    def update(self, datastream_revision, changed_fields, **fields):
        if 'title' in fields:
            fields['title'] = fields['title'].strip().replace('\n', ' ')
        if 'description' in fields:
            fields['description'] = fields['description'].strip().replace('\n', ' ')
        if 'notes' in fields and fields['notes']:
            fields['notes'] = fields['notes'].strip()

        datastream_revision.update(changed_fields, **fields)

        DatastreamI18n.objects.get(datastream_revision=datastream_revision, language=fields['language']).update(
            changed_fields,
            **fields
        )

        if 'tags' in fields:
            datastream_revision.add_tags(fields['tags'])
        if 'sources' in fields:
            datastream_revision.add_sources(fields['sources'])
        if 'parameters' in fields:
            datastream_revision.add_parameters(fields['parameters'])

        return datastream_revision

    def get(self, user, datastream_id=None, datastream_revision_id=None, guid=None, published=False):
        """get all data of datastream 
        :param user: mandatory
        :param datastream_id:
        :param datastream_revision_id:
        :param guid:
        :param published: boolean
        :return: JSON Object
        """

        if settings.DEBUG: logger.info('Getting Datasstream %s' % str(locals()))

        resource_language = Q(datastreami18n__language=user.language)
        category_language = Q(category__categoryi18n__language=user.language)

        if guid:
            condition = Q(datastream__guid=guid)
        elif datastream_id:
            condition = Q(datastream__id=datastream_id)
        elif datastream_revision_id:
            condition = Q(pk=datastream_revision_id)
        else:
            logger.error('[ERROR] DataStreamDBDAO.get: no guid, resource id or revision id')
            raise

        # controla si esta publicado por su STATUS y no por si el padre lo tiene en su last_published_revision
        if published:
            status_condition = Q(status=StatusChoices.PUBLISHED)
            last_revision_condition = Q(pk=F("datastream__last_published_revision"))
        else:
            status_condition = Q(status__in=StatusChoices.ALL)
            last_revision_condition = Q(pk=F("datastream__last_revision"))

        # aca la magia
        account_condition = Q(user__account=user.account)

        try:
            datastream_revision = DataStreamRevision.objects.select_related().get(condition & resource_language & category_language & status_condition & account_condition & last_revision_condition)
        except DataStreamRevision.DoesNotExist:
            logger.error('[ERROR] DataStreamRev Not exist Revision (query: %s %s %s %s account_id: %s %s)'% (condition, resource_language, category_language, status_condition, user.account.id, last_revision_condition))
            raise

        tags = datastream_revision.tagdatastream_set.all().values('tag__name', 'tag__status', 'tag__id')
        sources = datastream_revision.sourcedatastream_set.all().values('source__name', 'source__url', 'source__id')

        try:
            parameters = datastream_revision.get_parameters()
        except FieldError:
            parameters = []

        # Get category name
        category = datastream_revision.category.categoryi18n_set.get(language=user.language)
        datastreami18n = DatastreamI18n.objects.get(datastream_revision=datastream_revision, language=user.language)
        dataset_revision = datastream_revision.dataset.last_revision

        datastream = dict(

            resource_id=datastream_revision.datastream.id,
            revision_id=datastream_revision.id,

            datastream_id=datastream_revision.datastream.id,
            datastream_revision_id=datastream_revision.id,
            dataset_id=datastream_revision.dataset.id,
            user_id=datastream_revision.user.id,
            author=datastream_revision.user.nick,
            account_id=datastream_revision.user.account.id,
            category_id=datastream_revision.category.id,
            category_name=category.name,
            category_slug=category.slug,
            end_point=dataset_revision.end_point,
            filename=dataset_revision.filename,
            collect_type=dataset_revision.dataset.type,
            impl_type=dataset_revision.impl_type,
            status=datastream_revision.status,
            modified_at=datastream_revision.modified_at,
            meta_text=datastream_revision.meta_text,
            guid=datastream_revision.datastream.guid,
            created_at=datastream_revision.dataset.created_at,
            last_revision_id=datastream_revision.datastream.last_revision_id if datastream_revision.datastream.last_revision_id else '',
            last_published_revision_id=datastream_revision.datastream.last_published_revision_id if datastream_revision.datastream.last_published_revision_id else '',
            last_published_date=datastream_revision.datastream.last_published_revision_date if datastream_revision.datastream.last_published_revision_date else '',
            title=datastreami18n.title,
            description=datastreami18n.description,
            notes=datastreami18n.notes,
            tags=tags,
            sources=sources,
            is_cached=dataset_revision.is_cached(), 
            is_file=dataset_revision.is_file(), 
            is_live=dataset_revision.is_live(),
            parameters=parameters,
            data_source=datastream_revision.data_source,
            select_statement=datastream_revision.select_statement,
            slug= slugify(datastreami18n.title),
            cant=DataStreamRevision.objects.filter(dataset__id=datastream_revision.dataset.id).count(),
        )

        return datastream

    def query(self, account_id=None, language=None, page=0, itemsxpage=settings.PAGINATION_RESULTS_PER_PAGE,
          sort_by='-id', filters_dict=None, filter_name=None, exclude=None, filter_status=None,
          filter_category=None, filter_text=None, filter_user=None, full=False):
        """ Consulta y filtra los datastreams por diversos campos """

        query = DataStreamRevision.objects.filter(
            id=F('datastream__last_revision'),
            datastream__user__account=account_id,
            datastreami18n__language=language,
            category__categoryi18n__language=language
        )

        if exclude:
            query.exclude(**exclude)

        if filter_name:
            query = query.filter(datastreami18n__title__icontains=filter_name)

        if filters_dict:
            predicates = []
            for filter_class, filter_value in filters_dict.iteritems():
                if filter_value:
                    predicates.append((filter_class + '__in', filter_value))
            q_list = [Q(x) for x in predicates]
            if predicates:
                query = query.filter(reduce(operator.and_, q_list))

        if filter_status is not None:
            query = query.filter(status__in=[filter_status])

        if filter_category is not None:
            query = query.filter(category__categoryi18n__slug=filter_category)

        if filter_text is not None:
            query = query.filter(Q(datastreami18n__title__icontains=filter_text) | 
                                 Q(datastreami18n__description__icontains=filter_text))

        if filter_user is not None:
            query = query.filter(datastream__user__nick=filter_user)

        total_resources = query.count()
        query = query.values(
            'datastream__user__nick',
            'datastream__user__name',
            'status',
            'id',
            'datastream__guid',
            'datastream__id',
            'category__id',
            'datastream__id',
            'category__categoryi18n__slug',
            'category__categoryi18n__name',
            'datastreami18n__title',
            'datastreami18n__description',
            'created_at',
            'modified_at',
            'datastream__user__id',
            'datastream__last_revision_id',
            'datastream__last_published_revision_id',
            'datastream__last_published_revision__modified_at',
            'dataset__last_revision__dataseti18n__title',
            'dataset__last_revision__impl_type',
            'dataset__last_revision__id'
        )

        query = query.order_by(sort_by)

        if full:
            parameters = DataStreamParameter.objects.filter(
                    datastream_revision_id__in=[x['id'] for x in query]
                ).values(
                    'name', 'default', 'position', 'description', 'datastream_revision_id'
                )
            par_dict = {}
            for parameter in parameters:
                par_dict.setdefault(parameter['datastream_revision_id'], []).append(parameter)
            for datastream in query:
                datastream['parameters'] = par_dict.setdefault(datastream['id'], [])
        
        # Limit the size.
        nfrom = page * itemsxpage
        nto = nfrom + itemsxpage
        query = query[nfrom:nto]

        # sumamos el field cant
        map(self.__add_cant, query)

        return query, total_resources

    def __add_cant(self, item):
            item['cant']=DataStreamRevision.objects.filter(datastream__id=item['datastream__id']).count()


    def query_hot_n(self, limit, lang, hot = None):

        if not hot:
            hot = Setting.objects.get(pk = settings.HOT_DATASTREAMS).value

        sql = """SELECT `ao_datastream_revisions`.`id` as 'datastream_revision_id',
                   `ao_datastream_revisions`.`datastream_id` as 'datastream_id',
                   `ao_datastream_i18n`.`title`,
                   `ao_datastream_i18n`.`description`,
                   `ao_categories_i18n`.`name` AS `category_name`,
                   `ao_users`.`nick` AS `user_nick`,
                   `ao_users`.`email` AS `user_email`,
                   `ao_users`.`account_id`
            FROM `ao_datastream_revisions`
            INNER JOIN `ao_datastream_i18n` ON (`ao_datastream_revisions`.`id` = `ao_datastream_i18n`.`datastream_revision_id`)
            INNER JOIN `ao_categories` ON (`ao_datastream_revisions`.`category_id` = `ao_categories`.`id`)
            INNER JOIN `ao_categories_i18n` ON (`ao_categories`.`id` = `ao_categories_i18n`.`category_id`)
            INNER JOIN `ao_datastreams` ON (`ao_datastream_revisions`.`datastream_id` = `ao_datastreams`.`id`)
            INNER JOIN `ao_users` ON (`ao_datastreams`.`user_id` = `ao_users`.`id`)
            WHERE `ao_datastream_revisions`.`id` IN (
                SELECT MAX(`ao_datastream_revisions`.`id`)
                FROM `ao_datastream_revisions`
                 WHERE `ao_datastream_revisions`.`datastream_id` IN (""" + hot + """)
                       AND `ao_datastream_revisions`.`status` = 3
                GROUP BY `datastream_id`
            ) -- AND `ao_categories_i18n`.`language` = %s"""

        cursor = connection.cursor()
        cursor.execute(sql, [lang])
        row = cursor.fetchone()
        datastreams = []
        while row:
            datastream_id = row[1]
            title = row[2]
            slug = slugify(title)
            permalink = reverse('datastreams-data', kwargs={'id': datastream_id, 'format': 'json'}, urlconf='microsites.urls')
            datastreams.append({'id'          : row[0],
                                'title'        : title,
                                'description'  : row[3],
                                'category_name': row[4],
                                'user_nick'    : row[5],
                                'user_email'   : row[6],
                                'permalink'    : permalink,
                                'account_id'   : row[7]
                                })
            row = cursor.fetchone()
        return datastreams

    def query_filters(self, account_id=None, language=None):
        """
        Reads available filters from a resource array. Returns an array with objects and their
        i18n names when available.
        """
        query = DataStreamRevision.objects.filter(
                                                id=F('datastream__last_revision'),
                                                dataset__user__account=account_id,
                                                datastreami18n__language=language,
                                                category__categoryi18n__language=language)

        query = query.values('datastream__user__nick', 'datastream__user__name', 'status',
                             'category__categoryi18n__name')

        filters = set([])

        for res in query:
            status = res.get('status')

            filters.add(('status', status,
                unicode(STATUS_CHOICES[status])
                ))
            if 'category__categoryi18n__name' in res:
                filters.add(('category', res.get('category__categoryi18n__name'),
                    res.get('category__categoryi18n__name')))
            if res.get('datastream__user__nick'):
                filters.add(('author', res.get('datastream__user__nick'),
                    res.get('datastream__user__name')))

        return [{'type':k, 'value':v, 'title':title} for k,v,title in filters]

    def query_childs(self, datastream_id, language, status=None):
        """ Devuelve la jerarquia completa para medir el impacto """

        related = dict()

        query = VisualizationRevision.objects.select_related()

        if status == StatusChoices.PUBLISHED:
            query = query.filter(visualization__last_published_revision_id=F('id'))
        else:
            query = query.filter(visualization__last_revision_id=F('id'))

        query = query.filter(
            visualization__datastream__id=datastream_id,
            visualizationi18n__language=language
        ).values('status', 'id', 'visualizationi18n__title', 'visualizationi18n__description',
                 'visualization__user__nick', 'created_at', 'visualization__last_revision')

        # ordenamos desde el mas viejo
        related['visualizations'] = query.order_by("created_at")

        return related


class DatastreamSearchDAOFactory():
    """ select Search engine"""

    def __init__(self):
        pass

    def create(self, datastream_revision):
        if settings.USE_SEARCHINDEX == 'searchify':
            self.search_dao = DatastreamSearchifyDAO(datastream_revision)
        elif settings.USE_SEARCHINDEX == 'elasticsearch':
            self.search_dao = DatastreamElasticsearchDAO(datastream_revision)
        elif settings.USE_SEARCHINDEX == 'test':
            self.search_dao = DatastreamSearchDAO(datastream_revision)
        else:
            raise SearchIndexNotFoundException()

        return self.search_dao

        
class DatastreamSearchDAO():
    """ class for manage access to datastream index"""

    TYPE="ds"
    def __init__(self, revision):
        self.revision=revision
        self.search_index = SearchifyIndex()

    def _get_type(self):
        return self.TYPE
    def _get_id(self):
        """ Get Tags """
        return "%s::%s" %(self.TYPE.upper(),self.revision.datastream.guid)

    def _get_tags(self):
        """ Get Tags """
        return self.revision.tagdatastream_set.all().values_list('tag__name', flat=True)

    def _get_category(self):
        """ Get category name """
        return self.revision.category.categoryi18n_set.all()[0]

    def _get_i18n(self):
        """ Get category name """
        return DatastreamI18n.objects.get(datastream_revision=self.revision)
        
    def _build_document(self):

        tags = self._get_tags()

        category = self._get_category()
        datastreami18n = self._get_i18n()

        text = [datastreami18n.title, datastreami18n.description, self.revision.user.nick, self.revision.datastream.guid]
        text.extend(tags) # datastream has a table for tags but seems unused. I define get_tags funcion for dataset.
        text = ' '.join(text)

        meta_text=[]
        if self.revision.meta_text != "":
            meta_json = json.loads(self.revision.meta_text)
            if 'field_values' in meta_json:
                for data in meta_json['field_values']:
                    meta_text.append(data)

        dataset = self.revision.dataset

        timestamp = int(int(time.mktime(self.revision.modified_at.timetuple()))*1000)
        if dataset.last_published_revision and dataset.last_published_revision.is_live():
            timestamp = settings.MAX_TIMESTAMP

        document = {
                'docid' : self._get_id(),
                'fields' :
                    {'type' : self.TYPE,
                     'resource_id': self.revision.datastream.id,
                     'revision_id': self.revision.id,
                     'datastream_id': self.revision.datastream.id,
                     'datastream__revision_id': self.revision.id,
                     'title': datastreami18n.title,
                     'text': text,
                     'description': datastreami18n.description,
                     'owner_nick' :self.revision.user.nick,
                     'tags' : ','.join(tags),
                     'account_id' : self.revision.user.account.id,
                     'parameters': "",
                     'timestamp': timestamp,
                     'created_at': int(time.mktime(self.revision.created_at.timetuple())),
                     'modified_at': int(time.mktime(self.revision.modified_at.timetuple())),
                     'hits': 0,
                     'web_hits': 0,
                     'api_hits': 0,
                     'end_point': self.revision.dataset.last_published_revision.end_point,
                    },
                'categories': {'id': unicode(category.category_id), 'name': category.name},
                'meta_text': meta_text,
                }

        return document


class DatastreamSearchifyDAO(DatastreamSearchDAO):
    """ class for manage access to datastreams searchify documents """
    def __init__(self, datastream_revision):
        self.datastream_revision=datastream_revision
        self.search_index = SearchifyIndex()
        
    def add(self):
        self.search_index.indexit(self._build_document())
        
    def remove(self, datastream_revision):
        self.search_index.delete_documents([self._get_id()])


class DatastreamElasticsearchDAO(DatastreamSearchDAO):
    """ class for manage access to datastreams elasticsearch documents """

    def __init__(self, revision):
        self.revision=revision
        self.search_index = ElasticsearchIndex()
        
    def add(self):
        output=self.search_index.indexit(self._build_document())

        return (self.revision.id, self.revision.datastream.id, output)
        
    def remove(self):
        return self.search_index.delete_documents([{"type": self._get_type(), "docid": self._get_id()}])


class DatastreamHitsDAO():
    """class for manage access to Hits in DB and index"""

    doc_type = "ds"
    from_cache = False

    # cache ttl, 1 hora
    TTL=3600 

    CHANNEL_TYPE=("web","api")

    def __init__(self, datastream):
        self.datastream = datastream
        if isinstance(self.datastream, dict):
            self.datastream_id = self.datastream['datastream_id']
        else:
            self.datastream_id = self.datastream.id 
        #self.datastream_revision = datastream.last_published_revision
        self.search_index = ElasticsearchIndex()
        self.cache=Cache()

    def add(self,  channel_type):
        """agrega un hit al datastream. """

        # TODO: Fix temporal por el paso de DT a DAO.
        # Es problema es que por momentos el datastream viene de un queryset y otras veces de un DAO y son objetos
        # distintos
        try:
            datastream_id = self.datastream.datastream_id
        except:
            datastream_id = self.datastream['datastream_id']

        try:
            guid = self.datastream.guid
        except:
            guid = self.datastream['guid']

        try:
            hit=DataStreamHits.objects.create(datastream_id=datastream_id, channel_type=channel_type)
        except IntegrityError:
            # esta correcto esta excepcion?
            raise DataStreamNotFoundException()

        # armo el documento para actualizar el index.
        doc={'docid':"DS::%s" % guid,
                "type": "ds",
                "script": "ctx._source.fields.%s_hits+=1" % self.CHANNEL_TYPE[channel_type]}

        return self.search_index.update(doc)

    def count(self, channel_type=ChannelTypes.WEB):
        return DataStreamHits.objects.filter(datastream_id=self.datastream_id, channel_type=channel_type).count()

    def count_by_days(self, day=30, channel_type=None):
        """trae un dict con los hits totales de los ultimos day y los hits particulares de los días desde day hasta today"""

        # no sé si es necesario esto
        if day < 1:
            return {}

        # tenemos la fecha de inicio
        start_date=now()-timedelta(days=day)

        # tomamos solo la parte date
        truncate_date = connection.ops.date_trunc_sql('day', 'created_at')

        qs=DataStreamHits.objects.filter(datastream_id=self.datastream_id,created_at__gte=start_date)

        if channel_type:
            qs=qs.filter(channel_type=channel_type)

        hits=qs.extra(select={'_date': truncate_date, "fecha": 'DATE(created_at)'}).values("fecha").order_by("created_at").annotate(hits=Count("created_at"))

        control=[ now().date()-timedelta(days=x) for x in range(day-1,0,-1)]
        control.append(now().date())
        
        for i in hits:
            try:
                control.remove(i['fecha'])
            except ValueError:
                pass

        hits=list(hits)
            
        for i in control:
            hits.append({"fecha": i, "hits": 0})

        hits = sorted(hits, key=lambda k: k['fecha']) 

        # transformamos las fechas en isoformat
        hits=map(self._date_isoformat, hits)
        return hits

    def _date_isoformat(self, row):
        row['fecha']=row['fecha'].isoformat()
        return row
