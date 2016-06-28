import logging
import urllib

from django.conf import settings
from django.views.decorators.clickjacking import xframe_options_exempt

from core.models import DataStreamRevision
from core.helpers import RequestProcessor
from core.choices import ChannelTypes
from core.daos.datastreams import DatastreamHitsDAO, DataStreamDBDAO
from core.shortcuts import render_to_response
from core.lib.datastore import *


def view(request, id, slug):
    """
    Get a datastream
    :param request:
    :param id:
    :param slug:
    :return:
    """
    logger = logging.getLogger(__name__)

    account = request.account

    preferences = request.preferences

    # parche horrible para usar account_language en vez del language del user
    user = request.user
    user.language = preferences['account_language']

    datastream = DataStreamDBDAO().get(user, datastream_id=id, published=True)

    url_query = urllib.urlencode(RequestProcessor(request).get_arguments(datastream['parameters']))

    DatastreamHitsDAO(datastream).add(ChannelTypes.WEB)

    notes = datastream['notes']
    if request.GET.get('embedded', False) == 'true':
        return render_to_response('viewDataStream/embedded.html', locals())
    else:
        return render_to_response('viewDataStream/index.html', locals())


@xframe_options_exempt
def embed(request, guid):
    """
    Get an embedded datastream
    :param request:
    :param guid:
    :return:
    """
    account = request.account
    preferences = request.preferences
    msprotocol = 'https' if account.get_preference('account.microsite.https') else 'http'
    base_uri = msprotocol + '://' + preferences['account_domain']

    try:
        # parche horrible para usar account_language en vez del language del user
        user = request.user
        user.language = preferences['account_language']

        datastream = DataStreamDBDAO().get(user, guid=guid, published=True )
        parameters_query = RequestProcessor(request).get_arguments(datastream['parameters'])
    except DataStreamRevision.DoesNotExist:
        return render_to_response('viewDataStream/embed404.html', {'settings': settings, 'request': request})

    DatastreamHitsDAO(datastream).add(ChannelTypes.WEB)
    end_point = urllib.urlencode(parameters_query)
    header_row = request.REQUEST.get('header_row', False)
    fixed_column = request.REQUEST.get('fixed_column', False)

    return render_to_response('viewDataStream/embed.html', locals())

