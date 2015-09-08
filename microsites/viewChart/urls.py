from django.conf.urls import *
from microsites.viewChart.views import *

urlpatterns = patterns('',
    url(r'^(?P<id>\d+)/(?P<slug>[A-Za-z0-9\-]+)/$', 'microsites.viewChart.views.action_view', name='chart_manager.action_view'),

    url(r'^(?P<id>\d+)-(?P<slug>[A-Za-z0-9\-]+).download$', 'core.downloadDatastream.views.download', name='datastream_manager.download'),
    url(r'^(?P<id>\d+)-(?P<slug>[A-Za-z0-9\-]+).csv$', 'core.exportDataStream.views.action_csv', name='datastream_manager.csv'),
    url(r'^(?P<id>\d+)-(?P<slug>[A-Za-z0-9\-]+).html$', 'core.exportDataStream.views.action_html', name='datastream_manager.html'),
    url(r'^(?P<id>\d+)-(?P<slug>[A-Za-z0-9\-]+).xls(?:$|x$)', 'core.exportDataStream.views.action_xls', name='datastream_manager.xls'),
    
    url(r'^invoke$', 'microsites.viewChart.views.action_invoke', name='chart_manager.action_invoke'),

    url(r'^get_last_30_days_visualization/(?P<vz_id>\d+)$', hits_stats, name='chart_manager.get_last_30_days_visualization'),
)
