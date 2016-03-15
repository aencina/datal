import json

from rest_framework import serializers
from rest_framework.compat import OrderedDict
from core.models import CategoryI18n, Category
import json

class ResourceSerializer(serializers.Serializer):
    def getCategory(self, category_slug):
        return CategoryI18n.objects.get(
            slug=category_slug,
            category__account=self.context['request'].auth['account'],
            language=self.context['request'].auth['language']).category

    def tryKeysOnDict(self, toDict, toKey, fromDict, fromKeys):
        toDict[toKey] = None
        for key in fromKeys:
            if key in fromDict:
                toDict[toKey] = fromDict[key]

    def to_representation(self, obj):
        answer = {}

        self.tryKeysOnDict(answer, 'guid', obj, ['guid'])
        self.tryKeysOnDict(answer, 'title', obj, ['title'])
        self.tryKeysOnDict(answer, 'description', obj, ['description'])
        self.tryKeysOnDict(answer, 'user', obj, ['author', 'owner_nick'])
        self.tryKeysOnDict(answer, 'tags', obj, ['tags'])
        self.tryKeysOnDict(answer, 'created_at', obj, ['created_at'])
        self.tryKeysOnDict(answer, 'endpoint', obj, ['endpoint', 'end_point'])
        self.tryKeysOnDict(answer, 'link', obj, ['permalink'])
        self.tryKeysOnDict(answer, 'category_name', obj, ['category_name'])
        self.tryKeysOnDict(answer, 'parameters', obj, ['parameters'])
        self.tryKeysOnDict(answer, 'result', obj, ['result'])

        try:
            if 'format' in obj and obj['format'].startswith('application/json'):
                answer['result'] = json.loads(answer['result']) 
        except AttributeError:
            # TODO: ver esto, plis
            pass

        if answer['tags']:
            answer['tags'] = map(lambda x: x['tag__name'] if type(x) == dict else x, answer['tags'])

        if answer['link']:
            domain = self.context['request'].auth['microsite_domain']
            answer['link'] = domain + answer['link']
        return OrderedDict(answer)

