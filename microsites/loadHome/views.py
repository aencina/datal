from django.core.paginator import Paginator
from django.http import HttpResponse, Http404
from django.views.decorators.http import require_POST, require_GET
from django.core.serializers.json import DjangoJSONEncoder
from django.template import loader, Context
from core.models import *
from core.managers import *
#from core.shortcuts import render_to_response
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.humanize.templatetags.humanize import intcomma

from core.http import add_domains_to_permalinks
from microsites.loadHome.forms import QueryDatasetForm
from core.communitymanagers import *
from microsites.loadHome.managers import HomeFinder
from django.shortcuts import redirect
from django.utils.translation import ugettext
from core.exceptions import *
from microsites.exceptions import *
from core.search.finder import FinderQuerySet
from core.builders.themes import ThemeBuilder
#from django.views.decorators.cache import cache_page

from core.decorators import datal_cache_page, cache_page
import json
import logging

from core.plugins_point import DatalPluginPoint

logger = logging.getLogger(__name__)

@require_GET
#@datal_cache_page(60*5)
def load(request):
    """
    Shows the microsite's home page
    :param request:
    """
    jsonObject = None
    language = request.auth_manager.language
    account = request.account
    preferences = request.preferences
    is_preview = 'preview' in request.GET and request.GET['preview'] == 'true'

    builder = ThemeBuilder(preferences, is_preview, language, request.user)

    resources = ["ds", "vz"]
    resources.extend([finder.doc_type for finder in DatalPluginPoint.get_active_with_att('finder')])

    if account.get_preference("account.dataset.show"):
        resources.append("dt")

    if is_preview or preferences["account_home"]:
        """ shows the home page new version"""
        data = builder.parse()

        if data:

            accounts_ids=data['federated_accounts_ids'] + [account.id]

            finder_manager = FinderManager(HomeFinder)
            queryset = FinderQuerySet(finder_manager, 
                max_results=250, account_id=accounts_ids, resource=resources )

            paginator = Paginator(queryset, 25)
            revisions = paginator.page(1)

            if data['federated_accounts_ids']:
                add_domains_to_permalinks(revisions.object_list)

            context = data.copy()
            context['has_federated_accounts'] = data['federated_accounts_ids'] != []
            context['request'] = request
            context['paginator'] = paginator
            context['revisions'] = revisions
            context['categories'] = Category.objects.get_for_home(language, accounts_ids)

            context['categories_dict'] = {}
            for cat in context['categories']:
                key = str(cat['id'])
                context['categories_dict'][key] = cat['name']

            context['format_str'] = {
                'total': intcomma(finder_manager.finder.count(account.id))
            }
            for resource in resources:
                context['format_str'][resource] = intcomma(finder_manager.finder.count(account.id, resource))

            return render_to_response(data['template_path'], context, context_instance=RequestContext(request))
    
    for redirect_home in DatalPluginPoint.get_active_with_att('redirect_home'):
        redirect_url = redirect_home(preferences)
        if redirect_url:
            return redirect(redirect_url)

    return redirect('/search/')


@require_POST
def update_list(request):
    account         = request.account
    auth_manager    = request.auth_manager
    preferences     = account.get_preferences()
    language        = request.auth_manager.language

    resources = ["ds", "vz"]
    resources.extend([finder.doc_type for finder in DatalPluginPoint.get_active_with_att('finder')])
        
    if account.get_preference("account.dataset.show"):
        resources.append("dt")


    form = QueryDatasetForm(request.POST)
    if form.is_valid():
        query = form.cleaned_data.get('search')
        page = form.cleaned_data.get('page')
        order = form.cleaned_data.get('order')
        order_elastic = None
        if order == "0":
            order_elastic = "title"
        elif order == "1":
            order_elastic = "last"

        order_type = form.cleaned_data.get('order_type')
        reverse = order_type.lower() == 'ascending'

        category_filters = form.cleaned_data.get('category_filters')
        if category_filters:
            category_filters=category_filters.split(",")

        builder = ThemeBuilder(preferences, False, language, request.user)
        data = builder.parse()

        if data['federated_accounts_ids']:

            entity = form.cleaned_data.get('entity_filters')
            if entity:
                accounts_ids = [int(entity)]
            else:
                accounts_ids = data['federated_accounts_ids'] + [account.id]

            typef = form.cleaned_data.get('type_filters')
            if typef:
                if typef in resources:
                    resources = [typef]

            queryset = FinderQuerySet(FinderManager(HomeFinder), 
                query = query,
                max_results = 250,
                account_id = accounts_ids,
                resource = resources,
                category_filters=category_filters,
                order = order_elastic,
                reverse = reverse
            ) 

        else:
            all_resources = form.cleaned_data.get('all')
            if not all_resources:
                resources_type = form.cleaned_data.get('type')
                aux = []
                for resource_name in resources_type.split(','):
                    if resource_name in resources:
                        aux.append(resource_name)

                resources=aux

            queryset = FinderQuerySet(FinderManager(HomeFinder), 
                category_filters= category_filters,
                query=query,
                resource=resources,
                max_results=250,
                order=order_elastic,
                reverse = reverse,
                account_id=account.id
            )

        paginator = Paginator(queryset, 25)

        revisions = paginator.page(page and page or 1)
        if data['federated_accounts_ids']:
            add_domains_to_permalinks(revisions.object_list)
        error = ''

        results = revisions.object_list
    else:
        error = 'Invalid data'
        results=[]
        categories=[]

    t = loader.get_template('loadHome/table.json')
    c = Context(locals())
    return HttpResponse(t.render(c), content_type="application/json")


@require_GET
def update_categories(request):
    language = request.auth_manager.language
    params = request.GET
    account_id = params.get('account_id','')

    # we need a full categories list in case is a "federated account" (have childs accounts)
    if account_id == '':
        account = request.account
        preferences = request.preferences

        builder = ThemeBuilder(preferences, False, language, request.user)
        data = builder.parse()

        if data['federated_accounts_ids']:
            federated_accounts=data['federated_accounts']
    
        categories = data['categories']
    else:
        # account_id is single account or a list of federated accounts
        categories = Category.objects.get_for_home(language, account_id)

    return render_to_response('loadHome/categories.js', locals(), mimetype="text/javascript")
