from django.conf import settings
from django.forms.formsets import formset_factory
from rest_framework.response import Response
from core.v8.factories import AbstractCommandFactory
from core.v8.forms import RequestFormSet, RequestForm
from core.v8.serializers import EngineSerializer
from django.http import HttpResponse
import urllib2
import logging

logger = logging.getLogger(__name__)

class EngineViewSetMixin(object):
    def engine_call(self, request, engine_method, format=None, is_detail=True, 
                    form_class=RequestForm, serialize=True, download=True):
        mutable_get = request.GET.copy()
        mutable_get.update(request.POST.copy())
        mutable_get['output'] = 'json'
        if format is not None:
            format = 'prettyjson' if format == 'pjson' else format
            format = 'json_array' if format == 'ajson' else format
            mutable_get['output'] = format 
        
        resource = {}
        if is_detail:
            resource = self.get_object()
            mutable_get['revision_id'] = resource[self.dao_pk]
           
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
            response = HttpResponse(mimetype='application/force-download')
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
            
        return response
