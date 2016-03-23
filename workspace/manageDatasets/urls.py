from django.conf.urls import patterns, url

from workspace.manageDatasets.views import *

urlpatterns = patterns(
    '',
    url(r'^$', index, name='manageDatasets.index'),
    url(r'^(?P<revision_id>\d+)/$', view, name='manageDatasets.view'),
    url(r'^create/$', list, name='manageDatasets.create'),
    url(r'^create/(?P<collect_type>[a-z0-9]+)/$', create, name='manageDatasets.create_type'),
    url(r'^edit/$', edit, name='manageDatasets.edit'),
    url(r'^edit/(?P<dataset_revision_id>\d+)/$', edit, name='manageDatasets.edit'),
    url(r'^filter/$', filter, name='manageDatasets.filter'),
    url(r'^filters.json/$', get_filters_json, name='manageDatasets.get_filters'),
    url(r'^remove/(?P<type>[a-z]+)/(?P<dataset_revision_id>\d+)/$', remove, name='manageDatasets.remove'),
    url(r'^remove/(?P<dataset_revision_id>\d+)/$', remove, name='manageDatasets.remove'),
    url(r'^retrieve_childs/$', retrieve_childs, name='manageDatasets.retrieve_childs'),
    url(r'^change_status/(?P<dataset_revision_id>\d+)/$', change_status, name='manageDatasets.change_status'),
    url(r'^download_file/$', download_file, name='manageDatasets.download_file'),
    url(r'^check_endpoint_url/$', check_endpoint_url, name='check_endpoint_url'),
    url(r'^(?P<revision_id>\d+)/get_childs/$', get_childs, name='manageDatasets.dataset.get_childs'),
)
