from django.conf.urls import *
from workspace.viewLandingPage.views import *

urlpatterns = patterns('',
    url(r'^load/$', load, name='viewLandingPage.load')
)