# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy, ugettext

from core.lifecycle.visualizations import VisualizationLifeCycleManager
from core.choices import VISUALIZATION_LIBS, VISUALIZATION_TYPES, VISUALIZATION_TEMPLATES, BOOLEAN_FIELD, \
    INCLUDE_EXCLUDE, MAP_TYPE_FIELD


class VisualizationForm(forms.Form):
    title = forms.CharField(max_length=80, label=u'Title', required=True)
    description = forms.CharField(max_length=250, required=False, label=u'Description')
    notes = forms.CharField(required=False, label=u'Note')
    type = forms.ChoiceField(required=True, choices=VISUALIZATION_TYPES)
    chartTemplate = forms.ChoiceField(required=True, choices=VISUALIZATION_TEMPLATES)
    showLegend = forms.ChoiceField(required=False, choices=BOOLEAN_FIELD)
    nullValueAction = forms.ChoiceField(required=False, choices=INCLUDE_EXCLUDE)
    nullValuePreset = forms.CharField(required=False, max_length=200)
    data = forms.CharField(max_length=300, required=True)
    xTitle = forms.CharField(required=False, max_length=200)
    yTitle = forms.CharField(required=False, max_length=200)
    labelSelection = forms.CharField(required=False, max_length=200)
    headerSelection = forms.CharField(required=False, max_length=200)
    lib = forms.ChoiceField(required=True, choices=VISUALIZATION_LIBS)
    invertData = forms.ChoiceField(required=False, choices=BOOLEAN_FIELD)
    invertedAxis = forms.ChoiceField(required=False, choices=BOOLEAN_FIELD)
    correlativeData = forms.ChoiceField(required=False, choices=BOOLEAN_FIELD)
    is3D = forms.ChoiceField(required=False, choices=BOOLEAN_FIELD)

    # Mapas
    latitudSelection = forms.CharField(required=False, max_length=200)
    longitudSelection = forms.CharField(required=False, max_length=200)
    traceSelection = forms.CharField(required=False, max_length=200)
    mapType = forms.ChoiceField(required=False, choices=MAP_TYPE_FIELD)
    geoType = forms.CharField(required=False, max_length=20)
    zoom = forms.IntegerField(required=False)
    bounds = forms.CharField(required=False, max_length=200)

    def save(self, request, datastream_rev=None, visualization_rev=None):
        if datastream_rev:
            lifecycle = VisualizationLifeCycleManager(user=request.user)
            visualization_rev = lifecycle.create(datastream_rev, language=request.user.language,  **self.cleaned_data)

            return dict(
                status='ok',
                revision_id=visualization_rev.id,
                messages=[ugettext('APP-VISUALIZATION-CREATEDSUCCESSFULLY-TEXT')]
            )
        elif visualization_rev:
            lifecycle = VisualizationLifeCycleManager(
                user=request.user,
                visualization_revision_id=visualization_rev['visualization_revision_id']
            )
            visualization_rev = lifecycle.edit(
                language=request.auth_manager.language,
                changed_fields=self.changed_data,
                **self.cleaned_data
            )
            return dict(
                status='ok',
                revision_id=visualization_rev.id,
                messages=[ugettext('APP-VISUALIZATION-CREATEDSUCCESSFULLY-TEXT')]
            )


class InitializeChartForm(forms.Form):
    datastream_revision_id = forms.IntegerField(label=ugettext_lazy( 'APP-DATASTREAMREVISION-TEXT' ), required=True)


class ViewChartForm(forms.Form):
    visualization_revision_id = forms.IntegerField(label=ugettext_lazy( 'APP-VISUALIZATIONREVISION-TEXT' ), required=True)


class RequestForm(forms.Form):
    visualization_revision_id = forms.IntegerField(required=False)
    limit = forms.IntegerField(required=False)
    page = forms.IntegerField(required=False)
    bounds = forms.CharField(required=False)
    zoom = forms.IntegerField(required=False)


class PreviewForm(RequestForm):
    type = forms.ChoiceField(required=True, choices=VISUALIZATION_TYPES)
    nullValueAction = forms.CharField(required=True)
    nullValuePreset = forms.CharField(required=False)
    invertData = forms.CharField(required=False)
    invertedAxis = forms.CharField(required=False)
    data = forms.CharField(required=True)
    labels = forms.CharField(required=False)
    headers = forms.CharField(required=False)
    lat = forms.CharField(required=False)
    lon = forms.CharField(required=False)
    traces = forms.CharField(required=False)


class PreviewMapForm(RequestForm):
    nullValueAction = forms.CharField(required=True)
    nullValuePreset = forms.CharField(required=False)

    data = forms.CharField(required=True)
    lat = forms.CharField(required=True)
    lon = forms.CharField(required=True)

    headers = forms.CharField(required=False)
    traces = forms.CharField(required=False)

    bounds = forms.CharField(required=False)
    zoom = forms.IntegerField(required=False)

