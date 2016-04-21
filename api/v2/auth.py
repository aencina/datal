from django.db.models import Q
from core.models import Application, Account, User, AccountAnonymousUser
from core.http import get_domain, get_domain_by_request
from urlparse import urlparse
from rest_framework import authentication
from rest_framework import exceptions

import logging
import re

logger = logging.getLogger(__name__)


class DatalApiAuthentication(authentication.TokenAuthentication):
    def authenticate(self, request):
        self.request = request
        auth_key = request.query_params.get("auth_key", None)
        if not auth_key:
            # TODO: Esto es para soportar la api v1 lo deberiamos sacar
            auth_key = request.data.get('auth_key', None)
            if not auth_key:
                return super(DatalApiAuthentication, self).authenticate(request)
        return self.authenticate_credentials(auth_key)

    def authenticate_credentials(self, auth_key):
        user_id = None
        account_id = None

        account = self.resolve_account(self.request)
        if not account:
            raise exceptions.AuthenticationFailed('Invalid Account.')

        application = self.resolve_application(self.request, auth_key, account)
        if not application:
            raise exceptions.AuthenticationFailed('Auth Key does not exist.')
        if application.is_public_auth_key(auth_key):
            if not self.check_referer(self.request, application):
                raise exceptions.AuthenticationFailed('Invalid referer')

        preferences = account.get_preferences()
        
        user = self.resolve_user(application, account, preferences['account.language'])

        return (
            user, {
                'account': account,
                'preferences': preferences,
                'application': application,
                'auth_key': auth_key,
                'language': preferences['account.language'],
                'microsite_domain': get_domain(account.id),
            }
        )

    def authenticate_header(self, request):
        return 'Token'
    
    def check_referer(self, request, application):

        referer = request.META.get('HTTP_REFERER', None)
        if not referer:
            return False

        if not application.domains:
            return False

        domains = application.domains.split('\n')
        wcardsdoms = [ wcardsdom for wcardsdom in domains if wcardsdom ]

        parsed_referer = urlparse(referer)
        for wcardsdom in wcardsdoms:
            to_match_domain = wcardsdom.replace('.', '\.').replace('*', '.*')
            to_match_domain = to_match_domain.strip()
            if re.search(to_match_domain, parsed_referer.netloc):
                return True
        return False

    def resolve_account(self, request):
        domain = get_domain_by_request(request)

        # creo que en algun punto desreferencia a Account
        from core.models import Account
        return Account.get_by_domain(domain)

    def resolve_application(self, request, auth_key, account):
        try:
            return Application.objects.filter(
                Q(auth_key = auth_key) | Q(public_auth_key = auth_key), 
                account=account,
                valid=True
            ).first()
        except Application.DoesNotExist:
            return None

    def resolve_user(self, application, account, language):
        if application.user_id:
            try:
                return User.objects.get(pk=application.user_id)
            except User.DoesNotExist:
                return AccountAnonymousUser(account, language)
        return AccountAnonymousUser(account, language)
