from rest_framework.decorators import detail_route
from django.utils.translation import ugettext_lazy as _
from rest_framework.response import Response
from rest_framework_extensions.cache.decorators import cache_response
from core.rest.cache import CacheKeyConstructor

class ResourceHitsMixin(object):

    @detail_route(methods=['get'])
    @cache_response(60 * 60, cache_errors=False, key_func=CacheKeyConstructor())
    def hits(self, request, *args, **kwargs):

        hits_dao = self.hits_dao_class(self.get_object())
        channel_type = self.request.query_params.get('channel_type', None)
        hits = hits_dao.count_by_days(30, channel_type)
        ans = []
        ans.append([unicode(_('REPORT-CHART-DATE')),
                       unicode(_('REPORT-CHART-TOTAL_HITS'))])
        ans.extend([[item['fecha'], item['hits']] for item in list(hits)])
        return Response({ 'chart':ans })