from django.template import Context, Template
from django.conf import settings
import json
import csv
import logging 
logger = logging.getLogger(__name__)


class DefaultAnswer(Template):
    """ 
    respuesta predeterminada con status (bool) + messages (list)
    puede usar campos extras
    """
    
    def __init__(self, template="defaul_answer.json"):
        tmpl = "{%% include '%s' %%}" % template
        super(DefaultAnswer, self).__init__(tmpl)

    def render(self, status=True, messages=[], extras=[]):
        data = {"status": status, "messages": messages, "extras": extras}
        context = {"data": data}
        ctx = Context(context)
        return super(DefaultAnswer, self).render(ctx)

class DefaultDictToJson(Template):
    """ 
    entregar un diccionario como Json como respuesta. 
    No usa realmente la clase <Template>
    No se requiere un template, se deslpiega el contenido del 
        diccionario (o una version normalizada {status: true|false, data: CONTENIDO})
    """

    def __init__(self):
        super(DefaultDictToJson, self).__init__("")
    
    def render(self, data, normalize=False):
        """ render dictionario. Normalize es para enviar status y data con el contenido"""
        
        if normalize:
            context = {"status": True, "data": data}
        else:
            context = data
        
        try:
            response = json.dumps(context)
        except Exception, e:
            error = "Invalida JSON parse error: %s " % str(e)
            logger.error(error)
            data = {"status": False, "messages": [error]}
            response = DefaultAnswer().render(status=False, messages=[error])

        return response
