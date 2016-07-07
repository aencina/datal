import urllib
import json

from django.conf import settings
from django.views.decorators.clickjacking import xframe_options_exempt

from core.helpers import RequestProcessor
from core.choices import ChannelTypes
from core.models import *
from core.daos.datastreams import DataStreamDBDAO
from core.daos.visualizations import VisualizationDBDAO
from core.shortcuts import render_to_response
from core.daos.visualizations import VisualizationHitsDAO
from core.v8.factories import AbstractCommandFactory
from microsites.exceptions import VisualizationRevisionDoesNotExist


def view(request, id, slug=None):
    """
    Show a microsite view
    """
    account = request.account
    preferences = request.preferences

    try:
        visualization_revision = VisualizationDBDAO().get(
            request.user,
            visualization_id=id,
            published=True
        )

        visualization = visualization_revision['visualization']

        # For datastream sidebar functions (downloads and others)
        datastream = DataStreamDBDAO().get(request.user,
            datastream_revision_id=visualization_revision["datastream_revision_id"]
        )

    except VisualizationRevision.DoesNotExist:
        raise VisualizationRevisionDoesNotExist
    else:
        VisualizationHitsDAO(visualization_revision).add(ChannelTypes.WEB)

        visualization_revision_parameters = RequestProcessor(request).get_arguments(visualization_revision["parameters"])

        chart_type = json.loads(visualization_revision["impl_details"]).get('format').get('type')
        if chart_type == 'mapchart':
            geo_type = json.loads(visualization_revision["impl_details"]).get('chart').get('geoType')
        else:
            geo_type = ''

        visualization_revision_parameters = urllib.urlencode(visualization_revision_parameters)

        url_query = urllib.urlencode(RequestProcessor(request).get_arguments(visualization_revision['parameters']))

        notes = visualization_revision['notes']
        if request.GET.get('embedded', False) == 'true':
            return render_to_response('viewChart/embedded.html', locals())
        else:
            return render_to_response('viewChart/index.html', locals())


@xframe_options_exempt
def embed(request, guid):
    """
    Show an embed microsite view
    """
    account = request.account
    preferences = request.preferences
    msprotocol = 'https' if account.get_preference('account.microsite.https') else 'http'
    base_uri = msprotocol + '://' + preferences['account_domain']

    try:
        visualization_revision = VisualizationDBDAO().get(request.user,
            published=True, guid=guid )

        datastream = DataStreamDBDAO().get(request.user,
            datastream_revision_id=visualization_revision["datastream_revision_id"]
        )
    except:
        return render_to_response('viewChart/embed404.html',{'settings': settings, 'request' : request})

    # VisualizationHitsDAO(visualization_revision.visualization).add(ChannelTypes.WEB)
    VisualizationHitsDAO(visualization_revision).add(ChannelTypes.WEB)

    width = request.REQUEST.get('width', False) # TODO get default value from somewhere
    height = request.REQUEST.get('height', False) # TODO get default value from somewhere

    visualization_revision_parameters = RequestProcessor(request).get_arguments(visualization_revision["parameters"])
    visualization_revision_parameters['pId'] = visualization_revision["datastream_revision_id"]

    command = AbstractCommandFactory('microsites').create("invoke",
            "vz", (visualization_revision_parameters,))
    json, type = command.run()
    visualization_revision_parameters = urllib.urlencode(visualization_revision_parameters)

    return render_to_response('viewChart/embed.html', locals())
