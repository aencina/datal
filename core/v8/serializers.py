from django.conf import settings
from rest_framework import serializers
import logging
import json

logger = logging.getLogger(__name__)

class EngineSerializer(serializers.Serializer):

    def get_filename(self, obj, engine_result=None, redirect=False):
        # busco nombre original
        filename = None
        dao_filename = self.context['dao_filename']
        if dao_filename in obj:
            filename = obj[dao_filename].split('/')[-1:][0].encode('utf-8')
    
        # busco segunda opcion
        filename2 = None
        redirect_to = ''
        if redirect:
            redirect_to = engine_result.get('fUri')
            filename2 = redirect_to.split('/')[-1:][0].encode('utf-8')
            extension = redirect_to.split('.')[-1:][0]
        
        # evitar ugly names en las referencias locales a nuestro datastore
        if filename2 and filename2.startswith('temp_') and filename:
            # el filename origina puede ser un CSV y esta una descarga de XLSX. Asegurarse
            # la extension real
            name = filename if len(filename.split('.')) == 1 else '.'.join(filename.split('.')[:-1])
            filename2 = '{}.{}'.format(name, extension)

        if settings.DEBUG: 
            logger.info('Redirect %s %s' % (redirect_to, filename))
            if filename2: logger.info('Redirect f2 %s %s' % (redirect_to, filename2))
        
        return filename2 or filename

    def to_representation(self, obj):
        if 'result' in obj:
            json_data =  None
            redirect = False
            if ('format' in obj and obj['format'].startswith('application/json') and obj['result']):
                json_data = json.loads(obj['result'])
                redirect = isinstance(json_data, dict) and json_data.get('fType') == 'REDIRECT'
            
            filename = self.get_filename(obj, json_data, redirect)
            
            return {'result': json_data or obj['result'], 
                    'redirect': redirect, 
                    'filename': filename 
            }
        return {}