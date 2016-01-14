# -*- coding: utf-8 -*-
import logging
from django.conf import settings
from core.choices import SourceImplementationChoices

logger = logging.getLogger(__name__)


class DatasetImplBuilderWrapper:

    def __init__(self, **fields):
        if int(fields['impl_type']) == SourceImplementationChoices.REST:
            self.builder = RESTImplBuilder(**fields)
        elif int(fields['impl_type']) == SourceImplementationChoices.SOAP:
            self.builder = SOAPImplBuilder(**fields)
        else:
            self.builder = DefaultImplBuilder(**fields)

    def build(self):

        return self.builder is None and '' or self.builder.build()


class DefaultImplBuilder(object):
    required_fields = []

    def __init__(self, changed_fields=None, **fields):
        self.changed_fields = changed_fields
        self.fields = fields

    def build(self):
        return ''

    def has_changed(self, changed_fields):
        return set(changed_fields).isdisjoint(set(self.required_fields))


class RESTImplBuilder(DefaultImplBuilder):

    def __init__(self, **fields):
        super(self.__class__, self).__init__(**fields)

        self.required_fields += ['path_to_headers', 'path_to_data', 'token', 'algorithm', 'username', 'password', 'useCache', 'parameters', 'signature']


    def build(self):
        """ build for SourceImplementationChoices = 14 (REST)
        Sometimes impl_details is defined on JS. On API call it's necesary to build it
        """
        path_to_headers = self.fields.get('path_to_headers')
        path_to_data = self.fields.get('path_to_data')
        token = self.fields.get('token')
        algorithm = self.fields.get('algorithm')
        username = self.fields.get('username')
        password = self.fields.get('password')
        useCache = str(self.fields.get('use_cache', False)).lower()
        attHeaders = str(self.fields.get('att_headers', False)).lower()
        parameters = self.fields.get('parameters')
        signature = self.fields.get('signature')

        if not path_to_data or path_to_data == '':
            path_to_data = '$'
        impl_details = '<wsOperation useCache="%s" useAttrAsHeaders="%s"><pathToHeaders>%s</pathToHeaders><pathToData>%s</pathToData>' % (useCache, attHeaders, path_to_headers, path_to_data)

        # uriSignatures
        if token != "" or algorithm != "":
            impl_details += '<uriSignatures>'
            impl_details += '<%s>' % signature
            impl_details += '<token>%s</token>' % token
            impl_details += '<algorithm>%s</algorithm>' % algorithm
            impl_details += '</%s>' % signature
            impl_details += '</uriSignatures>'
        else:
            impl_details += '<uriSignatures/>'

        if parameters and len(parameters) > 0:
            impl_details += '<args>'
            for argue in parameters:
                impl_details += '<%s editable="%s">%s</%s>' % (argue['name'], argue['editable'], argue['default_value'], argue['name'])
            impl_details += '</args>'
        else:
            impl_details += "<args/>"

        # user and pass
        if username != "" or password != "":
            impl_details += '<authentication><userName>%s</userName><password>%s</password></authentication>' % (username, password)
        else:
            impl_details += '<authentication/>'

        impl_details += '</wsOperation>'

        return impl_details


class SOAPImplBuilder(DefaultImplBuilder):

    def __init__(self, **fields):
        super(self.__class__, self).__init__(**fields)

        self.required_fields += ['method_name', 'namespace', 'useCache', 'parameters']

    def build(self):
        """ build for SourceImplementationChoices = 1 (SOAP) """

        method_name = self.fields.get('method_name')
        namespace = self.fields.get('namespace')
        useCache = str(self.fields.get('use_cache', False)).lower()
        attHeaders = str(self.fields.get('att_headers', False)).lower()
        parameters = self.fields.get('parameters')

        if settings.DEBUG: logger.info('Building SOAP impl_details (%s) (%s) (%s) (%s) (%s)' % (method_name, namespace, str(useCache), str(attHeaders), str(parameters)))
        
        impl_details = '<wsOperation useCache="%s" useAttrAsHeaders="%s">' % (useCache, attHeaders)
        impl_details += '<methodName>%s</methodName>' % method_name
        impl_details += '<targetNamespace>%s</targetNamespace>' % namespace

        if parameters and len(parameters) > 0:
            impl_details += '<args>'
            for argue in parameters:
                impl_details += '<%s editable="%s">%s</%s>' % (argue['name'], argue['editable'], argue['default_value'], argue['name'])
            impl_details += '</args>'
        else:
            impl_details += "<args/>"

        impl_details += '</wsOperation>'
        return impl_details

        """ SOAP impl_details example
            <wsOperation>
                <methodName>IndicadoresResumenAnual</methodName>
                <targetNamespace>http://www.bahiablanca.gov.ar/wsMBB</targetNamespace>
                <fields>
                    <Key>xxxxxxxxxxxxxxxxxxxd</Key>
                    <IDPrograma editable="true">1</IDPrograma>
                    <IDIndicadores editable="true">1</IDIndicadores>
                    <AnioDesde editable="true">2012</AnioDesde>
                    <AnioHasta editable="true">2012</AnioHasta>
                </fields>
            </wsOperation>"""