import os

from django.conf.urls import *
from django.conf import settings
from django.views.i18n import javascript_catalog

from rest_framework import routers
from djangoplugins.utils import include_plugins

from core.plugins_point import DatalPluginPoint
from workspace.rest.datasets import RestDataSetViewSet
from workspace.rest.datastreams import RestDataStreamViewSet
from workspace.rest.maps import RestMapViewSet
from workspace.rest.charts import RestChartViewSet
from workspace.rest.sources import RestSourceViewSet
from workspace.rest.tags import RestTagViewSet
from workspace.rest.resources import MultipleResourceViewSet
from workspace.rest.categories import RestCategoryViewSet 
from workspace.rest.users import RestUserViewSet 


router = routers.DefaultRouter()
router.register(r'datastreams', RestDataStreamViewSet, base_name='datastreams')
router.register(r'maps', RestMapViewSet, base_name='maps')
router.register(r'charts', RestChartViewSet, base_name='charts')
router.register(r'datasets', RestDataSetViewSet, base_name='datasets')
router.register(r'sources', RestSourceViewSet, base_name='sources')
router.register(r'tags', RestTagViewSet, base_name='tags')
router.register(r'resources', MultipleResourceViewSet, base_name='resources')
router.register(r'categories', RestCategoryViewSet, base_name='categories')
router.register(r'users', RestUserViewSet, base_name='users')

# Implemento los routers que tenga el plugin
plugins = DatalPluginPoint.get_plugins()
for plugin in plugins:
    if plugin.is_active() and hasattr(plugin, 'workspace_routers'):
        for router_list in plugin.workspace_routers:
            router.register(router_list[0], router_list[1], base_name=router_list[2])


def jsi18n(request, packages=None, domain=None):
    if not domain:
        domain = 'djangojs'
    return javascript_catalog(request, domain, packages)

js_info_dict = {
    'domain': 'djangojs',
    'packages': ('workspace'),
}

urlpatterns = patterns('',
    (r'^rest/', include(router.urls)), 
    (r'^', include_plugins(DatalPluginPoint, urls='workspace_urls')),
    (r'^i18n/', include('django.conf.urls.i18n')),
    (r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict),
    url(r'^$', 'workspace.views.home', name='workspace.home'),
    url(r'^signup/$', 'workspace.manageMyAccount.views.signup', name='accounts.signup'),
    # url(r'^signup-free/$', 'workspace.manageMyAccount.views.signup_free', name='accounts.signup_free'),
    url(r'^signout/$', 'workspace.manageMyAccount.views.signout', name='accounts.signout'),
    url(r'^signin/$', 'workspace.manageMyAccount.views.signin', name='accounts.signin'),
    url(r'^welcome/$', 'workspace.viewLandingPage.views.load', name='accounts.landing'),
    url(r'^login/$', 'workspace.manageMyAccount.views.login', name='accounts.login'),
    url(r'^forgot_password/$', 'workspace.manageMyAccount.views.forgot_password', name='accounts.forgot_password'),
    url(r'^recovery/$', 'workspace.manageMyAccount.views.recovery', name='accounts.recovery'),
    url(r'^datasets/', include('workspace.manageDatasets.urls')),

    #TODO fix all urls (streams -> dataviews)
    url(r'^dataviews/', include('workspace.manageDataviews.urls')),
    url(r'^visualizations/', include('workspace.manageVisualizations.urls')),

    # TODO Nacho: Added by Nacho. This should be implemented different. Andres, please review
    (r'^accounts/', include('workspace.manageMyAccount.urls')),
    (r'^viewLandingPage/', include('workspace.viewLandingPage.urls')),
    (r'^admin/', include('workspace.manageAccount.urls')),
    (r'^auth/', include('core.auth.urls')),
    (r'^personalizeHome/', include('workspace.personalizeHome.urls')),
    (r'^js_core/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(settings.PROJECT_PATH, 'core', 'js')}),
    (r'^js_workspace/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(settings.PROJECT_PATH, 'workspace', 'js')}),
    # Please leave me always as the last url pattern
    url(r'^(?P<admin_url>[A-Za-z0-9\-]+)/$', 'workspace.manageMyAccount.views.signin', name='accounts.account_signin'),
)

handler404 = 'core.views.action404'
handler500 = 'core.views.action500'
