# -*- coding: utf-8 -*-
import logging

from django.conf import settings
from django.http import Http404
from django.shortcuts import redirect

from core.models import Account
from core.http import get_domain_by_request
from core.http import get_domain_with_protocol
from core.exceptions import *
from microsites.exceptions import *
from core.models import AccountAnonymousUser

class DependencyInjector(object):
    """ Gets the current site & account """

    def process_request(self, request):
        domain = get_domain_by_request(request)
        request.bucket_name = settings.AWS_BUCKET_NAME

        try:
            account = Account.get_by_domain(domain)
        except Account.DoesNotExist:
            logger = logging.getLogger(__name__)
            logger.error('The account do not exists: %s' % domain)
            raise AccountDoesNotExist

        request.account = account

        preferences = account.get_preferences()
        preferences.load_all()
        preferences['account_id'] = account.id
        request.preferences = preferences

        bucket_name = preferences['account_bucket_name']
        if bucket_name:
            request.bucket_name = bucket_name

        is_signin = False #Deprecado
        is_login = False #Deprecado
        is_activate = False #Deprecado
        is_jsi18n = request.path.startswith('/jsi18n')

        language = request.preferences['account_language']
        if language:
            request.session['django_language'] = language
            request.auth_manager.language = language

        if settings.DOMAINS['microsites'] == domain:
            if request.META.get('REQUEST_URI') == '/':
                return redirect(get_domain_with_protocol('microsites') + "/home")

        # hacemos que el User sea un AccountAnonymousUser
        # lo creamos con el account y el lenguaje que tenga el account_language
        request.user = AccountAnonymousUser(request.account, preferences['account_language'])

        return None
