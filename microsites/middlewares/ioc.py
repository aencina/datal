# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import redirect
from core.models import Account
from core.http import get_domain
from core.helpers import get_domain_with_protocol
import logging

class DependencyInjector(object):
    """ Gets the current site & account """

    def process_request(self, request):
        domain = get_domain(request)
        request.bucket_name = settings.AWS_BUCKET_NAME

        try:
            # check for develop domains
            if settings.DOMAINS['microsites'] != domain:
                account = Account.objects.get_by_domain(domain)
            else:
                # use default account if exists
                account = Account.objects.get(pk=1)
        except Account.DoesNotExist:
            logger = logging.getLogger(__name__)
            logger.error('The account do not exists: %s' % domain)
            raise Http404

        request.account = account

        preferences = account.get_preferences()
        preferences.load_all()
        request.preferences = preferences
        request.is_private_site = False

        bucket_name = preferences['account_bucket_name']
        if bucket_name:
            request.bucket_name = bucket_name

        is_signin = request.path.startswith(reverse('accounts.signin'))
        is_login = request.path.startswith(reverse('accounts.login'))
        is_activate = request.path.startswith(reverse('accounts.activate'))
        is_jsi18n = request.path.startswith('/jsi18n')



        language = request.preferences['account_language']
        if language:
            request.session['django_language'] = language
            request.auth_manager.language = language



        if settings.DOMAINS['microsites'] == domain:
            if request.META.get('REQUEST_URI') == '/':
                return redirect(get_domain_with_protocol('microsites') + "/home")

        return None
