# coding=utf-8
from rest_framework import serializers

from core.choices import VISUALIZATION_LIBS, VISUALIZATION_TYPES, VISUALIZATION_TEMPLATES, BOOLEAN_FIELD, \
    INCLUDE_EXCLUDE, MAP_TYPE_FIELD


class VisualizationSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=80, label='Title', required=True)
    description = serializers.CharField(max_length=250, required=False, label=u'Description')
    notes = serializers.CharField(required=False, label=u'Note')
    type = serializers.ChoiceField(required=True, choices=VISUALIZATION_TYPES)
    chartTemplate = serializers.ChoiceField(required=True, choices=VISUALIZATION_TEMPLATES)
    showLegend = serializers.ChoiceField(required=False, choices=BOOLEAN_FIELD)
    nullValueAction = serializers.ChoiceField(required=False, choices=INCLUDE_EXCLUDE)
    nullValuePreset = serializers.CharField(required=False, max_length=200)
    data = serializers.CharField(max_length=300, required=True)
    xTitle = serializers.CharField(required=False, max_length=200)
    yTitle = serializers.CharField(required=False, max_length=200)
    labelSelection = serializers.CharField(required=False, max_length=200)
    headerSelection = serializers.CharField(required=False, max_length=200)
    lib = serializers.ChoiceField(required=True, choices=VISUALIZATION_LIBS)
    invertData = serializers.ChoiceField(required=False, choices=BOOLEAN_FIELD)
    invertedAxis = serializers.ChoiceField(required=False, choices=BOOLEAN_FIELD)
    correlativeData = serializers.ChoiceField(required=False, choices=BOOLEAN_FIELD)
    is3D = serializers.ChoiceField(required=False, choices=BOOLEAN_FIELD)

    # Mapas
    latitudSelection = serializers.CharField(required=False, max_length=200)
    longitudSelection = serializers.CharField(required=False, max_length=200)
    traceSelection = serializers.CharField(required=False, max_length=200)
    mapType = serializers.ChoiceField(required=False, choices=MAP_TYPE_FIELD)
    geoType = serializers.CharField(required=False, max_length=20)
    zoom = serializers.IntegerField(required=False)
    bounds = serializers.CharField(required=False, max_length=200)

    parameters = serializers.DictField(required=False)

    def create(self, validated_data, datastream_rev=None, visualization_rev=None):
        print (validated_data)
