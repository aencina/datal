from django.conf.urls import patterns, url
from workspace.manageDataviews.views import *
from workspace.manageDatasets.views import filter as filterDataset

urlpatterns = patterns(
    '',
    url(r'^$', index, name='manageDataviews.index'),
    url(r'^(?P<revision_id>\d+)/$', view, name='manageDataviews.view'),
    url(r'^filter/$', filter, name='manageDataviews.filter'),
    url(r'^filters.json/$', get_filters_json, name='manageDataviews.get_filters'),
    url(r'^filter_dataset/$', filterDataset, name='manageDatasets.filter'),
    url(r'^remove/(?P<type>[a-z]+)/(?P<datastream_revision_id>\d+)/$', remove, name='manageDataviews.remove'),
    url(r'^remove/(?P<datastream_revision_id>\d+)/$', remove, name='manageDataviews.remove'),
    url(r'^create/$', create, name='manageDataviews.create'),
    url(r'^edit/$', edit, name='manageDataviews.edit'),
    url(r'^edit/(?P<datastream_revision_id>\d+)/$', edit, name='manageDataviews.edit'),
    url(r'^retrieve_childs/$', retrieve_childs, name='manageDataviews.retrieve_childs'),
    url(r'^change_status/(?P<datastream_revision_id>\d+)/$', change_status, name='manageDataviews.change_status'),
    url(r'^custom_views/$', custom_views, name='manageDataviews.custom_views'),
)
