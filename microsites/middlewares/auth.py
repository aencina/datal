# -*- coding: utf-8 -*-

from django.conf import settings
from core.auth.auth import AuthManager

import logging

logger = logging.getLogger(__name__)

class AccessManager(object):
    """
    Check for user, rol and active account
    """

    def process_request(self, request):
        """
        Checks user, role and account
        """

        # for anonymous users
        request.session['django_language'] = settings.LANGUAGES[0][0]

        if request.META.has_key('HTTP_ACCEPT_LANGUAGE'):
            user_language = request.META['HTTP_ACCEPT_LANGUAGE'].split(',')[0].split('-')[0]
            if user_language in [ language[0] for language in settings.LANGUAGES ]:
                request.session['django_language'] = user_language

        request.auth_manager = AuthManager(language = request.session['django_language'])

        # el user se arma en middlerware.ioc ya que necesitamos el account para completar el user
        request.user = None
        return None
