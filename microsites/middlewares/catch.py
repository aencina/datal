# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template import TemplateDoesNotExist
from microsites.exceptions import *
from core.exceptions import DATALException
from core.exceptions import ExceptionManager as ExceptionManagerCore

from django.template import Context, Template
from django.template.loader import get_template
import logging
import sys, traceback

import sys, traceback
from django.conf import settings

ERROR_KEY = 'error'
DESCRIPTION_KEY = 'message'
EXTRAS_KEY = 'extras'


class ExceptionManager(object):

    def get_content_type(self, request):
        content_type = None
        if request.META.get('CONTENT_TYPE', False):
            content_type = request.META['CONTENT_TYPE']
        elif request.META.get('HTTP_ACCEPT', False):
            content_type = request.META['HTTP_ACCEPT']
        elif request.META.get('HTTP_CONTENT_TYPE', False):
            content_type = request.META['HTTP_CONTENT_TYPE']
        return content_type

    def get_mime_type(self, request):
        content_type = self.get_content_type(request)
        if content_type.lower().startswith('application/json'):
            return 'application/json'

        if content_type.lower().startswith('multipart/form-data') and request.method == 'POST':
            return 'application/json'

        if content_type.lower().startswith('application/x-www-form-urlencoded') and request.method == 'POST':
            return 'application/json'

        return "text/html"

    def is_json(self, mimetype):
        return mimetype == 'application/json'

    def get_trace(self):
        return '\n'.join(traceback.format_exception(*(sys.exc_info())))

    def log_error(self, exception):
        logger = logging.getLogger(__name__)
        trace = '\n'.join(traceback.format_exception(*(sys.exc_info())))
        logger.error('[UnexpectedCatchError] %s. %s %s' % (
                str(exception), repr(exception), trace))

    """ Middleware for error handling """
    def process_exception(self, request, exception):
        mimetype = self.get_mime_type(request)
        extension = 'json' if self.is_json(mimetype) else 'html'

        if not isinstance(exception, DATALException):
            if extension == 'json':
                exception = UnkownException(str(exception.__class__.__name__),
                    self.get_trace())
            else:
                self.log_error(exception)
                raise

        template = 'microsities_errors/%s.%s' % (exception.template, extension)
        tpl = get_template(template)

        if hasattr(request, 'preferences'):
            preferences = request.preferences
        else:
            preferences = {
                'account_header_uri':False,
                'account_header_height':False,
                'account_footer_uri':False,
                'account_footer_height':False,
                'branding_footer':'',
                'branding_header':'',
            }

        context = Context({
            'preferences':preferences,
            "exception":exception,
            "auth_manager": request.auth_manager
        })

        response = tpl.render(context)
        return ExceptionManagerCore(response=response, output=mimetype,exception=exception, application="microsities",template=template).process()

