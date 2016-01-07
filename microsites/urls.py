import os

from django.conf.urls import *
from django.conf import settings
from django.views.generic import RedirectView

from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from djangoplugins.utils import include_plugins

from core.plugins_point import DatalPluginPoint
from microsites.rest.datastreams import RestDataStreamViewSet
from microsites.rest.maps import RestMapViewSet
from microsites.rest.charts import RestChartViewSet
from microsites.rest.routers import MicrositeEngineRouter
from core.plugins_point import DatalPluginPoint

router = MicrositeEngineRouter()
router.register(r'datastreams', RestDataStreamViewSet, base_name='datastreams')
router.register(r'maps', RestMapViewSet, base_name='maps')
router.register(r'charts', RestChartViewSet, base_name='charts')


# Implemento los routers que tenga el plugin
plugins = DatalPluginPoint.get_plugins()
for plugin in plugins:
    if plugin.is_active() and hasattr(plugin, 'microsites_routers'):
        for router_list in plugin.microsites_routers:
            router.register(router_list[0], router_list[1], base_name=router_list[2])

def jsi18n(request, packages = None, domain = None):
    if not domain:
        domain = 'djangojs'
    from django.views.i18n import javascript_catalog
    return javascript_catalog(request, domain, packages)

js_info_dict = {
    'domain': 'djangojs',
    'packages': ('microsites'),
}

urlpatterns = patterns('',
    (r'^rest/', include(format_suffix_patterns(router.urls))), 
    (r'^', include_plugins(DatalPluginPoint, urls='microsites_urls')),
    (r'^', include_plugins(DatalPluginPoint, urls='advancedfiltering_urls')),
    
    url(r'^$', RedirectView.as_view(pattern_name='loadHome.load')),
    (r'^i18n/', include('django.conf.urls.i18n')),
    (r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict),

    url(r'^a/(\w+)$', 'microsites.views.custom_pages'),

    (r'^visualizations/', include('microsites.viewChart.urls')),
    url(r'^visualizations/embed/(?P<guid>[A-Z0-9\-]+)$', 'microsites.viewChart.views.embed', name='chart_manager.embed'),

    # dejamos datastreams para no romper,
    # dataviews como deberia quedar definitivamente
    (r'^datastreams/', include('microsites.viewDataStream.urls')),
    (r'^dataviews/', include('microsites.viewDataStream.urls')),
    (r'^datasets/', include('microsites.viewDataset.urls')),

    (r'^search/', include('microsites.search.urls')),
    #(r'^search$', include('microsites.search.urls')),
    url(r'^developers/$', 'core.manageDeveloper.views.filter', name='manageDeveloper.filter'),
    url(r'^developers$', 'core.manageDeveloper.views.filter', name='manageDeveloper.filter'),
    url(r'^manageDeveloper/create$', 'core.manageDeveloper.views.create', name='manageDeveloper.create'),
    url(r'^branded/css/(?P<id>\d+).css$', 'microsites.views.get_css', name='microsites.get_css'),
    url(r'^branded/js/(?P<id>\d+).js$', 'microsites.views.get_js', name='microsites.get_js'),
    url(r'^branded/newcss/(?P<id>\d+).css$', 'microsites.views.get_new_css', name='microsites.get_new_css'),

#    url(r'^portal/DataServicesManager/actionEmbed/$', 'microsites.viewDataStream.views.legacy_embed', name='datastream_manager.legacy_embed'),
    url(r'^is_live$', 'microsites.views.is_live', name='microsites.is_live'),
    (r'^home/', include('microsites.loadHome.urls')),
    (r'^home', include('microsites.loadHome.urls')),
    url(r'^catalog.xml$', 'microsites.views.get_catalog_xml'),
    (r'^auth/', include('core.auth.urls')),

    
    (r'^js_core/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(settings.PROJECT_PATH, 'core', 'js')}),
    (r'^js_microsites/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(settings.PROJECT_PATH, 'microsites', 'js')}),

    url(r'^sitemap', 'microsites.home_manager.views.sitemap', name='home_manager.sitemap'),
)

handler404 = 'core.views.action404'
handler500 = 'core.views.action500'
