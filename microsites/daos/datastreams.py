# -*- coding: utf-8 -*-
import operator, logging
from django.db.models import Q, F
from core.models import Dataset, DatasetRevision, DataStream, Visualization, DataStreamRevision, VisualizationRevision
from core.daos.visualizations import VisualizationDBDAO

class DatastreamDAO():
    """ class for integrated managment of datastream + datastream_revision + datastream_i18n """

    def __init__(self, language=None, resource=None, datastream_id=0, datastream_revision_id=0):
        # internal used resources (optional). You could start by dataset or revision
        if type(resource) == DataStream:
            self.datastream = resource
            self.datastream_revision = DataStreamRevision.objects.get(pk=self.datastream.last_published_revision_id)
        elif type(resource) == DataStreamRevision:
            self.datastream_revision=resource
            self.datastream = resource.datastream
        elif datastream_id > 0:
            self.datastream=DataStream.objects.get(pk=datastream_id)
            self.datastream_revision = DataStreamRevision.objects.get(pk=self.datastream.last_published_revision_id)
        elif datastream_revision_id > 0:
            self.datastream_revision = DataStreamRevision.objects.get(pk=datastream_revision_id)
            self.datastream = self.datastream_revision.datastream
        else:
            self.datastream_revision = None
            self.datastream = None

        if language:
            self.language = language
        elif self.datastream:
            self.language = self.datastream.user.language

    def get(self):
        """ get a full datastream data """
        if self.datastream_revision is None:
            return None
        query = DataStreamRevision.objects.filter(pk=self.datastream_revision.id)
        query = query.filter(datastreami18n__language=self.language, category__categoryi18n__language=self.language)

        query = query.values('status', 'id', 'category__id', 'datastream__id', 'id', 'datastream__guid'
                            , 'category__categoryi18n__name', 'datastreami18n__title'
                            , 'datastreami18n__description', 'datastream__user__id')#TODO add , 'created_at' but not as an date object
        try:
            query = query.order_by('-id')[0]
        except IndexError:
            query = None

        return query

    def query(self, account_id, language=None, page=0, itemsxpage=10, order='-id', filters_dict=None):
        """ query for full datastream lists"""
        if not language:
            language = self.language

        """
        query = DataStreamRevision.objects.filter(user__account=account_id)
        query = query.filter(datastreami18n__language=language)
        query = query.filter(category__categoryi18n__language=language)
        """
        query = DataStreamRevision.objects.filter(id=F('datastream__last_published_revision'),
                                                user__account=account_id,
                                               datastreami18n__language=language,
                                               category__categoryi18n__language=language)
        if filters_dict:
            # Construct the query with Q.
            # Extracted from: http://www.michelepasin.org/blog/2010/07/20/the-power-of-djangos-q-objects/

            predicates = []
            for filter_class, filter_value in filters_dict.iteritems():
                if filter_value:
                    predicates.append((filter_class + '__in', filter_value))
            q_list = [Q(x) for x in predicates]
            if predicates:
                query = query.filter(reduce(operator.and_, q_list))


        total_resources = query.count()
        query = query.values('status', 'id', 'category__id', 'datastream__id', 'datastream__user__id'
                            , 'category__categoryi18n__name', 'datastreami18n__title'
                            , 'dataset__datasetrevision__dataseti18n__title', 'datastream__guid'
                            , 'dataset__datasetrevision__end_point'
                            , 'datastreami18n__description', 'datastream__user__nick', 'created_at','dataset')

        query = query.order_by(order)
        # Limit the size.
        nfrom = page * itemsxpage
        nto = nfrom + itemsxpage
        query = query[nfrom:nto]

        return query, total_resources

    def query_related_resources(self):
        """ get all related resources for measuring impact """

        ret = {}
        ds_json = self.get()
        ret['datastreams']= [ds_json] if ds_json else []
        # visualizations = Visualization.objects.filter(datastream=self.datastream)
        visualizations = Visualization.objects.filter(last_revision__visualization__datastream=self.datastream)
        ret['visualizations'] = []
        for visualization in visualizations:
            vz = VisualizationDBDAO().get(self.language, visualization_revision_id=visualization.last_published_revision.id, published=True)
            ret['visualizations'].append(vz)
        return ret
