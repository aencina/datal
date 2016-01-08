import logging
import urllib

from django.conf import settings
from django.http import Http404
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy
from django.template import loader, Context
from django.views.decorators.http import require_http_methods
from django.views.decorators.clickjacking import xframe_options_exempt

from core.http import get_domain_with_protocol
from core.models import DataStream, Account, DataStreamRevision
from core.helpers import RequestProcessor
from core.choices import ChannelTypes
from core.daos.datastreams import DatastreamHitsDAO, DataStreamDBDAO
from core.shortcuts import render_to_response
from core.lib.datastore import *
from microsites.viewDataStream import forms


def view(request, id, slug):
    logger = logging.getLogger(__name__)

    account = request.account

    preferences = request.preferences

    datastream = DataStreamDBDAO().get(language= preferences['account_language'], datastream_id=id, published=True)

    url_query = urllib.urlencode(RequestProcessor(request).get_arguments(datastream['parameters']))

    DatastreamHitsDAO(datastream).add(ChannelTypes.WEB)

    notes = datastream['notes']

    return render_to_response('viewDataStream/index.html', locals())

@xframe_options_exempt
def embed(request, guid):
    account = request.account
    preferences = request.preferences
    msprotocol = 'https' if account.get_preference('account.microsite.https') else 'http'
    base_uri = msprotocol + '://' + preferences['account_domain']

    try:
        datastream = DataStreamDBDAO().get(
            preferences['account_language'], guid=guid, published=True )
        parameters_query = RequestProcessor(request).get_arguments(datastream['parameters'])
    except Http404:
        return render_to_response('viewDataStream/embed404.html', {'settings': settings, 'request': request})

    DatastreamHitsDAO(datastream).add(ChannelTypes.WEB)
    end_point = urllib.urlencode(parameters_query)
    header_row = request.REQUEST.get('header_row', False)
    fixed_column = request.REQUEST.get('fixed_column', False)

    return render_to_response('viewDataStream/embed.html', locals())