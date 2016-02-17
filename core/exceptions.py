# import json
# from core.choices import StatusChoices
from django.utils.translation import ugettext_lazy as _
# from django.core.urlresolvers import reverse
from core.actions import *
from django.conf import settings
from core.choices import RESOURCES_CHOICES
from django.http import HttpResponse
from django.template import TemplateDoesNotExist
from django.template import Context, Template
from django.template.loader import get_template
import logging

class DATALException(Exception):
    """DATAL Exception class: Base class for handling exceptions."""
    title = _('EXCEPTION-TITLE-GENERIC')
    description = _('EXCEPTION-DESCRIPTION-GENERIC')
    tipo = 'datal-abstract'
    status_code = 400
    _context = {}
    template = 'datal_exception'

    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self._context = self._context.copy()
        self._context.update(kwargs)
        self.title = self.title % self._context
        self.description = self.description % self._context
        message = '%s. %s' % (self.title, self.description)
        super(DATALException, self).__init__(message)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return '%s: %s' % (self.title, self.description)

    def get_actions(self):
        return []

'''
ExceptionManager
Class to receive exceptions from middlewares and other classes and return the HttpResponse Object.
Arguments:
    response: Object response of Django.
    auth_manager: Object with user information
    output: type of return html or json
    exception: type of exception 500, 404, etc
    application: string api/microsites/workspace
    template: string width the template to return de view.
'''
class ExceptionManager():
    def __init__(self,response, output,exception, application,template):

        self.application = application
        self.output = output
        self.exception = exception
        self.response = response
        self.template = template     

    def process(self):
        logger = logging.getLogger(__name__)
        logger.warning('[CatchError]  %s. %s' % (self.exception.title, 
            self.exception.description))
        return HttpResponse(self.response, mimetype=self.output, status=self.exception.status_code)

class UnkownException(DATALException):
    title = _('EXCEPTION-TITLE-UNKNOWN')
    description = _('EXCEPTION-DESCRIPTION-UNKNOWN')
    tipo = 'unknown'
    status_code = 500 # Internal Server Error

    def __init__(self, name, trace):
        super(UnkownException, self).__init__(
            exception_name=name,
            exception_trace=trace)

    def get_actions(self):
        return [ContactUsExceptionAction()]

class LifeCycleException(DATALException):
    title = _('EXCEPTION-TITLE-LIFE-CYCLE')
    description = _('EXCEPTION-DESCRIPTION-LIFE-CYCLE')
    tipo = 'life-cycle'
    status_code = 409 # Conflict


class ChildNotApprovedException(LifeCycleException):
    """ Exception for resources that need approved child to change state """
    title = _('EXCEPTION-TITLE-CHILD-NOT-APPROVED')
    # Translators: Ejemplo, "Existen %(count)s hijos sin aprobar"
    description = _('EXCEPTION-DESCRIPTION-CHILD-NOT-APPROVED')
    tipo = 'child-not-approved'
    status_code =  409 # Conflict
    _context = {
        'count': 0,
        'resource_type': settings.TYPE_DATASTREAM 
    }

    def __init__(self, revision, resource_type):
        self.revision = revision
        for tipo, texto in RESOURCES_CHOICES:
            if resource_type == tipo:
                self.resource_type = texto
                break 
        super(ChildNotApprovedException, self).__init__(resource_type=self.resource_type)

    def get_actions(self):
        return [ReviewAssociatedResources(self.revision)]


class SaveException(LifeCycleException):

    title = _('EXCEPTION-TITLE-SAVE-ERROR')
    description = _('EXCEPTION-DESCRIPTION-SAVE-ERROR')
    tipo = 'save-error'
    status_code = 503 # Service Unavailable

    def __init__(self, form):
        self.form = form
        self.description += ' errors: %(errors)s'
        super(SaveException, self).__init__(errors=form.errors.as_text().replace('\n', ', '))
        
    def get_actions(self):
        return [ContactUsExceptionAction()]


class DatasetSaveException(SaveException):
    title = _('EXCEPTION-TITLE-DATASET-SAVE-ERROR')
    description = _('EXCEPTION-DESCRIPTION-DATASET-SAVE-ERROR')
    tipo = 'dataset-save-error'

class DatastreamSaveException(SaveException):
    title = _('EXCEPTION-TITLE-DATASTREAM-SAVE-ERROR')
    description = _('EXCEPTION-DESCRIPTION-DATASTREAM-SAVE-ERROR')
    tipo = 'datastream-save-error'


class VisualizationSaveException(SaveException):
    title = _('EXCEPTION-TITLE-VISUALIZATION-SAVE-ERROR')
    description = _('EXCEPTION-DESCRIPTION-VISUALIZATION-SAVE-ERROR')
    tipo = 'visualization-save-error'


class DatasetNotFoundException(LifeCycleException):
    title = _('EXCEPTION-TITLE-DATASET-NOT-FOUND')
    description = _('EXCEPTION-DESCRIPTION-DATASET-NOT-FOUND')
    tipo = 'dataset-not-found'
    status_code = 404  # Not Found

    def get_actions(self):
        return [ViewDatasetListExceptionAction()]

class DatasetTableNotFoundException(LifeCycleException):
    title = _('EXCEPTION-TITLE-DATASET-TABLE-NOT-FOUND')
    description = _('EXCEPTION-DESCRIPTION-DATASET-TABLE-NOT-FOUND')
    tipo = 'dataset-table-not-found'
    status_code = 404 # Not Found
    table_id = 0 # valor defaault

class DataStreamNotFoundException(LifeCycleException):
    title = _('EXCEPTION-TITLE-DATASTREAM-NOT-FOUND')
    description = _('EXCEPTION-DESCRIPTION-DATASTREAM-NOT-FOUND')
    tipo = 'datastream-not-found'
    status_code = 404 # Not Found

    def get_actions(self):
        return [ViewDatastreamListExceptionAction()]


class VisualizationNotFoundException(LifeCycleException):
    title = _('EXCEPTION-TITLE-VISUALIZATION-NOT-FOUND')
    description = _('EXCEPTION-DESCRIPTION-VISUALIZATION-NOT-FOUND')
    tipo = 'visualization-not-found'
    status_code = 404 # Not Found
    def get_actions(self):
        return [ViewVisualizationListExceptionAction()]


class VisualizationRequiredException(LifeCycleException):
    title = _('EXCEPTION-TITLE-VIZUALIZATION-REQUIRED')
    description = _('EXCEPTION-DESCRIPTION-VIZUALIZATION-REQUIRED')
    tipo = 'vizualization-required'
    status_code = 410 # Gone

    def get_actions(self):
        return [ViewVisualizationListExceptionAction()]

class ParentNotPublishedException(LifeCycleException):
    title = _('EXCEPTION-TITLE-PARENT-NOT-PUBLISHED')
    description = _('EXCEPTION-DESCRIPTION-PARENT-NOT-PUBLISHED')
    tipo = 'parent-not-published'
    status_code =  499 # Own status code for refresh

    def __init__(self, revision=None):
        self.revision = revision
        super(ParentNotPublishedException, self).__init__()

class VisualizationParentNotPublishedException(ParentNotPublishedException):
    title = _('EXCEPTION-TITLE-VISUALIZATION-PARENT-NOT-PUBLISHED')
    description = _('EXCEPTION-DESCRIPTION-VIZUALIZATION-PARENT-NOT-PUBLISHED')

    def get_actions(self):
        if hasattr(self, 'revision'):#Prevent exepction for Exception Test script to prevent fall in the view.
            return [ViewDatastreamExceptionAction(self.revision)]

class DatastreamParentNotPublishedException(ParentNotPublishedException):
    title = _('EXCEPTION-TITLE-DATASTREM-PARENT-NOT-PUBLISHED')
    description = _('EXCEPTION-DESCRIPTION-DATASTREM-PARENT-NOT-PUBLISHED')

    def get_actions(self):
        #Prevent exepction for Exception Test script to prevent fall in the view.
        if hasattr(self, 'revision'): #
            return [ViewDatasetExceptionAction(self.revision)]


class IllegalStateException(LifeCycleException):
    title = _('EXCEPTION-TITLE-ILLEGAL-STATE')
    description = _('EXCEPTION-DESCRIPTION-ILLEGAL-STATE')
    tipo = 'illegal-state'
    status_code =  409 # Conflict


class FileTypeNotValidException(LifeCycleException):
    title = _('EXCEPTION-TITLE-FILE-INVALID')
    description = _('EXCEPTION-DESCRIPTION-FILE-INVALID')
    tipo = 'illegal-state'
    file_type = '' #valor defaault
    status_code =  400 # Bad Request
    valid_types = [] #valor default

    def get_actions(self):
        return [ValidFileType(self._context['valid_types'])]


class ApplicationException(DATALException):
    title = 'Application error'


class DatastoreNotFoundException(ApplicationException):
    title = 'Data Store not found'


class MailServiceNotFoundException(ApplicationException):
    title = 'Mail service not found'


class SearchIndexNotFoundException(ApplicationException):
    title = 'Search index not found exception'





class S3CreateException(DATALException):
    title = 'S3 Create error'

    def __init__(self, description):
        super(S3CreateException, self).__init__(
            description=description,
            status_code=503
        )


class S3UpdateException(DATALException):
    title = 'S3 Update error'

    def __init__(self, description):
        super(S3UpdateException, self).__init__(
            description=description,
            status_code=503
        )


class SFTPCreateException(DATALException):
    title = 'SFTP Create error'

    def __init__(self, description):
        super(SFTPCreateException, self).__init__(
            description=description,
            status_code=503
        )


class SFTPUpdateException(DATALException):
    title = 'SFTP Update error'

    def __init__(self, description):
        super(SFTPUpdateException, self).__init__(
            description=description,
            status_code=503
        )


class NoStatusProvidedException(DATALException):
    title = _('EXCEPTION-TITLE-NO-STATUS-PROVIDED-ERROR')
    description = _('EXCEPTION-DESCRIPTION-NO-STATUS-PROVIDED-ERROR')
    tipo = 'change-resource-status-error'


### Old Api Excepctions

ERROR_KEY = 'error'
DESCRIPTION_KEY = 'message'


class JunarException(Exception):
    """
    JunarException class: Base class for handling exceptions.
    """

    def __init__(self, info):
        self.info = info
        super(JunarException, self).__init__(self.info[DESCRIPTION_KEY])

    def __str__(self):
        return str(self.info)

    def convert_json(self):
        return json.dumps(self.info)


class Http400(JunarException):
    """ Bad Request Exception """

    def __init__(self, description):
        self.info = dict()
        self.info[ERROR_KEY] = 'Bad request'
        self.info[DESCRIPTION_KEY] = description
        super(Http400, self).__init__(self.info)


class MintTemplateURLError(Http400):

    def __init__(self, description = 'The template URL is wrong or empty'):
        super(MintTemplateURLError, self).__init__(description)

class MintTemplateNotFoundError(Http400):

    def __init__(self, description = 'The template was not found'):
        super(MintTemplateNotFoundError, self).__init__(description)

class ApplicationNotAdmin(Http400):

    def __init__(self, description = 'The auth key is not for admin'):
        super(ApplicationNotAdmin, self).__init__(description)

class Http401(JunarException):
    """ Unauthorized Exception """

    def __init__(self, description='Unauthorized to access requested resource.'):
        self.info = dict()
        self.info[ERROR_KEY] = 'Unauthorized'
        self.info[DESCRIPTION_KEY] = description
        super(Http401, self).__init__(self.info)

class InvalidKey(Http401):
    def __init__(self, description = 'The auth key is not valid'):
        super(InvalidKey, self).__init__(description)

class Http405(JunarException):
    """ Not Allowed Exception """

    def __init__(self, p_methods=['GET']):
        """ By default the only accepted method is GET """
        self.info = dict()
        self.info[ERROR_KEY] = 'Not allowed'
        self.info[DESCRIPTION_KEY] = 'Method not allowed.'
        self.methods = p_methods
        super(Http405, self).__init__(self.info)

class Http404(JunarException):
    """ Not Found Exception """

    def __init__(self, description='Resource not found'):
        self.info = dict()
        self.info[ERROR_KEY] = 'Not found error'
        self.info[DESCRIPTION_KEY] = description
        super(Http404, self).__init__(self.info)

class Http500(JunarException):
    """ Internal Server Error Exception """

    def __init__(self, description):
        self.info = dict()
        self.info[ERROR_KEY] = 'Server error'
        self.info[DESCRIPTION_KEY] = description
        super(Http500, self).__init__(self.info)

class BigdataNamespaceNotDefined(Http500):
    """ The preference 'namespace' is not defined
        for this account.
    """

    def __init__(self):
        description = 'Bigdata namespace account preference must be defined.'
        super(BigdataNamespaceNotDefined, self).__init__(description)

class BigdataCrossNamespaceForbidden(Http401):
    """ Cross namespace requests to bigdata are not allowed
    """

    def __init__(self):
        description = 'Cross namespace requests are not allowed.'
        super(BigdataCrossNamespaceForbidden, self).__init__(description)

class BigDataInsertError(Http500):

    def __init__(self, namespace, context="", extras=""):
        description = 'BigData insertion fails. Namespace: [%s] Context: [%s] Detail [%s]' % (namespace, context, extras)
        super(BigDataInsertError, self).__init__(description)

class BigDataDeleteError(Http500):

    def __init__(self, namespace, context="", extras=""):
        description = 'BigData delete fails. Failed DELETE RDF-context [%s]-[%s] --  %s' % (context, namespace, extras)
        super(BigDataDeleteError, self).__init__(description)

class BigDataInvalidQuery(Http401):

    def __init__(self, error):
        # description = 'BigData unauthorized query. %s' % error
        super(BigDataInvalidQuery, self).__init__()

