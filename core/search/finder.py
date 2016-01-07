import re
import types
import logging
from django.db import models, connection
from django.conf import settings
from django.core.paginator import InvalidPage
from django.core.urlresolvers import reverse
from core.utils import slugify
from core import helpers, choices
from core.exceptions import SearchIndexNotFoundException
from core.plugins_point import DatalPluginPoint

logger = logging.getLogger(__name__)


class FinderManager:

    def __init__(self):
        self.finder = None
        logger.info('FinderManager start in %s (index: %s)' % (str(settings.SEARCH_INDEX['url']), settings.SEARCH_INDEX['index']))

    def get_finder(self):
        if not self.finder:
            self.finder = self.finder_class()

        logger.info('FinderManager return %s finder' % self.finder)
        return self.finder

    def get_failback_finder(self):
        self.finder = self.failback_finder_class()
        return self.finder

    def search(self, *args, **kwargs):

        try:
            return self.get_finder().search(*args, **kwargs)
        except InvalidPage:
            raise
        except Exception, e:
            return self.get_failback_finder().search(*args, **kwargs)

from core.lib.elastic import ElasticsearchIndex

try:
    from core.lib.searchify import SearchifyIndex
except ImportError:
    logger.warning("ImportError: No module named indextank.client.")

class FinderQuerySet(object):
    def __init__(self, finder, *args, **kwargs):
        self.values = {}
        self.finder = finder
        for key, value in kwargs.items():
            self.values[key] = value
        
    def __getitem__(self, key):
        if isinstance(key, slice):
            start = 0 if key.start is None else key.start
            stop = 0 if key.stop is None else key.stop
            limit = int(stop-start)
            page = int(start / limit) + 1 if limit else 1
            self.results, self.search_time, self.facets = self.finder.search(
                slice=limit, page=page, **self.values)
            return self.results

    def __len__(self):
        if not hasattr(self, 'search_time'):
            self[0:25]
        return self.search_time['count']

class Finder:

    order_by = {}

    def __init__(self):

        logger.info('New %sIndex INIT' % settings.USE_SEARCHINDEX)
        if settings.USE_SEARCHINDEX == 'searchify':
            self.index = SearchifyIndex()
        elif settings.USE_SEARCHINDEX == 'elasticsearch':
            self.index = ElasticsearchIndex()
#        elif settings.USE_SEARCHINDEX == 'test':
#            self.search_dao = DatastreamSearchDAO(datastream_revision)
        else:
            raise SearchIndexNotFoundException()

    def extract_terms_from_query(self):
        subqueries = re.split('\+', self.query.strip())
        query_terms = []

        for subquery in subqueries:
            if subquery:
                terms = re.split('"(.*?)"|', subquery.strip())
                subquery_terms = []
                for term in terms:
                    try:
                        clean_term = term.strip()
                        if clean_term:
                            subquery_terms.append(clean_term)
                    except:
                        pass
                query_terms.append(subquery_terms)

        # cleaning the blocked terms, unless this terms are the only terms
        term_count = 0
        terms_filtered = []
        for query in query_terms:
            subquery_terms = []
            for term in query:
                if term not in settings.SEARCH_TERMS_EXCLUSION_LIST:
                    subquery_terms.append(term)
                    term_count = term_count + 1
            terms_filtered.append(subquery_terms)

        if term_count:
            self.terms = terms_filtered
        else:
            self.terms = query_terms

        self.terms = [ subquery for subquery in self.terms if subquery ]

    def get_id_name(self, r):
        if r == 'ds':
            return "datastream_id"
        elif r == 'vz':
            return "visualization_id"
        elif r == 'dt':
            return "dataset_id"

        for finder in DatalPluginPoint.get_active_with_att('finder'):
            if finder.doc_type == r:
                return finder.id_name


    def get_dictionary(self, doc):
        if doc['type'] == 'ds':
            return self.get_datastream_dictionary(doc)
        elif doc['type'] == 'vz':
            return self.get_visualization_dictionary(doc)
        elif doc['type'] == 'dt':
            return self.get_dataset_dictionary(doc)

        for finder in DatalPluginPoint.get_active_with_att('finder'):
            if finder.doc_type == doc['type']:
                return finder.get_dictionary(doc)


    def get_datastream_dictionary(self, document):

        parameters = []
        if document['parameters']:
            import json
            parameters = json.loads(document['parameters'])

        id = document['datastream_id']
        title = document['title']
        slug = slugify(title)
        permalink = reverse('viewDataStream.view', urlconf='microsites.urls',
                            kwargs={'id': id, 'slug': slug})

        data = dict (id=id, revision_id=document['datastream__revision_id'], title=title, description=document['description'], parameters=parameters,
                             tags=[ tag.strip() for tag in document['tags'].split(',') ], permalink=permalink,
                             type=document['type'], category=document['category_id'], category_name=document['category_name'], guid=document['docid'].split("::")[1]
                             ,end_point=document['end_point'], timestamp=document['timestamp'], owner_nick=document['owner_nick'])

        return data

    def get_dataset_dictionary(self, document):

        parameters = []
        if document['parameters']:
            import json
            parameters = json.loads(document['parameters'])

        dataset_id = document['dataset_id']
        title = document['title']
        slug = slugify(title)
        permalink = reverse('manageDatasets.view', urlconf='microsites.urls', kwargs={'dataset_id': dataset_id,'slug': slug})

        dataset = dict(id=dataset_id, revision_id=document['datasetrevision_id'], title=title, description=document['description'], parameters=parameters,
                          tags=[ tag.strip() for tag in document['tags'].split(',') ], permalink=permalink,
                          #type=document['type'],end_point=document['end_point'], timestamp=document['timestamp'])
                             type=document['type'], category=document['category_id'], category_name=document['category_name'], guid=document['docid'].split("::")[1]
                             ,end_point=document['end_point'], timestamp=document['timestamp'], owner_nick=document['owner_nick'])
        return dataset

    def get_visualization_dictionary(self, document):

        try:
            if document['parameters']:
                import json
                parameters = json.loads(document['parameters'])
            else:
                parameters = []

        except:
            parameters = []

        title = document['title']
        slug = slugify(title)
        permalink = reverse('chart_manager.view',  urlconf='microsites.urls',
            kwargs={'id': document['visualization_id'], 'slug': slug})

        visualization = dict(id=document['visualization_id'], revision_id=document['visualization_revision_id'], title=title, description=document['description'],
                             parameters=parameters, tags=[tag.strip() for tag in document['tags'].split(',')],
                             permalink=permalink,
                             type=document['type'], category=document['category_id'], category_name=document['category_name'], guid=document['docid'].split("::")[1]
                             ,end_point=document.get('end_point', None), timestamp=document['timestamp'], owner_nick=document['owner_nick'])
        return visualization

    def _get_query(self, values, boolean_operator = 'AND'):
        self._validate_boolean_operator(boolean_operator)

        query = []
        for pair in values.iteritems():
            query.append('%s:%s' % pair)
        boolean_operator_query = ' %s ' % boolean_operator
        return boolean_operator_query.join(query)

    def _add_query(self, query, subquery, boolean_operator = 'AND'):
        self._validate_boolean_operator(boolean_operator)

        if query:
            return ' '.join([query, boolean_operator, subquery])
        else:
            return subquery

    def _validate_boolean_operator(self, boolean_operator):
        boolean_operators = ['AND', '+', 'OR', 'NOT', '-']
        if boolean_operator not in boolean_operators:
            raise Exception('Boolean operator used, does not exists')

    def _get_category_filters(self, category_filters, filter_key, filter_value):
        if filter_value:
            if type(filter_value) == types.ListType:
                category_filters[filter_key] = filter_value
            else:
                category_filters[filter_key] = [filter_value]

