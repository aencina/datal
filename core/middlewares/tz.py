# -*- coding: utf-8 -*-
from django.conf import settings
from django.utils import timezone
import pytz

class TimezoneMiddleware(object):
    """ Handles the request for forcing language """

    def process_request(self, request):
        if hasattr(request, 'auth_manager'):
            timezone.activate(pytz.timezone(request.auth_manager.timezone))
        