from django.core.paginator import EmptyPage, InvalidPage, Paginator
from django.conf import settings
from django.http import Http404
from core.shortcuts import render_to_response
from core.models import Category
from microsites.search import forms
from microsites.managers import *
from microsites.exceptions import *
from core.exceptions import *
from microsites.exceptions import *
from core.plugins_point import DatalPluginPoint


import logging


def action_browse(request, category_slug=None, page=1):
    logger = logging.getLogger(__name__)
    logger.error('action_browse')


def browse(request, category_slug=None, page=1):
    account = request.account
    preferences = request.preferences

    category = Category.objects.get_for_browse(category_slug, account.id, preferences['account_language'])
    accounts_ids =  [x['id'] for x in account.account_set.values('id').all()] + [account.id]

    try:
        results, search_time, facets = FinderManager().search(category_id=category['id'], account_id=[account.id]+accounts_ids)
    except InvalidPage:
        raise InvalidPage

    paginator = Paginator(results, settings.PAGINATION_RESULTS_PER_PAGE)
    page_results = paginator.page(page).object_list

    return render_to_response('search/search.html', locals())


def search(request, category=None):
    account = request.account
    preferences = request.preferences
    form = forms.SearchForm(request.GET)

    if form.is_valid():
        query = form.get_query()
        page = form.cleaned_data.get('page')
        order = form.cleaned_data.get('order')
        reverse = form.cleaned_data.get('reverse')
        resource = form.cleaned_data.get('resource')

        all_resources = ["dt", "ds", "vz"]
        all_resources.extend([finder.doc_type for finder in DatalPluginPoint.get_active_with_att('finder')])

        # si no se pasa resource o es cualquier cosa
        # utiliza el all_resources
        if not resource or resource not in all_resources:
            
            # en caso de que la preferencia este en False, se excluye el DT
            if not account.get_preference("account.dataset.show"):
                all_resources.remove("dt")
            resource=all_resources
        # no puede buscar por dt si account.dataset.show == False
        elif resource == "dt" and not account.get_preference("account.dataset.show"):
            raise InvalidPage

        try:
            meta_data= json.loads(form.cleaned_data.get('meta_data'))
        except ValueError:
            meta_data=None

        accounts_ids = [x['id'] for x in account.account_set.values('id').all()] + [account.id]

        try:
            results, search_time, facets = FinderManager().search(
                query=query, account_id=accounts_ids, category_filters=category, order=order,
                resource=resource, reverse=reverse, meta_data=meta_data
            )
        except InvalidPage:
            raise InvalidPage

        paginator = Paginator(results, settings.PAGINATION_RESULTS_PER_PAGE)

        try:
            page_results = paginator.page(page).object_list
        except EmptyPage:
            page_results = []

        pref_search_tips = preferences['account_search_tips']
        if pref_search_tips: 
            search_tips = json.loads(pref_search_tips)
        else:
            search_tips = {}

        return render_to_response('search/search.html', locals())
    else:
        raise Http404
