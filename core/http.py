from django.http import HttpResponse
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models import Q
from core.choices import (SourceImplementationChoices, 
    SOURCE_IMPLEMENTATION_EXTENSION_CHOICES,
    SOURCE_IMPLEMENTATION_MIMETYPE_CHOICES)
from core.models import Account

class JSONHttpResponse(HttpResponse):
    """ A custom HttpResponse that handles the headers for our JSON responses """
    #TODO move to CORE
    def __init__(self, content):
        """ Set the headers of the response and assign it a value """
        HttpResponse.__init__(self, content)
        self['Content-Type'] = 'application/json;charset=utf-8'

def get_domain_with_protocol(app, protocol = 'http'):
    return protocol + '://' + settings.DOMAINS[app]

def get_domain(account_id):
    account = Account.objects.get(pk=account_id)
    protocol = 'https' if account.get_preference('account.microsite.https') else 'http'
    account_domain = account.get_preference('account.domain')
    account_domain = '{}://{}'.format(protocol, account_domain)
    return account_domain

def get_domain_by_request(request, default_domain = ''):
    domain = request.META.get('HTTP_HOST', None)
    if domain is None:
        domain = request.META.get('SERVER_NAME', None)
        if domain is None:
            domain = default_domain
    return domain

def gravatar_url(email, size):
    import urllib
    import hashlib
    email_hash = hashlib.md5(email.lower()).hexdigest()
    #default_image = urllib.quote(settings.MEDIA_URI + settings.GRAVATAR['default_image'], safe='')
    default_image = urllib.quote(settings.GRAVATAR['default_image'], safe='')
    return settings.GRAVATAR['url'] % (email_hash, size, default_image)

def add_domains_to_permalinks(resources):
    from core.models import Preference
    accounts_ids = [ item['account_id'] for item in resources ]
    seen = set()
    seen_add = seen.add
    accounts_ids = [ x for x in accounts_ids if x not in seen and not seen_add(x)]
    accounts_domains = Preference.objects.values_list('account_id', 'value', 'key').filter(Q(key='account.domain') | Q(key='account.name'), account__in = accounts_ids)

    r = {}
    for account_id, value, key in accounts_domains:
        if r.has_key(account_id):
            r[account_id][key] = value
        else:
            r[account_id] = {key: value}

    for resource in resources:
        account_id = resource['account_id']
        if r.has_key(account_id):
            account = Account.objects.get(pk=account_id)
            msprotocol = 'https' if account.get_preference('account.microsite.https') else 'http'
            account_domain = r[account_id]['account.domain']
            resource['permalink'] = msprotocol + '://' + account_domain + resource['permalink']
            resource['account_name'] = r[account_id]['account.name']

def get_file_type_from_extension(extension):
    for source_id, extensions in SOURCE_IMPLEMENTATION_EXTENSION_CHOICES:
        if extension in extensions:
            return source_id

def get_impl_type(mimetype, end_point, old_impl_type=None):
    
    if old_impl_type:
        try:
            return int(old_impl_type)
        except ValueError:
            pass

    mimetype = mimetype.split(';')[0]
    
    for source_id, mimetypes in SOURCE_IMPLEMENTATION_MIMETYPE_CHOICES:
        if mimetype in mimetypes:
            return source_id

    extension = end_point.split('/')[-1].split('.')[-1]
    return get_file_type_from_extension(extension)
