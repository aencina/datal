from django.conf import settings
from django.forms.formsets import formset_factory
from django.http import HttpResponseRedirect, QueryDict, HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext
from core.auth import forms
from core.auth.decorators import login_required
from core.http import gravatar_url
from core.models import *
import urlparse
import json

REDIRECT_FIELD_NAME = 'next'

def redirect_to_login(next, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Redirects the user to the login page, passing the given 'next' page
    """
    if not login_url:
        login_url = settings.LOGIN_URL

    login_url_parts = list(urlparse.urlparse(login_url))
    if redirect_field_name:
        querystring = QueryDict(login_url_parts[4], mutable=True)
        querystring[redirect_field_name] = next
        login_url_parts[4] = querystring.urlencode(safe='/')

    return HttpResponseRedirect(urlparse.urlunparse(login_url_parts))

@login_required
def grant_datastream(request):

    auth_manager = request.auth_manager
    private_datastream_share_form = forms.PrivateDataStreamShareForm(request.POST, prefix='private_share_form')
    collaborator_formset = formset_factory(forms.CollaboratorForm)
    collaborator_forms = collaborator_formset(request.POST, prefix='private_share_form_collaborators')

    if private_datastream_share_form.is_valid() and collaborator_forms.is_valid():
        datastream_id = private_datastream_share_form.cleaned_data['id']

        if not auth_manager.has_privilege_on_object(datastream_id, 'datastream', 'share', request.is_workspace):
            raise Http404

        datastream = get_object_or_404(DataStream, pk=datastream_id, user__account = auth_manager.account_id)

        old_collaborators = []
        for collaborator in ObjectGrant.objects.get_collaborators(datastream_id, 'datastream'):
            collab = {'email': collaborator['email'], 'role': collaborator['role']}
            old_collaborators.append(collab)

        new_collaborators = []
        for collaborator_form in collaborator_forms.forms:
            collab = {'email': collaborator_form.cleaned_data['email'],
                      'role': collaborator_form.cleaned_data['role']}
            new_collaborators.append(collab)

        added = [ collab for collab in new_collaborators if collab not in old_collaborators ]
        deleted = [ collab for collab in old_collaborators if collab not in new_collaborators ]

        for collaborator in deleted:
            ObjectGrant.objects.filter(datastream=datastream, grant__user__email = collaborator['email']).delete()
            # logging
            user = User.objects.get(email = collaborator['email'])
            content = """{"user_nick": "%s", "action": "deleted grant"}""" % user.nick
            Log.objects.create(user_id=auth_manager.id, content=content, datastream_id=datastream_id)

        for collaborator in added:
            role = Role.objects.get(code=collaborator['role'])
            user = User.objects.get(email = collaborator['email'])
            grant, is_new = Grant.objects.get_or_create(user=user, role=role)
            object_grant = ObjectGrant.objects.get_or_create(type='datastream', datastream=datastream, grant=grant)
            # logging
            content = """{"user_nick": "%s", "action": "granted %s"}""" % (user.nick, role.code)
            Log.objects.create(user_id=auth_manager.id, content=content, datastream_id=datastream_id)

    else:
        return HttpResponse('{"pStatus": "ERROR", "pMessage": "'+ugettext("PRIV-SHARE-DS-ERROR")+'"}', content_type='application/json', status=400)

    return HttpResponse('{"pStatus": "OK", "pMessage": "'+ugettext("PRIV-SHARING-UPDATED")+'"}', content_type='application/json')

@login_required
def grant_visualization(request):

    auth_manager = request.auth_manager
    private_visualization_share_form = forms.PrivateVisualizationShareForm(request.POST, prefix='private_share_form')
    collaborator_formset = formset_factory(forms.CollaboratorForm)
    collaborator_forms = collaborator_formset(request.POST, prefix='private_share_form_collaborators')

    if private_visualization_share_form.is_valid() and collaborator_forms.is_valid():
        visualization_id = private_visualization_share_form.cleaned_data['id']
        visualization = get_object_or_404(Visualization, pk=visualization_id, user__account = auth_manager.account_id)

        if not auth_manager.has_privilege_on_object(visualization_id, 'visualization', 'share', request.is_workspace):
            raise Http404

        old_collaborators = []
        for collaborator in ObjectGrant.objects.get_collaborators(visualization_id, 'visualization'):
            collab = {'email': collaborator['email'], 'role': collaborator['role']}
            old_collaborators.append(collab)

        new_collaborators = []
        for collaborator_form in collaborator_forms.forms:
            collab = {'email': collaborator_form.cleaned_data['email'],
                      'role': collaborator_form.cleaned_data['role']}
            new_collaborators.append(collab)

        added = [ collab for collab in new_collaborators if collab not in old_collaborators ]
        deleted = [ collab for collab in old_collaborators if collab not in new_collaborators ]

        for collaborator in deleted:
            ObjectGrant.objects.filter(visualization=visualization, grant__user__email = collaborator['email']).delete()
            # logging
            user = User.objects.get(email = collaborator['email'])
            content = """{"user_nick": "%s", "action": "deleted grant"}""" % user.nick
            Log.objects.create(user_id=auth_manager.id, content=content, visualization_id=visualization_id)

        for collaborator in added:
            role = Role.objects.get(code=collaborator['role'])
            user = User.objects.get(email = collaborator['email'])
            grant, is_new = Grant.objects.get_or_create(user=user, role=role)
            object_grant = ObjectGrant.objects.get_or_create(type='visualization', visualization=visualization, grant=grant)
            # logging
            content = """{"user_nick": "%s", "action": "granted %s"}""" % (user.nick, role.code)
            Log.objects.create(user_id=auth_manager.id, content=content, visualization_id=visualization_id)

    else:
        return HttpResponse('{"pStatus": "ERROR", "pMessage": "'+ugettext("PRIV-SHARE-VZ-ERROR")+'"}', content_type='application/json', status=400)

    return HttpResponse('{"pStatus": "OK", "pMessage": "'+ugettext("PRIV-SHARING-UPDATED")+'"}', content_type='application/json')

def get_email_info(request):
    auth_manager = request.auth_manager
    email_form = forms.EmailForm(request.GET)

    if email_form.is_valid():
        email = email_form.cleaned_data['email']
        image_url = gravatar_url(email, 38)
        response = { 'email': email, 'image_url': image_url}
    else:
        return HttpResponse('{"pStatus": "ERROR", "pMessage": "'+ugettext("PRIV-SHARE-EMAIL-ERROR")+'"}', content_type='application/json', status=400)
    return HttpResponse(json.dumps(response), content_type='application/json')
