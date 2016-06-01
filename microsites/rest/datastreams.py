from rest_framework.decorators import detail_route
from core.daos.datastreams import DataStreamDBDAO, DatastreamHitsDAO
from core.v8.serializers import EngineSerializer
from core.rest.views import ResourceViewSet
from core.v8.forms import DatastreamRequestForm, UpdateGridRequestForm
from rest_framework import renderers
from core.v8.renderers import (CSVEngineRenderer, XLSEngineRenderer, 
                               HTMLEngineRenderer, GridEngineRenderer, 
                               FlexEngineRenderer)
from core.rest.mixins import ResourceHitsMixin
from core.rest.renderers import UTF8JSONRenderer

class RestDataStreamViewSet(ResourceHitsMixin, ResourceViewSet):
    queryset = DataStreamDBDAO() 
    serializer_class = EngineSerializer
    lookup_field = 'id'
    data_types = ['ds']
    dao_get_param = 'datastream_revision_id'
    dao_pk = 'datastream_revision_id'
    app = 'microsites'
    hits_dao_class = DatastreamHitsDAO
    
    @detail_route(methods=['get'], renderer_classes=[
        UTF8JSONRenderer,
        renderers.BrowsableAPIRenderer,
        CSVEngineRenderer,
        FlexEngineRenderer,
        XLSEngineRenderer,
        HTMLEngineRenderer,
        GridEngineRenderer])
    def data(self, request, format=None, *args, **kwargs):
        if format == 'grid':
            return self.engine_call( request, 'invoke', 'json',
                form_class=UpdateGridRequestForm,
                serialize=False, limit=True)   
        return self.engine_call( request, 'invoke', format,
            form_class=DatastreamRequestForm,
            serialize=False,
            limit=format in ['json', 'pjson', 'ajson', 'jsonp'] or not format)
