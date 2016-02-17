from django.core.urlresolvers import reverse
from django.db import connection
from django.http import HttpResponse, Http404
from django.utils.translation import ugettext
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from core.auth.decorators import login_required, privilege_required
from core.decorators import threshold
from core.choices import TicketChoices, StatusChoices, AccountRoles
from core.models import *
from core.shortcuts import render_to_response
from core.lib.mail import mail
from core.lib.datastore import *
from core.http import get_domain_with_protocol
from workspace.manageAccount import forms
from core.utils import generate_ajax_form_errors

import random
import logging
import json
from uuid import uuid4
import urllib
import re


@login_required
@privilege_required('workspace.can_access_admin')
def edit_info(request):
    account = request.auth_manager.get_account()
    keys = [
        'account.name', 
        'account.link',
        'account.contact.person.name',
        'account.contact.person.email',
        'account.contact.person.phone', 
        'account.contact.person.country',
        'account.contact.dataperson.email'
    ]

    form = forms.AccountInfoForm(initial=get_initial(account, keys))
    account_info = True
    return render_to_response('admin_manager/info.html', locals())


@login_required
@privilege_required('workspace.can_access_admin')
@require_POST
@csrf_exempt
def edit_info_update(request):

    form = forms.AccountInfoForm(request.POST)
    if form.is_valid():
        account = request.auth_manager.get_account()

        preferences = {}
        form_fields_keys = form.fields.keys()
        for field_key in form_fields_keys:
            key = field_key.replace('_', '.')
            value = form.cleaned_data[field_key]
            account.set_preference(key, value)

        return HttpResponse(json.dumps({'status': 'ok', 'messages': [ugettext('APP-SETTINGS-SAVE-OK-TEXT')]}), content_type='application/json')

    else:
        errors = generate_ajax_form_errors(form)
        response = {'status': 'error', 'messages': errors}
        return HttpResponse(json.dumps(response), content_type='application/json', status=400)


@login_required
@privilege_required('workspace.can_access_admin')
def index_users(request):
    auth_manager = request.auth_manager
    preferences = auth_manager.get_account().get_preferences()
    roles = AccountRoles.ALL
    form = forms.UserForm(roles)
    users = User.objects.values('id', 'name', 'nick', 'last_visit', 'email', 'roles__name', 'roles__code').filter(
        account=auth_manager.account_id, roles__code__in=roles).all()
    users = [ user for user in users if user['roles__code'] in roles ]
    return render_to_response('admin_manager/users.html', locals())


@login_required
@privilege_required('workspace.can_access_admin')
@threshold("workspace.create_user_limit")
@require_POST
def create_user(request):
    logger = logging.getLogger(__name__)
    roles = AccountRoles.ALL
    form = forms.UserForm(roles, request.POST)
    if form.is_valid():
        auth_manager = request.auth_manager

        user = User.objects.create(
            account_id=auth_manager.account_id,
           name=form.cleaned_data['name'],
           nick=form.cleaned_data['username'],
           email=form.cleaned_data['email'],
           language=auth_manager.language
        )

        role_code = form.cleaned_data['role']
        role = Role.objects.get(code=role_code)
        user.roles.add(role)

        # to activate the user
        user_pass_ticket = UserPassTickets.objects.create(
            uuid=unicode(uuid4()),
            user=user,
            type=TicketChoices.USER_ACTIVATION
        )

        account = auth_manager.get_account()
        preferences = account.get_preferences()

        company = preferences['account_name']
        domain = settings.WORKSPACE_URI

        link = domain + reverse('accounts.activate') + '?' + urllib.urlencode({'ticket': user_pass_ticket.uuid})
        language = auth_manager.language

        logger.debug('[list_subscribe] %s', user)
        country = preferences['account.contact.person.country']
        extradata = {'country': country, 'company': company}

        # Suscribirlo a la lista de usuarios del workspace (si tiene servicio)
        if mail.mail_service:
            if settings.SUBSCRIBE_NEW_USERS_TO_MAIL_LIST:
                mail.mail_service.list_subscribe(user, language, extradata)
        
            # Enviarle el email de bienvenida
            mail.mail_service.send_welcome_mail(user, link, company)
        else: # necesita el codigo de activacion al menos, lo redirijo alli
            response = {'status': 'ok', 
                        'messages': [ugettext('APP-USER-CREATEDSUCCESSFULLY-TEXT'), 'Activar en %s' % link],
                        'redirect': link}
            return HttpResponse(json.dumps(response), content_type='application/json')

        response = {'status': 'ok', 'messages': [ugettext('APP-USER-CREATEDSUCCESSFULLY-TEXT')]}
        return HttpResponse(json.dumps(response), content_type='application/json')
    else:
        errors = generate_ajax_form_errors(form)
        response = {'status': 'error', 'messages': errors}
        return HttpResponse(json.dumps(response), content_type='application/json', status = 400)


@login_required
@privilege_required('workspace.can_access_admin')
@require_POST
def edit_user(request):
    roles = AccountRoles.ALL
    form = forms.UserForm(roles, request.POST)
    if form.is_valid():
        auth_manager = request.auth_manager
        user = User.objects.get(id=form.cleaned_data['id'], account=auth_manager.account_id)

        user.name = form.cleaned_data['name']
        user.nick = form.cleaned_data['username']
        user.email = form.cleaned_data['email']
        user.save()

        user.roles.clear()
        role_code = form.cleaned_data['role']
        role = Role.objects.get(code=role_code)
        user.roles.add(role)

        response = {'status': 'ok', 'messages': [ugettext('APP-USER-UPDATEDSUCCESSFULLY-TEXT')]}
        return HttpResponse(json.dumps(response), content_type='application/json')
    else:
        errors = generate_ajax_form_errors(form)
        response = {'status': 'error', 'messages': errors}
        return HttpResponse(json.dumps(response), content_type='application/json', status = 400)


@login_required
@privilege_required('workspace.can_access_admin')
def edit_branding(request):
    account = request.auth_manager.get_account()
    preferences = account.get_preferences()
    keys = [
        'account.page.titles', 
        'account.header.uri', 
        'account.header.height', 
        'account.footer.uri', 
        'account.footer.height', 
        'account.favicon',
        'account.title.color', 
        'account.button.bg.color', 
        'account.button.border.color', 
        'account.button.font.color', 
        'account.mouseover.bg.color', 
        'account.mouseover.border.color', 
        'account.mouseover.title.color', 
        'account.mouseover.text.color', 
        'account.header.bg.color', 
        'account.header.border.color',
        'account.logo'
    ]

    form = forms.AccountBrandingForm(initial=get_initial(account, keys))
    updateCache = random.random()
    branding = True
    return render_to_response('admin_manager/branding.html', locals())


@login_required
@privilege_required('workspace.can_access_admin')
@require_POST
@csrf_exempt
def edit_branding_update(request):
    logger = logging.getLogger(__name__)
    form = forms.AccountBrandingForm(request.POST)

    if form.is_valid():
        urls = {}
        account = request.auth_manager.get_account()
        form_fields_keys = form.fields.keys()
        form_fields_keys.remove('account_favicon')
        form_fields_keys.remove('account_logo')

        for field_key in form_fields_keys:
            key = field_key.replace('_', '.')
            value = form.cleaned_data[field_key]
            account.set_preference(key, value)

        accountid = str(request.auth_manager.account_id)
            
        if request.FILES.has_key('account_favicon'):
            data = request.FILES['account_favicon']
            keyname = 'favicon'
            active_datastore.upload(settings.AWS_CDN_BUCKET_NAME, keyname, data, account_id=accountid)
            value = '{}/{}/{}'.format(get_domain_with_protocol('cdn'), accountid, keyname)
            account.set_preference('account.favicon', value)
            urls['id_account_favicon'] = value

        if request.FILES.has_key('account_logo'):
            data = request.FILES['account_logo']
            keyname = 'logo'
            active_datastore.upload(settings.AWS_CDN_BUCKET_NAME, keyname, data, account_id=accountid)
            value = '{}/{}/{}'.format(get_domain_with_protocol('cdn'), accountid, keyname)
            account.set_preference('account.logo', value)
            urls['id_account_logo'] = value

        is_ie = False
        if request.META.has_key('HTTP_USER_AGENT'):
            user_agent = request.META['HTTP_USER_AGENT']
            pattern = "msie [1-9]\."
            prog = re.compile(pattern, re.IGNORECASE)
            match = prog.search(user_agent)
            if match:
                is_ie = True

        if is_ie:
            return HttpResponse(json.dumps({'status': 'ok', 'messages': [ugettext('APP-SETTINGS-SAVE-OK-TEXT')], 'urls': urls}), content_type='text/plain')
        else:
            return HttpResponse(json.dumps({'status': 'ok', 'messages': [ugettext('APP-SETTINGS-SAVE-OK-TEXT')], 'urls': urls}), content_type='application/json')
    else:
        errors = generate_ajax_form_errors(form)
        response = {'status': 'error', 'messages': errors}
        return HttpResponse(json.dumps(response), content_type='application/json', status=400)


@login_required
@privilege_required('workspace.can_access_admin')
def edit_social(request):
    account = request.auth_manager.get_account()
    preferences = account.get_preferences()
    keys = ['account.comments', 'enable.embed.options', 'account.enable.sharing', 'account.enable.notes', 'account.dataset.download']
    form = forms.AccountSocialForm(initial=get_initial(account, keys))
    social = True
    return render_to_response('admin_manager/social.html', locals())


@login_required
@privilege_required('workspace.can_access_admin')
@require_POST
def edit_social_update(request):

    form = forms.AccountSocialForm(request.POST)
    if form.is_valid():
        account = request.auth_manager.get_account()

        for field_key in form.fields.keys():
            key = field_key.replace('_', '.')
            value = form.cleaned_data[field_key]
            value = value and value or ''
            account.set_preference(key, value)

        return HttpResponse(json.dumps({'status': 'ok', 'messages': [ugettext('APP-SETTINGS-SAVE-OK-TEXT')]}), content_type='application/json')
    else:
        errors = generate_ajax_form_errors(form)
        response = {'status': 'error', 'messages': errors}
        return HttpResponse(json.dumps(response), content_type='application/json', status = 400)


@login_required
@privilege_required('workspace.can_access_admin')
def edit_domain(request):
    default_domain = '.' + settings.DOMAINS['microsites']
    account = request.auth_manager.get_account()
    preferences = account.get_preferences()
    keys = ['account.domain', 'account.api.domain', 'account.transparency.domain']

    initial=get_initial(account, keys)

    if initial['account_domain'].endswith(default_domain):
        initial['pick_a_domain'] = 'internal'
        initial['account_domain_internal'] = initial['account_domain'].replace(default_domain, '')
    else:
        initial['pick_a_domain'] = 'external'
        initial['account_domain_external'] = initial['account_domain']

    form = forms.AccountDomainForm(initial)
    return render_to_response('admin_manager/domain.html', locals())


@login_required
@privilege_required('workspace.can_access_admin')
@require_POST
def edit_domain_update(request):

    form = forms.AccountDomainForm(request.POST)
    if form.is_valid():
        account = request.auth_manager.get_account()

        for field_key in ['account_domain', 'account_api_domain', 'account_transparency_domain']:
            key = field_key.replace('_', '.')
            value = form.cleaned_data[field_key]
            account.set_preference(key, value)

        return HttpResponse(json.dumps({
            'status': 'ok',
            'messages': [ugettext('APP-SETTINGS-SAVE-OK-TEXT')]
        }), content_type='application/json')
    else:
        errors = generate_ajax_form_errors(form)
        response = {'status': 'error', 'messages': errors}
        return HttpResponse(json.dumps(response), content_type='application/json', status = 400)


@login_required
@privilege_required('workspace.can_access_admin')
def index_categories(request):
    logger = logging.getLogger(__name__)
    auth_manager = request.auth_manager
    account = auth_manager.get_account()
    preferences = account.get_preferences()
    form = forms.CategoryEditForm()
    categories = Category.objects.values('id', 'categoryi18n__name', 'categoryi18n__description').filter(
        account=auth_manager.account_id,
        categoryi18n__language=auth_manager.language
    )
    categories_tab = True

    # for block the "delete" button on transparency categories
    used_transparency_categories = preferences['account.transparency.categories'].split()

    try: default_category = int(preferences['account.default.category'])
    except: default_category = None
    return render_to_response('admin_manager/categories.html', locals())


@login_required
@privilege_required('workspace.can_access_admin')
@require_POST
def create_categories(request):
    form = forms.CategoryCreateForm(request.POST)
    if form.is_valid():
        auth_manager = request.auth_manager
        category_name = form.cleaned_data['name']
        # check for duplicates in this account
        duplicated = CategoryI18n.objects.filter(name=category_name, category__account__id=auth_manager.account_id)
        if len(duplicated) > 0:
            errors = [ugettext('ERROR-DUPLICATED-CATEGORY')]
            response = {'status': 'error', 'messages': errors}
            return HttpResponse(json.dumps(response), content_type='application/json', status = 400)

        category = Category.objects.create(account_id=auth_manager.account_id)
        categoryi18n = CategoryI18n.objects.create(
            category=category,
            name=category_name,
            description=form.cleaned_data['description'],
            language=auth_manager.language
        )

        is_default = form.cleaned_data['is_default']
        account = auth_manager.get_account()
        if is_default:
            account.set_preference('account.default.category', category.id)

        response = {'status': 'ok', 'messages': [ugettext('APP-CATEGORY-CREATEDSUCCESSFULLY-TEXT')]}
        return HttpResponse(json.dumps(response), content_type='application/json')
    else:
        errors = generate_ajax_form_errors(form)
        response = {'status': 'error', 'messages': errors}
        return HttpResponse(json.dumps(response), content_type='application/json', status = 400)


@login_required
@privilege_required('workspace.can_access_admin')
def edit_categories(request):
    form = forms.CategoryEditForm(request.POST)
    if form.is_valid():
        auth_manager = request.auth_manager
        account = auth_manager.get_account()
        category_id = form.cleaned_data['id']

        # check if it's a transparency category
        used_transparency_categories = account.get_preference('account.transparency.categories').split()
        if category_id in used_transparency_categories:
            response = {'status': 'error', 'messages': [ugettext('APP-CATEGORY-TRANSPARENCY-CANT-BE-EDITED')]}
            return HttpResponse(json.dumps(response), content_type='application/json', status=400)

        categoryi18n = CategoryI18n.objects.get(category_id = category_id
                                                , category__account = auth_manager.account_id
                                                , language = auth_manager.language)
        categoryi18n.name = form.cleaned_data['name']
        categoryi18n.description = form.cleaned_data['description']
        categoryi18n.save()

        # reindexing
        reindex_category_resources(category_id, auth_manager.language)

        is_default = form.cleaned_data['is_default']

        try:
            default_category = int(account.get_preference('account.default.category'))
        except:
            default_category = None
        if is_default:
            account.set_preference('account.default.category', category_id)
        elif default_category == category_id:
            response = {'status': 'error', 'messages': [ugettext('APP-CATEGORY-UPDATED-DEFAULT-FAIL')]}
            return HttpResponse(json.dumps(response), content_type='application/json', status=400)

        response = {'status': 'ok', 'messages': [ugettext('APP-CATEGORY-UPDATEDSUCCESSFULLY-TEXT')]}
        response['id'] = categoryi18n.category_id
        return HttpResponse(json.dumps(response), content_type='application/json')
    else:
        errors = generate_ajax_form_errors(form)
        response = {'status': 'error', 'messages': errors}
        return HttpResponse(json.dumps(response), content_type='application/json', status=400)


@login_required
@privilege_required('workspace.can_access_admin')
@require_POST
def delete_categories(request):
    logger = logging.getLogger(__name__)
    form = forms.CategoryDeleteForm(request.POST)
    if form.is_valid():
        auth_manager = request.auth_manager
        category_id = form.cleaned_data.get('id')
        account = auth_manager.get_account()
        try:
            default_category_id = int(account.get_preference('account.default.category'))
        except:
            # si no hay categoria por defecto entonces no se pueden eliminar estos recursos, no tenemos a
            # que categoria cambiarlos
            response = {'status': 'error', 'messages': [ugettext('APP-CATEGORY-DEFAULT-UNDEFINED')]}
            return HttpResponse(json.dumps(response), content_type='application/json', status=400)
            
        if category_id != default_category_id:

            # check if it's a transparency category
            used_transparency_categories = account.get_preference('account.transparency.categories').split()
            if category_id in used_transparency_categories:
                response = {'status': 'error', 'messages': [ugettext('APP-CATEGORY-TRANSPARENCY-CANT-BE-DELETED')]}
                return HttpResponse(json.dumps(response), content_type='application/json', status=400)

            # moving the resources to the default category
            datasets_to_update = DatasetRevision.objects.filter(category=category_id)
            datastreams_to_update = DataStreamRevision.objects.filter(category=category_id)

            if settings.DEBUG: logger.info('Resources to update %s %s' % (str(datasets_to_update), str(datastreams_to_update)))
            
            total = datastreams_to_update.update(category=default_category_id)
            total += datasets_to_update.update(category=default_category_id)

            # reindexing
            if total > 0:
                reindex_category_resources(default_category_id, auth_manager.language)

            # actually, deleting the category
            cat = Category.objects.get(pk=category_id)
            cat.delete()

        else:
            response = {'status': 'error', 'messages': [ugettext('APP-CATEGORY-DEFAULT-CANT-BE-DELETED')]}
            return HttpResponse(json.dumps(response), content_type='application/json', status=400)

        response = {'status': 'ok', 'messages': [ugettext('APP-CATEGORY-DELETEDSUCCESSFULLY-TEXT')], 'total': total, 'category_id':category_id}
        return HttpResponse(json.dumps(response), content_type='application/json')
    else:
        errors = generate_ajax_form_errors(form)
        response = {'status': 'error', 'messages': errors}
        return HttpResponse(json.dumps(response), content_type='application/json', status = 400)


@require_POST
def check_email(request):
    email = request.POST.get('email')
    user_id = request.POST.get('user_id')
    query = User.objects.filter(email=email)
    if user_id:
        query = query.exclude(id=user_id)
    return HttpResponse(str(not query.exists()).lower(), content_type='application/json')


@require_POST
def check_username(request):
    nick = request.POST.get('nick')
    user_id = request.POST.get('user_id')
    query = User.objects.filter(nick=nick)
    if user_id:
        query = query.exclude(id=user_id)
    return HttpResponse(str(not query.exists()).lower(), content_type='application/json')


@require_POST
def check_domain(request):
    account_id = request.auth_manager.account_id
    domain = request.POST.get('domain')
    exists = Preference.objects.filter(key='account.domain', value=domain).exclude(account_id=account_id).exists()
    return HttpResponse(str(not exists).lower(), content_type='application/json')


def get_initial(account, keys):
    """ change dots for underscores in a set of given preferences """
    preferences = account.get_preferences()
    backup_keys = list(keys)
    preferences.load(keys)

    initial = {}
    for key in backup_keys:
        key = key.replace('.', '_')
        initial[key] = preferences[key]
    return initial


def set_preferences(account, preferences):
    for key, value in preferences.items():
        account.set_preference(key, value)

#####################################################
# creo que todo esto deberia ser refactoreado para que
# se use el lifecycle en vez de hablar con el indexador
# de forma directa
from core.lifecycle.datasets import DatasetSearchDAOFactory
from core.lifecycle.datastreams import DatastreamSearchDAOFactory


# Para que se le pasa el language?
def reindex_category_resources(category_id, language):
    """ reindex all resurce using given category """
    logger = logging.getLogger(__name__)
    
    if settings.DEBUG:
        logger.info('Reindexing category resources %d, %s' % (category_id, language))
    
    datasets = Dataset.objects.filter(last_published_revision__category_id=category_id, last_published_revision__status=StatusChoices.PUBLISHED)
    datastreams = DataStream.objects.filter(last_published_revision__category_id=category_id, last_published_revision__status=StatusChoices.PUBLISHED)

    for dataset in datasets:
        datasetrevision=dataset.last_published_revision
        search_dao = DatasetSearchDAOFactory().create(datasetrevision)
        search_dao.add()
    for datastream in datastreams:
        datastreamrevision=datastream.last_published_revision
        search_dao = DatastreamSearchDAOFactory().create(datastreamrevision)
        search_dao.add()

@login_required
@privilege_required('workspace.can_access_admin')
def create_test_datasets(request, quantity=10):
    from core.lifecycle.datasets import DatasetLifeCycleManager
    quantity = int(quantity)
    info = '<h2>Creating %d datasets</h2>' % quantity
    #define any existent category
    account_id = request.auth_manager.account_id
    category = Category.objects.filter(account_id = account_id).order_by('-id')[0]
    category_id = category.id
    
    logger = logging.getLogger(__name__)
    logger.error("Categoy %d" % category_id)
    user = User.objects.get(pk=request.user.id)

    for x in range(0, quantity):
        dt = DatasetLifeCycleManager(user=user)
        typec = choices.CollectTypeChoices.SELF_PUBLISH
        typefile = choices.SourceImplementationChoices.CSV
        newdataset = dt.create(title='Datset %d' % x, collect_type=typec, description="Descripcion del dataset %d" % x,
                               end_point="/home/junar/Downloads/file-%d.csv" % x, notes='',
                               file_name="resource-%d.csv" % x, category=category_id, impl_type=typefile)
        info += '<br />Created Dataset %d' % x
    return HttpResponse(info)
