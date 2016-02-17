import json
import logging
from core.primitives import PrimitiveComputer

logger = logging.getLogger(__name__)

# Lo comento porque supuestamente no se va a uar mas
# /workspace/managers.py
# /core/managers.py
def next(p_iterator, p_default=None):
    try:
        l_next = p_iterator.next()
    except StopIteration, l_error:
        l_next = p_default

    return l_next

# Se va porque se va a refactorear
# /core/exportDataStream/views.py
def jsonToGrid(p_response, p_page = '', p_limit =''):
    """ p_response is a core.engine.invoke resultset """
    l_lists = {}
    l_hasHeader = False
    l_noMoreHeaders = False

    try:
        p_response = json.loads(p_response)
    except:
        return '{"page": 1, "rows": [], "total":1}'

    l_lists["page"] = p_page
    l_lists["total"] = p_response['fLength']
    l_lists["rows"] = []

    if p_response['fType']=='ARRAY':
        l_i = 0
        l_row_i = 0
        for l_row_number in range(0, p_response['fRows']):
            l_row  = {}
            l_row["id"] = str(l_i)
            l_row["cell"] = []
            for l_column_number in range(0, p_response['fCols']):
                l_cell = p_response['fArray'][l_i]

                # TRANSFORM DE DATA
                l_row["cell"].append(i18nize(l_cell))

                if l_cell.has_key('fHeader') and l_noMoreHeaders == False:
                    l_hasHeader = True
                l_i = l_i + 1

            l_row_i = l_row_i + 1

            if not l_hasHeader:
                l_lists["rows"].append(l_row)
            else:
                l_hasHeader = False
                l_noMoreHeaders = True

    return json.dumps(l_lists)

# Se va porque se va a refactorear
# /api/views.py
# /core/exportDataStream/views.py
# /microsites/exportDataStream/views.py
# /microsites/viewChart/views.py
# /workspace/manageVisualizations/views.py


class RequestProcessor:

    def __init__(self, request):
        self.request = request

    def get_arguments(self, paramaters):

        args = {}

        for parameter in paramaters:
            key = 'pArgument%d' % parameter['position']
            value = self.request.REQUEST.get(key, '')
            if value == '':
                parameter['value'] = parameter['default']
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

















