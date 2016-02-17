from django.conf.urls import *
from core.auth.views import *

urlpatterns = patterns('',
    url(r'^grant_datastream/$', grant_datastream, name='auth.grant_datastream'),
    url(r'^grant_visualization/$', grant_visualization, name='auth.grant_visualization'),
    url(r'^get_email_info/$', get_email_info, name='auth.get_email_info'),
)
