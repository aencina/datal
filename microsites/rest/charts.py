from rest_framework.decorators import detail_route
from core.rest.views import ResourceViewSet
from microsites.v8.forms import VisualizationRequestForm
from core.daos.visualizations import VisualizationDBDAO, VisualizationHitsDAO
from core.v8.serializers import EngineSerializer
from core.rest.mixins import ResourceHitsMixin

class RestChartViewSet(ResourceHitsMixin, ResourceViewSet):
    queryset = VisualizationDBDAO()
    serializer_class = EngineSerializer
    lookup_field = 'id'
    dao_get_param = 'visualization_revision_id'
    data_types = ['vz']
    dao_pk = 'visualization_revision_id' 
    app = 'microsites'
    hits_dao_class = VisualizationHitsDAO

    @detail_route(methods=['get'])
    def data(self, request, format=None, *args, **kwargs):
        return self.engine_call( request, 'invoke', format,
            form_class=VisualizationRequestForm,
            serialize=False)
