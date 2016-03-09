import types
import logging

from django.conf import settings
from django.core.urlresolvers import reverse

from core.search.finder import Finder


class IndexTankFinder(Finder):

    order_by = {}

    def search(self, *args, **kwargs):

        self.logger.info('Conectado con el search (args %s) (kwargs %s)' % (args,kwargs))
        self.query = kwargs.get('query', '')
        self.account_id = kwargs.get('account_id')
        self.resource = kwargs.get('resource', 'all')
        page = kwargs.get('page', 0)
        max_results = kwargs.get('max_results', 99999)
        slice = kwargs.get('slice', settings.PAGINATION_RESULTS_PER_PAGE)

        if page == 0:
            start = 0
            end = max_results
        else:
            end = max_results < slice and max_results or slice
            start = (page - 1) * end

        self.meta_data = kwargs.get('meta_data', {})

        self.extract_terms_from_query()

        query = self.make_query()
        self.last_query = query

        ### CATEGORY FILTERS
        category_filters = kwargs.get('category_filters', None)
        if category_filters is None:
            category_filters = {}
            self._get_category_filters(category_filters, 'id', kwargs.get('category_id'))
            self._get_category_filters(category_filters, 'name', kwargs.get('category_name'))

        scoring = kwargs.get('scoring', 1)

        #TODO define a search function in the right place
        results = self.index.search(query, start=start, length=end, snippet_fields=['title','text'], fetch_fields="*",
                                    fetch_categories="*", category_filters=category_filters, scoring_function=scoring)

        search_time = results['search_time']
        facets = results['facets']
        facets[u'id'] = None
        docs = results['results']

        order = kwargs.get('order', None)
        if order:
            docs = sorted(docs, key=lambda x: x[self.order_by.get(order)],
                          reverse=(kwargs.get('order_type', 'descending') == 'descending'))

        results = []
        # for check the real results ==> results.append(docs)

        for doc in docs:
            try:
                doc['category_name'] = doc.get("category_name","UNCATEGORIZED")
                to_add = self.get_dictionary(doc)
                results.append(to_add)
                # TODO, I can't ind the problem
                if doc['category_name'] == "UNCATEGORIZED":
                    logger = logging.getLogger(__name__)
                    logger.error("Can't find category on index -- %s" % str(doc))
                    
            except Exception, e:
                logger = logging.getLogger(__name__)
                logger.error('Search IndexTank [ERROR(%s--%s)] with doc = %s [TRACE:%s]' % (doc['type'], doc['title'], unicode(doc), repr(e)))

        return results, search_time, facets

    def make_query(self):

        l_subqueries = []
        if self.query:

            for l_term_set in self.terms:
                l_sub_query = ''
                l_terms_or = ' OR '.join(l_term_set)
                l_terms_and = ' AND '.join(l_term_set)
                l_terms_and = '(' + l_terms_and + ')^10'
                l_sub_query = ' OR '.join([l_terms_or, l_terms_and])
                l_subqueries.append(l_sub_query)

        if len(l_subqueries) > 1:
            l_subqueries = [ '(' + l_subquery + ')' for l_subquery in l_subqueries ]

        l_indextank_query = ' AND '.join(l_subqueries)

        metadata_query = ''
        for i in self.meta_data:
            metadata_query = ' AND '.join(['%s:%s' % (i, self.meta_data[i])])

        if l_indextank_query and metadata_query:
            l_indextank_query = ' AND '.join([l_indextank_query, metadata_query])
        elif metadata_query:
            l_indextank_query = metadata_query

        # user search is here to prevent ORs ANDs bugs we put ()
        if l_indextank_query:
            l_indextank_query = '(' + l_indextank_query + ')'

        # accounts!
        if self.account_id:
            # for one account_id
            if type(self.account_id) in (types.LongType, types.IntType):
                subquery = self._get_query({'account_id': self.account_id})
                l_indextank_query = self._add_query(l_indextank_query, subquery)
            else:
                # for more than one account
                account_list = []
                for accountid in self.account_id:
                    account_list.append(self._get_query({'account_id': accountid}))
                subquery = '(' + ' OR '.join(account_list) + ')'
                l_indextank_query = self._add_query(l_indextank_query, subquery)

        # resource
        # all        -> 'AND (type:ds OR type:db OR type:chart)'
        # ds         -> 'AND type:ds'
        # [ds,chart] -> 'AND (type:ds OR type:chart)'

        # curating resource types
        if self.resource == 'all':
            self.resource = ['ds', 'db', 'chart', 'dt']

#        elif self.resource in resource_types:
#            self.resource = [self.resource]

        resource_type_query = ''
        for res in self.resource:
            subquery = self._get_query({'type': res})
            resource_type_query = self._add_query(resource_type_query, subquery, 'OR')

        if len(self.resource) > 1:
            l_indextank_query = self._add_query(l_indextank_query, '('+resource_type_query+')')
        else:
            l_indextank_query = self._add_query(l_indextank_query, resource_type_query)

        return l_indextank_query
