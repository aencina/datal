# -*- coding: utf-8 -*-
from rest_framework.decorators import detail_route
from core.daos.datasets import DatasetDBDAO
from api.v2.serializers import ResourceSerializer
from core.rest.views import ResourceViewSet
from core.choices import ODATA_LICENSES, ODATA_FREQUENCY, SOURCE_IMPLEMENTATION_CHOICES, SourceImplementationChoices
from core.lifecycle.datasets import DatasetLifeCycleManager
from rest_framework import serializers
from rest_framework import mixins
from rest_framework import exceptions
from django.utils.translation import ugettext_lazy as _
from core.choices import StatusChoices, CollectTypeChoices
from core.forms import MimeTypeForm
from core.http import get_impl_type, get_file_type_from_extension
import urllib


class DataSetSerializer(ResourceSerializer):
    title = serializers.CharField(
        help_text=_(u'Título del conjunto de datos'))
    description = serializers.CharField(
        help_text=_(u'Descripción del conjunto de datos'))
    category = serializers.ChoiceField(tuple(),
        help_text=_(u'Nombre de la categoría para clasificar los recursos. Debe coincidir con alguna de las categorías de la cuenta'))
    notes = serializers.CharField(
        required=False, 
        allow_null=True,
        help_text=_(u'Texto de la nota del conjunto de datos'))
    end_point = serializers.URLField(
        required=False,
        allow_null=True,
        allow_blank=True,
        help_text=_(u'Url apuntando al recurso con los datos (archivos o página web).'))
    file = serializers.FileField(
        allow_null=True,
        required=False,
        help_text=_(u'Archivo a subir a la plataforma'))
    license = serializers.ChoiceField(ODATA_LICENSES,
        allow_null=True, 
        required=False,
        help_text=_(u'Tipo de licencia que aplica sobre el conjunto de datos'))
    spatial = serializers.CharField(
        required=False, 
        allow_null=True,
        help_text=_(u'Zona geográfica a la cual aplica el conjunto de datos'))
    frequency = serializers.ChoiceField(ODATA_FREQUENCY,
        allow_null=True, 
        required=False,
        help_text=_(u'Tipo de licencia que aplica sobre el conjunto de datos'))
    mbox = serializers.EmailField(
        allow_null=True, 
        required=False,
        help_text=_(u'Correo electronico de quien administra el conjunto de datos'))

    def __init__(self, *args, **kwargs):
        super(DataSetSerializer, self).__init__(*args, **kwargs)

        self.fields['category']= serializers.ChoiceField(
            self.getAccountCategoriesChoices(),
            help_text=self.fields['category'].help_text
        )

    def validate(self, data):
        for key, value in data.items():
            if not value:
                data.pop(key)

        if 'category' in data and data['category']:
            data['category'] = self.getCategory(data['category']).id

        if 'end_point' in data and data['end_point']:
            mimetype, status, url = MimeTypeForm().get_mimetype(data['end_point'])
            data['impl_type']  = get_impl_type(mimetype, url)
            if not data['impl_type']:
                data['impl_type'] = SourceImplementationChoices.HTML
            data['collect_type'] = CollectTypeChoices.URL
            data['file_name'] = data['end_point']

        if 'file' in data:
            file_data = data.pop('file')
            file_data.name = urllib.unquote(file_data.name)
            data['file_data'] = file_data
            data['impl_type'] = get_impl_type(file_data.content_type, file_data.name)
            data['collect_type'] = CollectTypeChoices.SELF_PUBLISH

        if ('impl_type' not in data or
            data['impl_type'] is None or 
            data['impl_type'] not in dict(SOURCE_IMPLEMENTATION_CHOICES).keys()):
                # TODO: mejorar errores
                raise exceptions.ValidationError({'impl_type': 'Tipo de Archivo Invalido'})

        if 'license' in data:
            data['license_url'] = data.pop('license')

        data['status'] = StatusChoices.PENDING_REVIEW

        data['language'] = self.context['request'].auth['language']

        return data

    def getDao(self, dataset_revision):
        return DatasetDBDAO().get(
            dataset_revision_id=dataset_revision.id,
            user=self.context['request'].user,
            published=False)

    def create(self, validated_data):
        if 'file_data' not in validated_data and 'end_point' not in validated_data:
            raise exceptions.ValidationError({'description': 'O end_point o file. No puede estar ambas vacias.'})

        return self.getDao(
            DatasetLifeCycleManager(self.context['request'].user).create(**validated_data)
        )

    def update(self, instance, validated_data):
        lcycle = DatasetLifeCycleManager(self.context['request'].user,
            dataset_id=instance['dataset_id'])
        if 'file_data' in validated_data and len(validated_data) == 5: #file and status, impl_type, collect_type, language
            return self.getDao(lcycle.update_file(**validated_data))
        else:
            instance.update(validated_data)
            if 'impl_details' in instance: instance.pop('impl_details')
            return self.getDao(lcycle.edit(changed_fields=validated_data.keys(),
                **instance))

class DataSetViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, ResourceViewSet):
    queryset = DatasetDBDAO()
    serializer_class = DataSetSerializer
    lookup_field = 'guid'
    dao_get_param = 'guid'
    data_types = ['dt']
    app = 'microsites'
