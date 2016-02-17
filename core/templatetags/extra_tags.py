from django import template
from django.core.urlresolvers import reverse
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from django.utils import simplejson
import hashlib
import urllib
import re
from urlparse import urlparse
from core.choices import AccountRoles, SOURCE_IMPLEMENTATION_CHOICES, COLLECT_TYPE_CHOICES

register = template.Library()


@register.filter(name='split')
@stringfilter
def split(p_source, p_args):
    """
    Split the source string with target and returns left[0] or right side[1]
    Aguments:
    String to be used for splitting the source string
    Side of the source string to be retrieved
    """
    try:
        l_args      = p_args.split(",")
        l_target    = l_args[0]
        l_side      = l_args[1]
        l_name      = p_source.split(l_target, 1)[l_side]
    except ValueError:
        l_name = p_source# Fail silently.

    return l_name


@register.filter(name='md5')
@stringfilter
def md5(p_value):
    try:
        return hashlib.md5(p_value.lower()).hexdigest()
    except:
        return ""


@register.filter(name='truncate')
def truncate(p_value, p_args):
    """
    Truncates a string after a given number of chars
    Argument: Number of chars to truncate after
    """
    try:
        l_length = int(p_args)
    except ValueError: # invalid literal for int()
        return p_value # Fail silently.
    if not isinstance(p_value, basestring):
        p_value = str(p_value)
    if (len(p_value) > l_length):
        return p_value[:l_length] + "..."
    else:
        return p_value


@register.filter(name='twitterUrlEncode')
@stringfilter
def twitterUrlEncode(p_url):
    """encode a url with the twitter format"""
    try:
        return urllib.quote(p_url, safe='')
    except:
        return ""


@register.filter(name='urlEncode')
@stringfilter
def urlEncode(p_url):
    try:
        return urllib.quote(p_url, safe='')
    except:
        return ""


@register.filter(name='unquote')
@stringfilter
def unquote(p_url):
    """unquote a url"""
    try:
        return urllib.unquote(p_url)
    except:
        return ""


@register.filter(name='prepareTagForSearch')
@stringfilter
def prepareTagForSearch(p_tag):
    """decides whether or not quote a tag for search"""
    if re.match('.*\ .*', p_tag):
        return '"'+p_tag+'"'
    else:
        return p_tag


@register.filter(name='truncateUrlLeavingDomain')
@stringfilter
def truncateUrlLeavingDomain(p_url):
    """truncate an url leaving the domain"""
    l_max_length  = 41
    l_parsed_url  = urlparse(p_url)
    l_base_url    = l_parsed_url.scheme + '://' + l_parsed_url.netloc
    l_base_url_len = len(l_base_url)
    if l_base_url_len > l_max_length:
        return l_base_url
    else:
        lMaxLengthForPath = l_max_length - l_base_url_len
        if len(l_parsed_url.path) > lMaxLengthForPath:
            return l_base_url + l_parsed_url.path[:lMaxLengthForPath - 3] + '...'
        else:
            return l_base_url + l_parsed_url.path


@register.filter(name='isGreaterThan')
def isGreaterThan(p_value, p_number):
    """evaluates if the number is greater compared with the parameter"""
    try:
        l_number = int(p_number)
    except ValueError:
        return False

    return p_value > l_number


@register.filter(name='addhttp')
def addhttp(url):
    """ put http:// if is not present in the url """
    if url:
        return url.startswith('http://') and url or 'http://' + url
    else:
        return '#'


@register.filter(name='impl_type_nice')
def impl_type_nice(item):
    """ obtener el nombre desde SOURCE_IMPLEMENTATION_CHOICES """
    impl_type_nice = unicode(SOURCE_IMPLEMENTATION_CHOICES[int(item)][1]).replace('/', '-').replace(' ', '-')

    return impl_type_nice

@register.filter(name='collect_type_nice')
def collect_type_nice(item):
    """ obtener el nombre desde SOURCE_IMPLEMENTATION_CHOICES """
    collect_type_nice = unicode(COLLECT_TYPE_CHOICES[int(item)][1]).replace('/', '-').replace(' ', '-')

    return collect_type_nice


    
@register.simple_tag
def gravatar(auth_manager, size, klass, user_nick=None, user_email=None):
    """ auth_manager param can also be a user object or dict with user nick and email """
    from django.conf import settings
    from core.http import gravatar_url

    if not user_nick:
        email = auth_manager.email
        nick = auth_manager.nick
    else:
        email = user_email
        nick = user_nick

    if not isinstance( size, (int, long)):
        size = settings.GRAVATAR['sizes'][size]
    url = gravatar_url(email, size)
    return '<img src="%s" alt="%s" title="%s" class="%s"/>' % (url, nick, nick, klass)


@register.simple_tag
def account_logo(account, klass, roles):
    preferences = account.get_preferences()
    account_logo = preferences['account_logo']
    account_domain = preferences['account_domain']
    href = ''
    if AccountRoles.ADMIN in roles and account_logo == '':
        account_domain = reverse('admin_manager.edit_info')
    elif AccountRoles.ADMIN in roles and account_domain == '':
        account_domain = reverse('admin_manager.edit_domain')
    elif 'ao-free-user' in roles:
        return ''
    else:
        msprotocol = 'https' if preferences['account.microsite.https'] else 'http'
        account_domain = msprotocol + '://' + account_domain
    account_logo = account_logo and account_logo or '/static/workspace/images/_workspace/im_logoNotDefined.gif'
    account_name = preferences['account_name']
    img_string = '<a title="%s" href="%s"><img src="%s" alt="%s" title="%s" class="%s"/></a>' % (account_name, account_domain, account_logo, account_name, account_name, klass)
    return img_string


@register.filter(name='format')
def format(value, arg):
    try:
        return value % arg
    except:
        return value

import json


@register.filter(name='jsonize')
def jsonize(obj):
    return json.dumps(obj, skipkeys=True, ensure_ascii=False)


@register.filter
def jsonify(o):
    return mark_safe(simplejson.dumps(o))


@register.filter(name='key')
def key(d, key_name):
    return d.get(key_name, "")