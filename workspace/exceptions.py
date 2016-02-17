from django.utils.translation import ugettext_lazy as _

from core.exceptions import *
from core.actions import *

class ResourceRequiredException(LifeCycleException):
    title = _('EXCEPTION-TITLE-RESOURCE-REQUIRED')
    description = _('EXCEPTION-DESCRIPTION-RESOURCE-REQUIRED')
    tipo = 'resource-required'

    def get_actions(self):
        return [ContactUsExceptionAction()]


class AnyResourceRequiredException(LifeCycleException):
    title = _('EXCEPTION-TITLE-ANY-RESOURCE-REQUIRED')
    description = _('EXCEPTION-DESCRIPTION-ANY-RESOURCE-REQUIRED')
    tipo = 'resource-required'


class DatasetRequiredException(ResourceRequiredException):
    title = _('EXCEPTION-TITLE-DATASET-REQUIRED')
    description = _('EXCEPTION-DESCRIPTION-DATASET-REQUIRED')
    tipo = 'dataset-required'


class DatastreamRequiredException(ResourceRequiredException):
    title = _('EXCEPTION-TITLE-DATASTREAM-REQUIRED')
    description = _('EXCEPTION-DESCRIPTION-DATASTREAM-REQUIRED')
    tipo = 'datastream-required'


class AnyDatasetRequiredException(AnyResourceRequiredException):
    title = _('EXCEPTION-TITLE-ANY-DATASET-REQUIRED')
    description = _('EXCEPTION-DESCRIPTION-ANY-DATASET-REQUIRED')
    tipo = 'any-dataset-required'

    def get_actions(self):
        return [ViewDatasetCreateExceptionAction()]

class AnyDatastreamRequiredException(AnyResourceRequiredException):
    title = _('EXCEPTION-TITLE-ANY-DATASTREAM-REQUIRED')
    description = _('EXCEPTION-DESCRIPTION-ANY-DATASTREAM-REQUIRED')
    tipo = 'any-datastream-required'

    def get_actions(self):
        return [ViewDatastreamCreateExceptionAction()]


class InsufficientPrivilegesException(DATALException):
    title = _('EXCEPTION-TITLE-INSUFFICIENT-PRIVILEGES')
    description = _('EXCEPTION-DESCRIPTION-INSUFFICIENT-PRIVILEGES')
    tipo = 'insufficient-priviliges'
    status_code = 403 # Forbidden


class RequiresReviewException(LifeCycleException):
    title = _('EXCEPTION-TITLE-REQUIRES-REVIEW')
    description = _('EXCEPTION-DESCRIPTION-REQUIRES-REVIEW')
    tipo = 'requires-review'
