from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import serializers
from rest_framework.response import Response
from core.daos.datasets import DatasetDBDAO
from core.daos.datastreams import DataStreamDBDAO
from core.daos.visualizations import VisualizationDBDAO
from core.choices import STATUS_CHOICES_REST
from rest_framework.compat import OrderedDict
from rest_framework_extensions.cache.decorators import cache_response
from django.conf import settings
from core.rest.cache import CacheKeyConstructor
from core.plugins_point import DatalPluginPoint

import json
import logging

logger = logging.getLogger(__name__)

class ResourceSerializer(serializers.Serializer):
    resources = (
        ('dataset', settings.TYPE_DATASET),
        ('datastream', settings.TYPE_DATASTREAM),
        ('visualization', settings.TYPE_VISUALIZATION)
    )
    resource_type = serializers.CharField()
    created_at = serializers.DateTimeField()

    @classmethod
    def get_mapping_dict(cls):
        answer = {
            'title': dict(map(lambda x: (x[1], x[0] + 'i18n__title'), cls.resources)),
            'description': dict(map(lambda x: (x[1], x[0] + 'i18n__description'), cls.resources)),
            'user': dict(map(lambda x: (x[1], x[0] + '__user__name'), cls.resources)),
            'nick': dict(map(lambda x: (x[1], x[0] + '__user__nick'), cls.resources)),
            'category': {
                settings.TYPE_DATASET: 'category__categoryi18n__slug',
                settings.TYPE_DATASTREAM: 'category__categoryi18n__slug',
                settings.TYPE_VISUALIZATION: 'visualization__datastream__last_revision__category__categoryi18n__slug',
            },
            'revision_id': dict(map(lambda x: (x[1], x[0] + '__last_revision_id'), cls.resources)),
            'published_revision_id': dict(map(lambda x: (x[1], x[0] + '__last_published_revision_id'), cls.resources)),
            'resource_id': dict(map(lambda x: (x[1], x[0] + '__id'), cls.resources)),
            'lib': {
                settings.TYPE_VISUALIZATION: 'lib'
            },
            'parameters': {
                settings.TYPE_DATASTREAM: 'parameters'
            }
        }
        for multiple_resources in DatalPluginPoint.get_active_with_att('multiple_resources'):
            for key, value in multiple_resources.get_mapping_dict().items():
                inner = answer.setdefault(key, {})
                inner.update(value)
        return answer

    def get_impl_details(self, obj):
        if 'impl_details' in obj:
            return json.loads(obj['impl_details'])
    
    def get_status_name(self, status_id):
        for id, valor in STATUS_CHOICES_REST:
            if id == status_id:
                return valor

    def get_type(self, obj):
        if 'impl_details' in obj:
            json_obj = json.loads(obj['impl_details'])
            return json_obj['format']['type']

    def to_representation(self, obj):
        answer = super(ResourceSerializer, self).to_representation(obj)
        for key, value in self.get_mapping_dict().items():
            if answer['resource_type'] in value:
                answer[key] = obj[value[answer['resource_type']]]
            else:
                answer[key] = None

        answer['status'] = self.get_status_name(obj['status'])
        answer['type'] = self.get_type(obj)
        answer['impl_details'] = self.get_impl_details(obj)

        return OrderedDict(answer)


def order_method(dic):
    def order_inner(obj):
        if isinstance(dic, dict):
            if obj['resource_type'] in dic:
                return obj[dic[obj['resource_type']]]
        return obj[dic]
    return order_inner

class MultipleResourceViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = ResourceSerializer

    def get_resources_types(self):
        resources_types = [
            (DatasetDBDAO, settings.TYPE_DATASET),
            (DataStreamDBDAO, settings.TYPE_DATASTREAM),
            (VisualizationDBDAO, settings.TYPE_VISUALIZATION)
        ]
        for multiple_resources in DatalPluginPoint.get_active_with_att('multiple_resources'):
            resources_types.append(multiple_resources.get_resources_types())
        return resources_types
        
    def get_queryset(self):
        return map(lambda x: x(), dict(self.get_resources_types()).keys())

    def get_status_id(self, status):
        if status:
            for id, valor in STATUS_CHOICES_REST:
                if status == valor:
                    return id

    def order_queryset(self, queryset):
        ordering = self.request.query_params.get('ordering', None)
        if ordering:
            reverse = False
            if ordering[0] == '-':
                reverse = True
                ordering = ordering.strip('-')
            mapping_dict = ResourceSerializer.get_mapping_dict()
            order_dict = {}
            if ordering in mapping_dict.keys():
                order_dict = mapping_dict[ordering]
            else:
                order_dict = ordering
            return sorted(queryset, key=order_method(order_dict), reverse=reverse)
        return queryset

    def filter_queryset(self, querysets):
        status = self.request.query_params.get('status', None)
        status_id = self.get_status_id(status)
        category = self.request.query_params.get('category', None)
        query = self.request.query_params.get('query', None)
        user = self.request.query_params.get('user', None)

        types = dict(self.get_resources_types())
        resources_types = (self.request.query_params.get('resources', None) or 
                           types.values())

        answer=[]
        for queryset in querysets:
            res_type = types[type(queryset)]
            if  res_type in resources_types:
                queryset, total = queryset.query(
                    account_id=self.request.auth['account'].id,
                    language=self.request.auth['language'],
                    filter_status=status_id,
                    filter_category=category,
                    filter_text=query,
                    filter_user=user,
                    full=True
                )
                for result in list(queryset):
                    result['resource_type'] = res_type
                    answer.append(result)


        return self.order_queryset(answer)

    #@cache_response(60 * 5, cache_errors=False, key_func=CacheKeyConstructor())
    def list(self, request, *args, **kwargs):
        return super(MultipleResourceViewSet, self).list(request, *args, **kwargs)