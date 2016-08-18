import json
from django.conf import settings
from core import VERSION

def request_context(request):
    obj = {}
    if hasattr(request, 'account'):
        account = request.account
        path = request.path
        # obj = {'tracking_id': account.get_preference('account.ga.tracking')}
        # ga_obj = account.get_preference('account.ga')

        msprotocol = 'https' if account.get_preference('account.microsite.https') else 'http'
        msdomain = account.get_preference('account.domain')

        # if ga_obj == '':
        #     ga_obj = '{}'
        # if 'visualizations' in path and 'embed' not in path:
        #     if 'dataview_view' in json.loads(ga_obj):
        #         final = {}
        #         final['dataview_view'] = json.loads(ga_obj)['dataview_view']
        #         obj.update({'ga': json.dumps(final)})
        # elif 'datastreams' in path and 'embed' not in path:
        #     if 'dataview_view' in json.loads(ga_obj):
        #         final = {}
        #         final['dataview_view'] = json.loads(ga_obj)['dataview_view']
        #         obj.update({'ga': json.dumps(final)})
        # elif 'search' in path:
        #     if 'search_view' in json.loads(ga_obj):
        #         final = {}
        #         final['search_view'] = json.loads(ga_obj)['search_view']
        #         obj.update({'ga': json.dumps(final)})
        # else:
        #     obj = {}

        if account.get_preference('account.ga.tracking') != '' :
            obj = {'tracking_id': account.get_preference('account.ga.tracking')}

    else: # pragma: no cover.
        # TODO: No se como testear este error.
        msprotocol = 'http' 
        msdomain=settings.DOMAINS['microsites'] 

    obj['account_show_dataset']=account.get_preference('account.dataset.show')
    obj['microsite_domain']=msdomain
    obj['microsite_uri']=msprotocol
    obj['core_version']=VERSION
    return obj

def context_paths(request):
    """ info for headers and footers about where am I and in which language show """
    
    is_home = request.path == '/' or request.path.startswith('/home')
    is_search = request.path.startswith('/search')
    is_developers = request.path.startswith('/developers') # not working (duplicated) reverse('developer_manager.action_query')) 
    is_datastream = request.path.startswith('/datastreams') or request.path.startswith('/dataviews')
    is_visualization = request.path.startswith('/visualizations')
    is_dashboard = request.path.startswith('/dashboards')

    if is_home: path_is='home'
    elif is_search: path_is='search'
    elif is_developers: path_is='developers'
    elif is_datastream: path_is='datastream'
    elif is_visualization: path_is='visualization'
    elif is_dashboard: path_is='dashboard'
    else: path_is='unknown'

    res = {'context_path': path_is}
    
    # read if we're forcing language
    if request.GET.get('locale', None) in dict(settings.LANGUAGES).keys():
        res['force_language'] = request.GET['locale']
        
    return res