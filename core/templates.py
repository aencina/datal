from django.template import Context, Template
from django.conf import settings
import json
import csv
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


class DatasetOutputBigDataTemplate(Template):
    """ procesar un archivo CSV a traves de un template para producir un RDF 
    Tener en cuenta la posibilidad de archivos muy grandes que no quepan en memoria
    """
    # for process CSV files
    csv_url = ''
    csv_local_file = ''
    csv_reader = None # DictReader Object
    total_rows = 0
    final_csv_data = []  # csv data used
    account = None
    datasetrevision = None 
    last_error = '' # for return none and show details
    
    def __init__(self, template):
        # add my filters
        template = "%s\n%s\n%s\n" % ("{% load mint_tags %}", "{% load semantic %}", template)
        super(DatasetOutputBigDataTemplate, self).__init__(template)

    def render(self, request, metadata={}):
        headers = {}
        rows = []
        rows_array = []
        summ = {} # all  columns added
        params = metadata['params']
        page = params.get('page', None)
        limit = params.get('limit', None)
        
        self.open_csv()

        index = 0
        row_number = 0
        self.final_csv_data = []
        
        for line in self.yield_csv(page, limit):
            self.final_csv_data.append(line)
            if row_number == 0: # headers
                total_cols = len(self.csv_reader.fieldnames)
                h = 0
                # for header in reader[0].keys():
                for header in self.csv_reader.fieldnames:
                    headers['column%d' % h] = header
                    summ['column%d' % h] = 0.0
        
            # normal rows
            row  = {}
            row_array = []
            column_number = 0
            # desordenado! -> for key, value in line.iteritems():
            for header in self.csv_reader.fieldnames:
                key = header
                value = line[header]
                
                dat = {"fType": "TEXT", "fStr": value} # emula el sistema anterior
                #summ function for all fields
                try:
                    summ['column%s' % column_number] = summ['column%s' % column_number] + float(value)
                except:
                    pass
                    
                row['column%s' % column_number] = value
                row['data%s' % column_number] = dat # add extra data in case we need it.
                row_array.append(value)
                
                column_number = column_number + 1
                index = index + 1
                
            row_number = row_number + 1
                
            rows.append(row)
            rows_array.append(row_array)

        # extra data
        metadata['summ'] = summ
        metadata['total_rows'] = self.total_rows
        metadata['total_cols'] = total_cols
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
            res = super(DatasetOutputBigDataTemplate, self).render(Context({"rows": rows, "owner": owner, 
                                                                               "publisher": publisher, "author" : author, 
                                                                               "metadata": metadata, "headers": headers}))
        except Exception,e:
            import traceback
            tb = traceback.format_exc()
            self.render_errors = 'ERROR: %s -- TRACE %s' % ( str(e), tb )
            res = False

        return res


    def prepare_csv(self, datasetrevision):
        self.datasetrevision = datasetrevision
        self.account = datasetrevision.user.account

    def open_csv(self):
        # get the CSV file.
        # csv_url = datasetrevision.end_point
        # el API no tiene IOC para cargar al request con el bucket_name
        from core.lib.datastore import active_datastore
        import urllib
        
        account = self.account
        bucket_name = account.get_preference('account_bucket_name') if account.get_preference('account_bucket_name') else settings.AWS_BUCKET_NAME

        datasetrevision = self.datasetrevision
        # detect local vs URL
        end_point = datasetrevision.end_point
        if end_point.find('file://') == 0:
            self.csv_url = active_datastore.build_url(bucket_name, datasetrevision.end_point.replace("file://", ""))
        else:
            self.csv_url = end_point
            
        logger.info('OPEN CSV. url:{}'.format(self.csv_url))
        # guardar el archivo con un nombre vinculado a su URL para no repetir esta descarga
        # en procesos de paginado
        import base64, os.path, tempfile
        # full /tmp disk filename = os.path.join(tempfile.gettempdir(), base64.b64encode(self.csv_url))
        filename = os.path.join('/mnt', base64.b64encode(self.csv_url))
        
        exists = os.path.isfile(filename)
        self.csv_local_file = filename
        logger.info('OPEN CSV check file:{} ({})'.format(filename, exists))
        
        if exists:
            return self.csv_local_file
            
        try:
            # csv_file = urllib2.urlopen(csv_url)
            self.csv_local_file, headers = urllib.urlretrieve(self.csv_url, self.csv_local_file)
            logger.info('OPEN CSV. local:{}'.format(self.csv_local_file))
        except Exception, e:
            logger.error(e)
            return None

        return self.csv_local_file

    
    def yield_csv(self, page=0, limit=10):
        """ huge CSV must be a problem, get data it row by row  """
        if settings.DEBUG: logger.info('YIELD CSV START {} {}'.format(page, limit))
        
        self.total_rows = 0
        page_size = limit
        actual_row = 0
        actual_page = 0
        rows_sended = 0
        
        with open(self.csv_local_file, "rU") as csvfile:
            # detectar el delimitador
            # NOT WORKING dialect = csv.Sniffer().sniff(csvfile.read(1024), [',', ';', '\t'])
            delimiters = [',', ';', '\t']
            first_line = csvfile.readline()
            max_count = 0
            final_delimiter = ',' # def value
            for delimiter in delimiters:
                count = first_line.count(delimiter)
                if count > max_count:
                    final_delimiter = delimiter
                    
                    
            if settings.DEBUG: logger.info('CSV Delimiter {}'.format( str(final_delimiter) ) )
            csvfile.seek(0)
            
            self.csv_reader = csv.DictReader(csvfile, delimiter=final_delimiter)
            
            for row in self.csv_reader:
                self.total_rows += 1
                actual_row += 1

                actual_page = actual_row / page_size
                
                if actual_page == page:
                    rows_sended += 1
                    yield row
                
            if settings.DEBUG: logger.info('YIELD CSV ENDS {}/{}'.format(rows_sended, self.total_rows))
            return
                

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
