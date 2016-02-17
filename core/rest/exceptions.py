from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework.compat import set_rollback
from rest_framework import status
from django.conf import settings
from core.exceptions import DATALException
import logging
import sys, traceback
import json

def datal_exception_handler(exception, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exception, context)

    # Now add the HTTP status code to the response.
    if not response is None:
        response.data['status'] = response.status_code
        if not 'description' in response.data:
            response.data['description'] = ''
            if 'detail' in response.data:
                response.data['description'] =  response.data.pop('detail')
        response.data['error'] = str(exception.__class__.__name__)
        response.data['type'] = 'api-error'
    elif isinstance(exception, DATALException):
        set_rollback()
        response = Response({}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        response.data['status'] = exception.status_code
        response.data['description'] =  exception.description % {}
        response.data['error'] = str(exception.__class__.__name__)
        response.data['type'] = exception.tipo
    elif not settings.DEBUG:
        logger = logging.getLogger(__name__)
        trace = '\n'.join(traceback.format_exception(*(sys.exc_info())))
        logger.error('[UnexpectedCatchError] %s. %s %s' % (
                str(exception), repr(exception), trace))
        set_rollback()
        response = Response({}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        response.data['status'] = response.status_code
        response.data['description'] = json.dumps(str(exception))
        response.data['error'] = str(exception.__class__.__name__)
        response.data['type'] = 'unexpected-error'

    return response
