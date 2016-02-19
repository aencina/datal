# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import detail_route
from core.daos.datastreams import DataStreamDBDAO, DatastreamHitsDAO
from core.daos.datasets import DatasetDBDAO
from core.lifecycle.datastreams import DatastreamLifeCycleManager
from django.utils.translation import ugettext_lazy as _
from api.v2.serializers import ResourceSerializer
from core.rest.views import ResourceViewSet
from core.choices import DATASTREAM_IMPL_VALID_CHOICES
from core.models import Dataset
from rest_framework import serializers
from rest_framework import mixins
from rest_framework import exceptions
from rest_framework.response import Response
from core.choices import StatusChoices
from core.v8.forms import DatastreamRequestForm
from rest_framework import renderers
from core.builders.datastreams import SelectStatementBuilder, DataSourceBuilder
from core.v8.renderers import *

class DataStreamSerializer(ResourceSerializer):
    title = serializers.CharField(
        help_text=_(u'Título del conjunto de datos'))
    description = serializers.CharField(

        help_text=_(u'Descripción del conjunto de datos'))
    category = serializers.CharField(
        help_text=_(u'Nombre de la categoría para clasificar los recursos. Debe coincidir con alguna de las categorías de la cuenta'))
    notes = serializers.CharField(
        required=False,
        allow_null=True,
        help_text=_(u'Texto de la nota del conjunto de datos'))
    table_id = serializers.IntegerField(
        required=False, 
        allow_null=True,
        default=0,
        help_text=_(u'Indice de la tabla en el conjunto de datos, comenzando de cero.'))
    header_row = serializers.IntegerField(
        required=False,
        allow_null=True,
        help_text=_(u'Indice de la fila a usar como cabecera de la tabla comenzando de cero. Por defecto es vacio'))
    dataset = serializers.CharField(
        required=False,
        help_text=_(u'GUID del conjunto de datos asociado a la vista'))
    meta_text = serializers.CharField(
        required=False,
        allow_null=True,
        help_text=_(u'Meta text del recurso.'))
    tags = serializers.CharField(
        required=False,
        allow_null=True,
        help_text=_(u'Tags separados por coma'))

    def to_representation(self, obj):
        answer= super(DataStreamSerializer, self).to_representation(obj)
        self.tryKeysOnDict(answer, 'parameters', obj, ['parameters'])
        return answer

    def validate(self, data):
        guid = data.pop('dataset', None)
        if guid:
            try:
                self.dataset = DatasetDBDAO().get(self.context['request'].user,
                    guid=guid, published=False)
                data['dataset']=Dataset.objects.get(id=self.dataset['dataset_id'])
            except ObjectDoesNotExist:
                # TODO: mejorar errores
                raise exceptions.ValidationError({'dataset':'Dataset no existe'})

            if data['dataset'].last_revision.impl_type not in DATASTREAM_IMPL_VALID_CHOICES:
                # TODO: mejorar errores
                raise exceptions.ValidationError({'dataset':'El tipo de archivo no permite creacion de vistas'})

            if 'table_id' in data:
                table_id = data.pop('table_id')
                data['select_statement'] = SelectStatementBuilder().build(table_id)
                header_row = None
                if 'header_row' in data:
                    header_row = data.pop('header_row')
                data['data_source'] = DataSourceBuilder().build(table_id, header_row,
                    data['dataset'].last_revision_id, 'microsites')

        if 'category' in data and data['category']:
            data['category'] = self.getCategory(data['category']).id


        if 'tags' in data:
            if data['tags']:
                data['tags'] = map(lambda x: {'name':x}, data['tags'].split(','))
            else:
                data.pop('tags')

        data['status'] = StatusChoices.PENDING_REVIEW

        data['language'] = self.context['request'].auth['language']

        return data

    def getDao(self, datastream_revision):
        return DataStreamDBDAO().get(user=self.context['request'].user,
            datastream_revision_id=datastream_revision.id,
            published=False)

    def create(self, validated_data):
        if 'dataset' not in validated_data:
            raise exceptions.ValidationError({'dataset': 'No hay dataset'})

        return self.getDao(DatastreamLifeCycleManager(self.context['request'].user).create(
            **validated_data)
        )

    def update(self, instance, validated_data):
        lcycle = DatastreamLifeCycleManager(self.context['request'].user,
            datastream_id=instance['datastream_id'])
        instance.update(validated_data)
        instance.pop('datastream', None)
        instance.pop('dataset', None)
        instance.pop('user', None)
        instance.pop('status', None)
        instance.pop('parameters', None)
        if 'category' not in instance:
            instance['category'] = instance['category_id']
        return self.getDao(lcycle.edit(changed_fields=validated_data.keys(),
                **instance))

class DataStreamViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, ResourceViewSet):
    queryset = DataStreamDBDAO() 
    serializer_class = DataStreamSerializer
    lookup_field = 'guid'
    data_types = ['ds']
    dao_get_param = 'guid'
    dao_pk = 'datastream_revision_id'
    app = 'microsites'

    @detail_route(methods=['get'], renderer_classes=[
        renderers.BrowsableAPIRenderer,
        renderers.JSONRenderer,
        CSVEngineRenderer,
        XLSNonRedirectEngineRenderer,
        #TSVEngineRenderer,
        XMLEngineRenderer,
        PJSONEngineRenderer,
        AJSONEngineRenderer,])
    def data(self, request, pk=None, format=None,  *args, **kwargs):
        instance = self.get_object()
        DatastreamHitsDAO(instance).add(1)
        if format in ['json', 'pjson', 'ajson'] or not format:
            return self.engine_call(request, 'invoke', format)
        return self.engine_call(request, 'invoke', format, 
            serialize=False, form_class=DatastreamRequestForm,
            download=False)

    @detail_route(methods=['post'])
    def clone(self, request,  *args, **kwargs):
        instance = self.get_object()
        dsr = DatastreamLifeCycleManager(request.user, datastream_id=instance['datastream_id']).clone()
        dsdao = DataStreamDBDAO().get(user=request.user, datastream_revision_id=dsr.id, published=False)
        serializer = self.get_serializer(dsdao)
        return Response(serializer.data)

