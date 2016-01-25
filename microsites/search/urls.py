from django.conf.urls import *
from microsites.search.views import *

urlpatterns = patterns('',
    url(r'^category/(?P<category>.*)/$', search_by_query_and_category,
        name='search.search_by_query_and_category'),
    url(r'^$', search, name='search.search'),
)
