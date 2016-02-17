import json

from django.http import HttpResponse
from django.utils.decorators import available_attrs
from django.utils.translation import ugettext
from django.views.decorators.cache import cache_page

from functools import wraps

from core.models import Dataset, Threshold, User
from core.exceptions import ApplicationNotAdmin
from core.models import Application
# from django.utils.encoding import smart_str


def public_keys_forbidden(view_func):
    """ 'application' means users by auth_key access """
    @wraps(view_func, assigned=available_attrs(view_func))
    def _wrapped_view(request, *args, **kwargs):
        try:
            auth_key = request.REQUEST.get('auth_key')
            app = Application.objects.get(auth_key = auth_key)
            request.app = app
            if app.type == "04":
                return view_func(request, *args, **kwargs)
            else:
                raise ApplicationNotAdmin("Invalid Authorization Key")
        except:
            raise ApplicationNotAdmin("Invalid Authorization Key")

    return _wrapped_view


def datal_make_key(key, key_prefix, version):
    """
        sobre escribe el metodo make_key del cache para generar la key, ignorando key
    """
    # en junar return smart_str(':'.join([key_prefix, str(version), key]))
    return ":".join([str(version), key_prefix])


def datal_cache_page(**kwargs):
    def _cache_page(viewfunc):
        @wraps(viewfunc, assigned=available_attrs(viewfunc))
        def _cache_page(request, *args, **kw):
            params=str(hash(frozenset(sorted(request.REQUEST.items()))))
            key_prefix = ":".join([request.path, params])
            response = cache_page(60, cache='engine', key_prefix=key_prefix)(viewfunc)
            return response(request, *args, **kw)
        return _cache_page
    return _cache_page

def threshold(code):
    def decorator(func):
        def inner_decorator(request, *args, **kwargs):
            if code == 'workspace.create_dataset_limit':
                response = calculate_dataset_limit(request, code)

            if code == 'workspace.create_user_limit':
                response = calculate_user_limit(request, code)

            if response == '':
                return func(request, *args, **kwargs)
            else:
                return HttpResponse(json.dumps(response), mimetype='application/json', status=400)

        return wraps(func)(inner_decorator)

    return decorator


def calculate_dataset_limit(request, code):
    account_id = request.auth_manager.account_id
    datasets_count = Dataset.objects.filter(user__account__id=account_id).count()
    limit = Threshold.objects.get_limit_by_code_and_account_id(code, account_id)

    if datasets_count >= limit:
        response = {'status': 'error', 'messages': [ugettext('APP-EXCEDEDDATASET-LIMIT')]}
        return response
    else:
        return ''


def calculate_user_limit(request, code):
    account_id = request.auth_manager.account_id
    users_count = User.objects.filter(account=account_id).count()
    limit = Threshold.objects.get_limit_by_code_and_account_id(code, account_id)

    if users_count >= limit:
        response = {'status': 'error', 'messages': [ugettext('APP-EXCEDEDUSERS-LIMIT')]}
        return response
    else:
        return ''
