from django.conf import settings
from django.http import HttpResponse, Http404
from django.views.decorators.clickjacking import xframe_options_exempt
from core.helpers import RequestProcessor
from core.choices import ChannelTypes
from core.models import *
from core.daos.datastreams import DataStreamDBDAO
from core.daos.visualizations import VisualizationDBDAO
from core.http import get_domain_with_protocol
from core.shortcuts import render_to_response
from core.daos.visualizations import VisualizationHitsDAO
from django.template import loader, Context
from core.v8.factories import AbstractCommandFactory
from core.exceptions import *
from microsites.exceptions import *

import urllib
import json

def view(request, id, slug=None):
    """
    Show a microsite view
    """
    account = request.account

    preferences = request.preferences

    try:
        visualization_revision = VisualizationDBDAO().get(
            preferences['account_language'],
            visualization_id=id,
            published=True
        )

        # verify if this account is the owner of this viz
        visualization = Visualization.objects.get(pk=id)
        if account.id != visualization.user.account.id:
            raise NotAccesVisualization

        #for datastream sidebar functions (downloads and others)
        datastream = DataStreamDBDAO().get(
            preferences['account_language'],
            datastream_revision_id=visualization_revision["datastream_revision_id"]
        )
        
    except VisualizationRevision.DoesNotExist:
        raise VisualizationRevisionDoesNotExist
    else:
        VisualizationHitsDAO(visualization_revision).add(ChannelTypes.WEB)

        visualization_revision_parameters = RequestProcessor(request).get_arguments(visualization_revision["parameters"])

        chart_type = json.loads(visualization_revision["impl_details"]).get('format').get('type')

        visualization_revision_parameters = urllib.urlencode(visualization_revision_parameters)

        notes = visualization_revision['notes']

        return render_to_response('viewChart/index.html', locals())


@xframe_options_exempt
def embed(request, guid):
    """
    Show an embed microsite view
    """
    account = request.account
    preferences = request.preferences
    msprotocol = 'https' if account.get_preference('account.microsite.https').lower() == 'true' else 'http'
    base_uri = msprotocol + '://' + preferences['account_domain']

    try:
        visualization_revision = VisualizationDBDAO().get(
            preferences['account_language'], published=True, guid=guid )

        datastream = DataStreamDBDAO().get(
            preferences['account_language'],
            datastream_revision_id=visualization_revision["datastream_revision_id"]
        )
    except:
        return render_to_response('viewChart/embed404.html',{'settings': settings, 'request' : request})

    #VisualizationHitsDAO(visualization_revision.visualization).add(ChannelTypes.WEB)
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

def visualization_error_404(request,id):
    raise VisualizationRevisionDoesNotExist
