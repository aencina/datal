from django.conf.urls import *

urlpatterns = patterns(
    '',
    url(r'^create/$', 'workspace.manageMyAccount.views.create', name='accounts.create'),
    url(r'^activate/$', 'workspace.manageMyAccount.views.activate', name='accounts.activate'),
    url(r'^check_admin_url/$', 'workspace.manageMyAccount.views.check_admin_url', name='accounts.check_admin_url'),
    url(r'^my_account/$', 'workspace.manageMyAccount.views.my_account', name='accounts.my_account'),
)
