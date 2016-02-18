from django.template import Context, Template
import json
import datetime
import logging 
logger = logging.getLogger(__name__)


class DataStreamOutputBigDataTemplate(Template):

    def __init__(self, template):
        # add my filters
        template = "%s\n%s\n%s\n" % ("{% load mint_tags %}", "{% load semantic %}", template)
        super(DataStreamOutputBigDataTemplate, self).__init__(template)

    def render(self, contents, request, metadata={}):
        headers = {}
        rows = []
        rows_array = [] = []
        summ = {} # all  columns added
        
        result = json.loads(contents)
        if result['fType']=='ARRAY':
            array = result['fArray']
            index = 0
            for row_number in range(0, result['fRows']):
                row  = {}
                row_array = []
                header = False
                for column_number in range(0, result['fCols']):
                    # take the string value, date or number and just send that
                    dat = array[index]
                    if dat["fType"] == "TEXT":
                        val = dat["fStr"]
                    if dat["fType"] == "NUMBER":
                        val = dat["fNum"]
                    if dat["fType"] == "DATE":
                        try:
                            #return a datetime object
                            val = datetime.datetime.utcfromtimestamp(dat["fNum"] / 1000)
                        except Exception,e:
                            # val = str(dat["fNum"]) + " ERR " + str(e)
                            raise

                    header = dat.get("fHeader", False)
                    
                    if header:
                        headers['column%s' % column_number] = val
                        summ['column%s' % column_number] = 0.0
                    else:
                        #summ function for all fields
                        try:
                            if not summ.get('column%s' % column_number, False): summ['column%s' % column_number] = 0.0
                            summ['column%s' % column_number] = summ['column%s' % column_number] + float(val)
                        except:
                            pass
                        
                    row['column%s' % column_number] = val
                    row['data%s' % column_number] = dat # add extra data in case we need it.
                    row_array.append(val)
                    
                    
                    index = index + 1
                    
                if not header:
                    rows.append(row)
                    rows_array.append(row_array)
                    
        else: # not an ARRAY (?)
            # error ?
            metadata['error'] = 'Result is (%s)' % str(result)            
            result['fRows'] = -1
            result['fCols'] = -1
            
        # extra data
        metadata['summ'] = summ
        metadata['total_rows'] = result.get('fRows', -1)
        metadata['total_cols'] = result.get('fCols', -1)
        metadata['rows_array'] = rows_array
        
        
        # define extra values required
        owner = request.owner
        publisher = request.publisher
        author = request.author
        # JP-17/04/2014 We must define default values for owner, publisher and author that make sense (why /junar.com/cities instead of just simply junar.com/tim os something more generic?)
        # or raise a new Exception called TemplateMissingArgumentsError.
        # retrieve key values using request.GET[key]
        # Pass the KeyError exception as an argument to the constructor.

        try:
            res = super(DataStreamOutputBigDataTemplate, self).render(Context({"rows": rows, "owner": owner, 
                                                                               "publisher": publisher, "author" : author, 
                                                                               "metadata": metadata, "headers": headers}))
        except Exception,e:
            import traceback
            tb = traceback.format_exc()
            self.render_errors = 'ERROR: %s -- TRACE %s' % ( str(e), tb )
            res = False

        return res

class MintTemplateResponse(Template):

    def __init__(self, template='json'): # json or HTML
        tpl = "{% include 'mint_response." + template + "' %}" # . and %s fails (?)
        super(MintTemplateResponse, self).__init__(tpl)

    def render(self, rdf, template, errors, result, message, results_length=0, contents=''):
        return super(MintTemplateResponse, self).render(Context({"rdf": rdf, "template": template, "errors": errors, 
                                                                 "result": result, "message": message, 
                                                                 "results_length": results_length, 
                                                                 "contents": contents}))

class DefaultCoreError(Template):

    def __init__(self, template="core_errors/core_error.html"):
        tmpl = "{%% include '%s' %%}" % template
        super(DefaultCoreError, self).__init__(tmpl)

    def render(self, title, description, request, extras={}):
        context = {"error_title": title, "error_description": description, "extras": json.dumps(extras), "auth_manager": request.auth_manager}
        ctx = Context(context)
        return super(DefaultCoreError, self).render(ctx)

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
