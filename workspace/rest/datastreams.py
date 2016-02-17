from rest_framework.decorators import detail_route, list_route
from core.daos.datastreams import DataStreamDBDAO
from api.v2.datastreams import DataStreamSerializer
from core.rest.views import ResourceViewSet
from core.v8.forms import DatastreamRequestForm, UpdateGridRequestForm
from workspace.v8.forms import DatastreamPreviewForm
from rest_framework import renderers
from core.v8.renderers import (CSVEngineRenderer, XLSEngineRenderer, 
                               HTMLEngineRenderer, GridEngineRenderer)

class RestDataStreamViewSet(ResourceViewSet):
    queryset = DataStreamDBDAO() 
    serializer_class = DataStreamSerializer
    lookup_field = 'id'
    data_types = ['ds']
    dao_get_param = 'datastream_revision_id'
    dao_pk = 'datastream_revision_id'
    app = 'workspace'
    published = False
    
    @detail_route(methods=['get'], renderer_classes=[
        renderers.JSONRenderer,
        renderers.BrowsableAPIRenderer,
        GridEngineRenderer])
    def data(self, request, format=None, *args, **kwargs):
        if format == 'grid':
            return self.engine_call( request, 'invoke',
                form_class=UpdateGridRequestForm,
                serialize=False)    
        return self.engine_call( request, 'invoke', 
            form_class=DatastreamRequestForm,
            serialize=False)

    @list_route(methods=['get', 'post'])
    def sample(self, request, format=None, *args, **kwargs):
        return self.engine_call( request, 'preview', 
            form_class=DatastreamPreviewForm,
            serialize=False,
            is_detail=False)
