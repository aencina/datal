from django.conf import settings
from django.forms.formsets import formset_factory
from rest_framework.response import Response
from core.v8.factories import AbstractCommandFactory
from core.v8.forms import RequestFormSet, RequestForm
from core.v8.serializers import EngineSerializer
from django.http import HttpResponse
from core import choices

from core.lib.elastic import ElasticsearchIndex
import urllib2
import logging
import time


logger = logging.getLogger(__name__)

class EngineViewSetMixin(object):
    def get_default_parameters(self, request):
        instance = self.get_object()
        answer = {}
        if 'parameters' in instance:
            for parameter in instance['parameters']:
                argument = "pArgument%d" % parameter['position']
                if not request.GET.get(argument, None):
                    answer[argument] = parameter['default']
        return answer

    def get_max_rows(self, request):
        preferences = request.auth['preferences']
        if not preferences:
            return settings.MAX_ROWS_BY_REQUEST

        max_rows = preferences['account.api.maxrowsbyrequest']
        if max_rows is None or max_rows == '':
            return settings.MAX_ROWS_BY_REQUEST
        return max_rows

    def update_timestamp(self, response, resource):
        doubts = [
            'is_file' in resource,
            resource['is_file'],
            'collect_type' in resource,
            resource['collect_type'] == choices.CollectTypeChoices.URL,
            self.dao_pk == 'datastream_revision_id'
        ]
        if all(doubts):
            if type(response) == type({}) and "fTimestamp" in response.keys():
                timestamp=response['fTimestamp']
            else:
                timestamp=int(round(time.time() * 1000))

            try:
                es = ElasticsearchIndex()
                doc_id = es.search(doc_type="ds", query={ "query": { "match": {"revision_id": resource['revision_id']}}}, fields="_id")['hits']['hits'][0]['_id']
                es.update({'doc': {'fields': {'timestamp': timestamp}}, 'docid': doc_id, 'type': "ds"})
            except IndexError:
                pass
            except Exception as e:
                logger.warning('[ENGINE COMMAND] error desconocido %s ' % str(e))



    def engine_call(self, request, engine_method, format=None, is_detail=True, 
                    form_class=RequestForm, serialize=True, download=True, 
                    limit=False):
        mutable_get = request.GET.copy()
        mutable_get.update(request.POST.copy())
        mutable_get['output'] = 'json'
        if format is not None:
            format = 'prettyjson' if format == 'pjson' else format
            format = 'json_array' if format == 'ajson' else format
            format = 'json' if format == 'jsonp' else format
            mutable_get['output'] = format 

        if limit:
            max_rows = int(self.get_max_rows(request))
            param_rows = mutable_get.get('limit', None)
            if max_rows > 0 and (not param_rows or int(param_rows) <= 0 or int(param_rows) > max_rows):
                mutable_get['limit'] = max_rows
             
        resource = {}
        if is_detail:
            resource = self.get_object()
            mutable_get['revision_id'] = resource[self.dao_pk]
            mutable_get.update(self.get_default_parameters(request))

        items = dict(mutable_get.items())
        
        formset=formset_factory(form_class, formset=RequestFormSet)
        form = formset(items)
        if not form.is_valid():
            logger.info("form errors: %s" % form.errors)
            # TODO: correct handling
            raise Exception("Wrong arguments")        

        command = AbstractCommandFactory(self.app).create(engine_method, 
            self.data_types[0], form.cleaned_data)
        result = command.run()
        if not result:
            # TODO: correct handling
            raise Exception('Wrong engine answer')

        
        resource['result'] = result[0] if result[0] else {}
        resource['format'] = result[1]

        if serialize:
            serializer = self.get_serializer(resource)
            return Response(serializer.data)

        serializer = EngineSerializer(resource, 
            context={'dao_filename': self.dao_filename})

        if download and 'redirect' in serializer.data and serializer.data['redirect']:
            response = HttpResponse(content_type='application/force-download')
            filename = serializer.data['filename']
            # UGLY HOTFIX
            # ENGINE SEND SOMETHING LIKE 
            ### Nivel_Rendimiento_anio_2008.xlsx?AWSAccessKeyId=AKIAI65****H2VI25OA&Expires=1452008148&Signature=u84IIwXrpIoE%3D
            filename2 = filename.split('?AWSAccessKeyId')[0]
            #TODO get the real name (title) or someting nice
            
            response['Content-Disposition'] = 'attachment; filename="{0}"'.format(filename2)
            redir = urllib2.urlopen(serializer.data['result']['fUri'])
            status = redir.getcode()
            resp = redir.read()
            url = redir.geturl()
            if settings.DEBUG: logger.info('REDIR %d %s -- %s -- %s -- %s' % (status, url, redir.info(), filename, filename2))
            response.write(resp)
            return response

        response = Response(serializer.data['result'], content_type=resource['format'])
        
        #TODO hacer una lista de los formatos que esperan forzar una descarga y los que se mostraran en pantalla
        output = mutable_get['output']
        if download and output not in ['json', 'html']: 
            # reemplazar la extension si la tuviera
            filename = serializer.data['filename']
            name = filename if len(filename.split('.')) == 1 else '.'.join(filename.split('.')[:-1])
            final_filename = '{}.{}'.format(name, output)
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(final_filename)
            

        # Si es un recurso, trato de guardar el timestamp si corresponde
        if is_detail and format == 'json':
            self.update_timestamp(response, resource)

        return response
