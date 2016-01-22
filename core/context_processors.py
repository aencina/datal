from django.conf import settings


def request_context(request):
    d = {'auth_manager': request.auth_manager}
    
    my_settings = {
        'BASE_URI' : settings.BASE_URI,
        'API_URI' : settings.API_URI,
        'API_KEY' : settings.API_KEY,
        'VERSION_JS_CSS': settings.VERSION_JS_CSS,
        'WORKSPACE_URI': settings.WORKSPACE_URI,
        'DOMAINS': settings.DOMAINS,
        'DOC_API_URL': settings.DOC_API_URL,
        'APPLICATION_DETAILS': settings.APPLICATION_DETAILS,
        'MSPROTOCOL': 'http',
        'APIPROTOCOL': 'http',
    }

    if hasattr(request, 'account'):
        account = request.account
        msprotocol = 'https' if account.get_preference('account.microsite.https') else 'http'
        apiprotocol = 'https' if account.get_preference('account.api.https') else 'http'
        my_settings['MSPROTOCOL'] = msprotocol
        my_settings['APIPROTOCOL'] = apiprotocol
        
    d['settings'] = my_settings
    d['preference'] = request.preferences
    if hasattr(request, 'stats'):
        d['stats'] = request.stats

    print d
    return d
