import logging

from core.primitives import PrimitiveComputer

logger = logging.getLogger(__name__)


class RequestProcessor:

    def __init__(self, request):
        self.request = request

    def get_arguments(self, paramaters):

        args = {}

        for parameter in paramaters:
            key = 'pArgument%d' % parameter['position']
            value = self.request.REQUEST.get(key, '')
            if value == '':
                parameter['value'] = unicode(parameter['default']).encode('utf-8')
                args[key] = parameter['value']
            else:
                parameter['value'] = unicode(value).encode('utf-8')
                args[key] = parameter['value']
                parameter['default'] = parameter['value']

        return args

    def get_arguments_no_validation(self, query = None):
        counter = 0

        if not query:
            args = {}
        else:
            args = dict(query)

        key = 'pArgument%d' % counter
        value = self.request.REQUEST.get(key, None)
        while value:
            args[key] = PrimitiveComputer().compute(value)
            counter += 1
            key = 'pArgument%d' % counter
            value = self.request.REQUEST.get(key, None)
        return args
