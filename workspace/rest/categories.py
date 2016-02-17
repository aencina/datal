from core.models import CategoryI18n
from rest_framework import serializers, viewsets

class CategorySerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(source='category.id')

    class Meta:
        model = CategoryI18n
        fields = ('id', 'category_id', 'name', 'slug')

# ViewSets define the view behavior.
class RestCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CategoryI18n.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        queryset = self.queryset.filter(
            language=self.request.auth['language'],
            category__account=self.request.auth['account'])
        return queryset