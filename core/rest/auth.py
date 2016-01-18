from core.models import AccountAnonymousUser
from core.http import get_domain 
from rest_framework import authentication


class RestAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        if hasattr(request, 'account') and request.account:
            account = request.account

            return (
                AccountAnonymousUser(account), {
                    'account': account,
                    'preferences': None,
                    'language': request.auth_manager.language,
                    'microsite_domain': get_domain(account.id),
                }
            )
