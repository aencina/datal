from django.conf.urls import patterns, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import routers
from core.utils import include_notroot_plugins

from core.plugins_point import DatalPluginPoint
from api.v2.datastreams import DataStreamViewSet
from api.v2.datasets import DataSetViewSet
from api.v2.visualizations import VisualizationViewSet
from api.v2.resources import APIResourceViewSet

router = routers.DefaultRouter()
router.register(r'resources', APIResourceViewSet, base_name='resources')
router.register(r'datastreams', DataStreamViewSet, base_name='datastreams')
router.register(r'datasets', DataSetViewSet, base_name='datasets')
router.register(r'visualizations', VisualizationViewSet, base_name='visualizations')

# Implemento los routers que tenga el plugin
plugins = DatalPluginPoint.get_plugins()
for plugin in plugins:
    if plugin.is_active() and hasattr(plugin, 'api_routers'):
        for router_list in plugin.api_routers:
            router.register(router_list[0], router_list[1], base_name=router_list[2])


urlpatterns = patterns('',
    (r'^api/v2/', include(router.urls)),
    (r'^', include_notroot_plugins(DatalPluginPoint, urls='root_api_urls')),
)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
