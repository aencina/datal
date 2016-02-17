from django.utils.translation import ugettext_lazy as _

from core.exceptions import *
from core.actions import *

class VisualizationRevisionDoesNotExist(LifeCycleException):
	title = _('EXCEPTION-TITLE-REVISION-NOT-EXIST')
	description = _('EXCEPTION-DESCRIPTION-REVISION-NOT-EXIST')
	tipo = 'revision-no-exist'
	status_code = 404

class VisualizationDoesNotExist(DATALException):
	title = _('EXCEPTION-TITLE-VISUALIZATION-NOT-EXIST')
	description = _('EXCEPTION-DESCRIPTION-VISUALIZATION-NOT-EXIST')
	tipo = 'visualization-dont-exist'
	status_code = 404

class AccountDoesNotExist(DATALException):
	title = _('EXCEPTION-TITLE-ACCOUNT-NOT-EXIST')
	description = _('EXCEPTION-DESCRIPTION-ACCOUNT-NOT-EXIST')
	tipo = 'account-no-exist'
	status_code = 404

class InvalidPage(DATALException):
	title = _('EXCEPTION-TITLE-INVALID-PAGE')
	description = _('EXCEPTION-DESCRIPTION-INVALID-PAGE')
	tipo = 'invalid-page'
	status_code = 404

class DataStreamDoesNotExist(DATALException):
	title = _('EXCEPTION-TITLE-DATASTREAM-NOT-EXIST')
	description = _('EXCEPTION-DESCRIPTION-DATASTREAM-NOT-EXIST')
	tipo = 'datastream-dont-exist'
	status_code = 404

class DatasetDoesNotExist(DATALException):
	title = _('EXCEPTION-TITLE-DATASET-NOT-EXIST')
	description = _('EXCEPTION-DESCRIPTION-DATASET-NOT-EXIST')
	tipo = 'dataset-dont-exist'
	status_code = 404

class DatsetError(DATALException):
	title = _('EXCEPTION-TITLE-DATASET-ERROR')
	description = _('EXCEPTION-DESCRIPTION-DATASTET-ERROR')
	tipo = 'dataset-error'
	status_code = 404

class NotAccesVisualization(DATALException):
	title = _('EXCEPTION-TITLE-VISUALIZATION-NOT-ACCESS')
	description = _('EXCEPTION-DESCRIPTION-VISUALIZATION-NOT-ACCESS')
	tipo = 'not-access'
	status_code = 404