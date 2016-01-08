# coding=utf-8
import re
import json

from django.views.decorators.http import require_POST
from django.utils.translation import ugettext
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import HttpResponse
from django.template.loader import render_to_string
from django.core.exceptions import ValidationError

from core.auth.decorators import login_required, privilege_required
from core.http import get_domain_with_protocol
from core.communitymanagers import FinderManager
from core.lib.datastore import *
from workspace.personalizeHome.managers import ThemeFinder
from core.builders.themes import ThemeBuilder

from core.models import Category

# Éste es usado para traer la variable de SETTINGS que necesito en el template HTML
#from core.shortcuts import render_to_response

# Éste ya estaba acá, si comento éste y descomento la anterior, da error en el metodo suggest.
from django.shortcuts import render_to_response
from django.template import RequestContext


@login_required
@privilege_required('workspace.can_access_admin')
@csrf_exempt
def load(request):
    """
    Vista de configuración de página de inicio
    :param request:
    :return:
    """
    auth_manager = request.auth_manager
    account = auth_manager.get_account()
    preference = account.get_preferences()
    stats = request.stats
    jsonContent = preference["account_home"]
    language = request.auth_manager.language
    home_tab = True

    # arlington theme (8) need categories
    # incluye las cuentas federadas
    federated_accounts_ids = [x['id'] for x in account.account_set.values('id').all()]
    categories = Category.objects.get_for_home(language, federated_accounts_ids+[account.id])

    return render_to_response('personalizeHome/index.html', locals(), context_instance=RequestContext(request))


@login_required
@privilege_required('workspace.can_access_admin')
@csrf_exempt
@require_POST
def save(request):
    """
    Vista de configuración de página de inicio. Método POST
    :param request:
    :return:
    """
    if request.method == 'POST':
        account = request.auth_manager.get_account()
        jsonContent = request.POST.get('jsonString')
        jsonObj = json.loads(jsonContent)
        preferences = account.get_preferences()
        if jsonObj['type'] == 'save':
            if jsonObj['theme'] is None:
                preferences['account.has.home'] = False
            else:
                preferences['account.has.home'] = True
            account.set_preference('account.home', jsonContent)
            return HttpResponse(json.dumps({
                'status': 'ok',
                'messages': [ugettext('APP-PREFERENCES-SAVESUCCESSFULLY-TEXT')]}), content_type='application/json')
        else:
            account = request.account
            msprotocol = 'https' if account.get_preference('account.microsite.https') else 'http'
            previewHome = msprotocol + '://' + preferences['account_domain']+'/home?preview=true'
            preferences['account.preview'] = jsonContent
            return HttpResponse(json.dumps({'preview_home':previewHome}), content_type='application/json')


@login_required
@csrf_exempt
def suggest(request):
    account = request.user.account
    preferences = account.get_preferences()
    language = request.auth_manager.language

    builder = ThemeBuilder(preferences, False, language, account)
    data = builder.parse()

    if data['federated_accounts_ids']:
        federated_accounts = data['federated_accounts']
        account_id = data['federated_accounts_ids']+[account.id]
    else:
        account_id = account.id

    query = request.GET.get('term', '')
    ids = request.GET.get('ids', '')
    resources = request.GET.getlist('resources[]', None)
    fm = FinderManager(ThemeFinder)

    if query:
        results, time, facets = fm.search(account_id=account_id, query=query, resource=resources)
        # optionally shows extra info
        # results.append({"extras": {"query": fm.get_finder().last_query, "time": time, "facets": facets}})
    elif ids:
        results, time, facets = fm.search(account_id=account_id, ids=ids, resource=resources)
    else:
        results = ''
    data = render_to_response('personalizeHome/suggest.json', {'objects': results})

    return HttpResponse(data,  content_type='application/json')


@csrf_exempt
def upload(request):
    value = ''
    for filename, file in request.FILES.iteritems():
        valuelist = request.FILES.getlist(filename)
        for val in valuelist:
            data = val
            name = data.name

            accountid = str(request.auth_manager.account_id)
            keyname = "%s/%s" % (accountid, name)

            active_datastore.upload(settings.AWS_CDN_BUCKET_NAME, name, data, str(request.auth_manager.account_id))
            value = get_domain_with_protocol('cdn') + '/' + keyname

    if request.FILES is None:
        response_data = [{"error": 'Must have files attached!'}]
        return HttpResponse(json.dumps(response_data))
    if request.method == 'POST':
        is_ie = False
        if request.META.has_key('HTTP_USER_AGENT'):
            user_agent = request.META['HTTP_USER_AGENT']
            pattern = "msie [1-9]\."
            prog = re.compile(pattern, re.IGNORECASE)
            match = prog.search(user_agent)
            if match:
                is_ie = True
        if is_ie:
            return HttpResponse(json.dumps({"url": value}),  content_type='text/plain')
        else:
            return HttpResponse(json.dumps({"url": value}),  content_type='application/json')


@csrf_exempt
def deleteFiles( request ):
    if request.method == 'POST':
            try:
                accountid = str(request.auth_manager.account_id)
                jsonContent = request.POST['deleteFilenames']
                jsonObj = json.loads(jsonContent)

                bucket = active_datastore.get_bucket(settings.AWS_CDN_BUCKET_NAME)

                if type(jsonObj) is list:
                    for fileName in jsonObj:
                        keyname = "%s/%s" %(accountid[::-1], fileName)
                        bucket.delete_key(keyname)
                if type(jsonObj) is str:
                        keyname = "%s/%s" %(accountid[::-1], fileName)
                        bucket.delete_key(keyname)
                response = {'status': 'ok', 'messages': [ugettext('APP-PREFERENCES-SAVESUCCESSFULLY-TEXT')]}
            except ValidationError, err:
                response = {'status': 'error', 'messages': [ugettext('ADMIN-HOME-DELETE-MESSAGE')]}

            return HttpResponse(json.dumps(response), mimetype='application/json');
