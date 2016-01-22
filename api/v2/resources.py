from core.daos.visualizations import VisualizationDBDAO
from api.v2.serializers import ResourceSerializer
from core.rest.views import ResourceViewSet
from django.conf import settings
from rest_framework.exceptions import NotFound

class APIResourceSerializer(ResourceSerializer):
    def to_representation(self, obj):
        answer = super(APIResourceSerializer, self).to_representation(obj)
        answer['type'] = obj['type']
        return answer
                

class APIResourceViewSet(ResourceViewSet):
    serializer_class = APIResourceSerializer
    app = 'microsites'        

    def get_object(self):
        raise NotFound()
