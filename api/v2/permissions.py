from rest_framework import permissions
from core.models import AccountAnonymousUser

class ApiPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return ('account_id' in obj and 
                obj['account_id'] in [x['id'] for x in request.auth['account'].account_set.values('id').all()] + [request.auth['account'].id])

class ApiPrivateForWritePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method not in permissions.SAFE_METHODS:
            return request.auth['application'].is_private_auth_key(
                request.auth['auth_key'])
        return True

class ApiIsUserForWritePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method not in permissions.SAFE_METHODS:
            return (request.user and 
                    not isinstance(request.user, AccountAnonymousUser) )
        return True
