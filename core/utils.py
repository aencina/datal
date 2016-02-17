from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify as django_slugify
from django.template.defaultfilters import date as _date
from django.db.models.base import ModelState
from django.conf.urls import include, patterns

from core.choices import SOURCE_IMPLEMENTATION_CHOICES
from core.choices import SourceImplementationChoices

import re
import json
import string
import decimal

validate_comma_separated_word_list = RegexValidator(
    re.compile('^[\w,]+$'), _(u'Enter only words separated by commas.'), 
    'invalid')



def include_notroot_plugins(point, pattern=r'{plugin}/', urls='urls'):
    pluginurls = []
    for plugin in point.get_plugins():
        if hasattr(plugin, urls) and hasattr(plugin, 'name'):
            _urls = getattr(plugin, urls)
            for url in _urls:
                url.default_args['plugin'] = plugin.name
            pluginurls.append(('', include(_urls) ))
    return include(patterns('', *pluginurls))

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'strftime'):
            return string.capitalize(_date(obj, 'F d, Y, h:i A'))
        elif isinstance(obj, decimal.Decimal):
            return float(obj)
        elif isinstance(obj, ModelState):
            return None
        else:
            return json.JSONEncoder.default(self, obj)


def slugify(value):
    value = django_slugify(value)
    value = value.replace('_', '-')
    value = re.sub('[^a-zA-Z0-9]+', '-', value.strip())
    value = re.sub('\-+', '-', value)
    value = re.sub('\-$', '', value)
    return value


# Esto solo se usa en un lugar no se si vale la pena que ete aca
def remove_duplicated_filters(list_of_resources):
    removed = dict()
    removed['status_filter'] = set([x.get('status') for x in list_of_resources])
    removed['type_filter'] = set([x.get('impl_type') for x in list_of_resources])
    removed['category_filter'] = set([x.get('category__categoryi18n__name') for x in list_of_resources])
    removed['author_filter'] = set([x.get('dataset__user__nick', '') for x in list_of_resources])
    removed['author_filter'] = removed['author_filter'].union(set([x.get('datastream__user__nick', '') for x in list_of_resources]))
    return removed    


def generate_ajax_form_errors(form):
    errors = []
    for (k,v) in form.errors.iteritems():
        if k != '__all__':
            k = unicode(form.fields[k].label) + ': '
        else:
            k = ''
        errors.append("%s%s" % (k, v))
    return errors