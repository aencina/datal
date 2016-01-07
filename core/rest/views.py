from django.http import Http404
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import mixins
from core.models import GuidModel, CategoryI18n
from core.communitymanagers import FinderManager
from core.search.elastic import ElasticsearchFinder
from core.v8.views import EngineViewSetMixin
from core.plugins_point import DatalPluginPoint
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotFound
from django.conf import settings

import logging
import urllib

logger = logging.getLogger(__name__)

class ResourceViewSet(EngineViewSetMixin, mixins.RetrieveModelMixin, 
    viewsets.GenericViewSet):
    queryset = GuidModel
    lookup_field = 'guid'
    dao_filename = 'filename'
    _data_types = [settings.TYPE_DATASET, settings.TYPE_DATASTREAM, settings.TYPE_VISUALIZATION]
    app = 'workspace'
    published = True
        
    def list(self, request, format='json'):
        rp = request.query_params.get('rp', None) # TODO check for rp arguemnt used in some grids
        limit = request.query_params.get('limit', rp)
        offset = request.query_params.get('offset', '0')
        order = request.query_params.get('order', None)
        reverse = order and order[0] == '-'
        order = order and order.strip('-')
        page_num = int(offset)/int(limit) + 1 if limit else 0
        categories= request.query_params.get('categories', None)
        category_filters = map(lambda x: str(urllib.unquote(x)), categories.split(',')) if categories else None

        if order == 'viewed': order = 'web_top'
        elif order == 'downloaded': order = 'api_top'

        # tenemos en cuenta los accounts federados
        account_ids = [x['id'] for x in request.auth['account'].account_set.values('id').all()] + [request.auth['account'].id]
        resources, time, facets = FinderManager(ElasticsearchFinder).search(
            query=request.query_params.get('query', ''),
            slice=int(limit) if limit else None,
            page=page_num,
            account_id=account_ids,
            user_id=request.user.id,
            resource=self.get_data_types(),
            order=order,
            category_filters=category_filters ,
            reverse=reverse)

        page = self.paginate_queryset(resources)
        if page is not None:
            self.paginator.count = time['count']
            serializer = self.get_serializer(resources, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(resources, many=True,
            context={'request':request} )

        return Response(serializer.data)

    def get_data_types(self):
        if hasattr(self, 'data_types'):
            return self.data_types
        
        resources = self.request.query_params.get('resources', None)
        if resources:
            return resources.split(',')
        
        answer = self._data_types
        for finder in DatalPluginPoint.get_active_with_att('finder'):
            answer.append(finder.doc_type)
        return answer

    def get_queryset(self):
        params = {'language': self.request.auth['language'] }
        params['published'] = self.published
        params[self.dao_get_param] = self.kwargs[self.lookup_field]
        try:
            return super(ResourceViewSet, self).get_queryset().get(**params)
        except (ObjectDoesNotExist, ValueError):
            raise NotFound()

    def get_object(self):
        obj = self.get_queryset()
        if not obj:
            raise NotFound()

        self.check_object_permissions(self.request, obj)
        return obj
