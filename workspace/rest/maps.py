from api.v2.visualizations import VisualizationSerializer
from core.daos.visualizations import VisualizationDBDAO
from core.rest.views import ResourceViewSet
from rest_framework.decorators import detail_route, list_route
from workspace.v8.forms import VisualizationRequestForm
from workspace.v8.forms import VisualizationPreviewMapForm


class RestMapViewSet(ResourceViewSet):
    queryset = VisualizationDBDAO()
    serializer_class = VisualizationSerializer
    lookup_field = 'id'
    dao_get_param = 'visualization_revision_id'
    data_types = ['vz']
    dao_pk = 'visualization_revision_id'
    app = 'workspace'
    published = False

    @detail_route(methods=['get'])
    def data(self, request, format=None, *args, **kwargs):
        return self.engine_call( request, 'invoke', format,
            form_class=VisualizationRequestForm,
            serialize=False)

    @list_route(methods=['get'])
    def sample(self, request, format=None, *args, **kwargs):
        return self.engine_call( request, 'preview', format,
            form_class=VisualizationPreviewMapForm,
            serialize=False,
            is_detail=False)
