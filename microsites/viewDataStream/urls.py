from django.conf.urls import *

urlpatterns = patterns('',
    url(r'^(?P<id>\d+)/(?P<slug>[A-Za-z0-9\-]+)/$', 'microsites.viewDataStream.views.view',
        name='viewDataStream.view'),
    url(r'^embed/(?P<guid>[A-Za-z0-9\-]+)/$', 'microsites.viewDataStream.views.embed',
        name='viewDataStream.embed'),
    url(r'^category/(?P<category_slug>[A-Za-z0-9\-]+)/$', 'microsites.search.views.browse',
        name='search.browse'),
    url(r'^category/(?P<category_slug>[A-Za-z0-9\-]+)/page/(?P<page>\d+)/$', 'microsites.search.views.browse',
        name='search.browse'),
)
