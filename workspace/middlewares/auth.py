# -*- coding: utf-8 -*-
from django.conf import settings
from django.shortcuts import redirect
from core.models import User, Account
from core.auth.auth import AuthManager
from django.utils.timezone import now
from core.http import get_domain_by_request

class AccessManager(object):
    """
    Check for user, rol and active account
    """

    def process_request(self, request):
        """
        Checks user, role and account
        """

        try:
            user_id = request.session.get("user_id")
            user = User.objects.get(pk=user_id)

        except User.DoesNotExist:
            # for anonymous users
            request.session['django_language'] = settings.LANGUAGES[0][0]

            if request.META.has_key('HTTP_ACCEPT_LANGUAGE'):
                user_language = request.META['HTTP_ACCEPT_LANGUAGE'].split(',')[0].split('-')[0]
                if user_language in [ language[0] for language in settings.LANGUAGES ]:
                    request.session['django_language'] = user_language

            request.auth_manager = AuthManager(language = request.session['django_language'])
            request.user = None
            return None

        user.last_visit = now()
        user.save()

        request.user = user
        request.auth_manager = AuthManager(user)
        request.session['django_language'] = user.language

        if not request.auth_manager.has_privilege('workspace.can_signin'):
            request.session.clear()
            return redirect('/')

        request.account = Account.objects.get(pk = user.account_id)

        return None





