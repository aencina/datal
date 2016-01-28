from django.conf.urls import patterns, url
from workspace.manageVisualizations.views import *
from workspace.manageDataviews.views import filter as filterDatastreams


urlpatterns = patterns(
    '',
    url(r'^$', index, name='manageVisualizations.index'),
    url(r'^filter_datastream/$', filterDatastreams, name='manageDatastream.filter'),
    url(r'^create/$', create, name='manageVisualizations.create'),
    url(r'^(?P<revision_id>\d+)/$', view, name='manageVisualizations.view'),
    url(r'^remove/(?P<type>[a-z]+)/(?P<visualization_revision_id>\d+)/$', remove, name='manageVisualizations.remove'),
    url(r'^remove/(?P<visualization_revision_id>\d+)/$', remove, name='manageVisualizations.remove'),
    url(r'^change_status/(?P<visualization_revision_id>\d+)/$', change_status, name='manageVisualizations.change_status'),
    url(r'^filter/$', filter, name='manageVisualizations.filter'),
    url(r'^retrieve_childs/$', retrieve_childs, name='manageVisualizations.retrieve_childs'),
    url(r'^edit/$', edit, name='manageVisualizations.edit'),
    url(r'^edit/(?P<revision_id>\d+)/$', edit, name='manageVisualizations.edit'),
    url(r'^filters.json/$', get_filters_json, name='manageVisualizations.get_filters'),
)
