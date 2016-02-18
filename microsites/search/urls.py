from django.conf.urls import *
from microsites.search.views import *

urlpatterns = patterns('',
    url(r'^category/(?P<category>.*)/$', search,
        name='search.search'),
    url(r'^$', search, name='search.search'),
)
