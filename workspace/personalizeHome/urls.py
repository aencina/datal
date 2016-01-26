from django.conf.urls  import patterns, url

urlpatterns = patterns('',   
    url(r'^save/$', 'workspace.personalizeHome.views.save', name='personalizeHome.save'),
    url(r'^suggest/$', 'workspace.personalizeHome.views.suggest', name='personalizeHome.suggest'),
    url(r'^upload/$', 'workspace.personalizeHome.views.upload', name='personalizeHome.upload'),
    url(r'^deleteFiles/$', 'workspace.personalizeHome.views.deleteFiles', name='personalizeHome.deleteFiles'),
   
)
