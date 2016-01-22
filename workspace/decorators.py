import logging

from functools import wraps
from django.utils.decorators import available_attrs
from django.conf import settings
from core.exceptions import *
from workspace.exceptions import *
from core.choices import StatusChoices
from core.lifecycle.datasets import DatasetLifeCycleManager
from core.lifecycle.datastreams import DatastreamLifeCycleManager
from core.daos.datasets import DatasetDBDAO
from core.daos.datastreams import DataStreamDBDAO
from core.models import DatasetRevision, DataStreamRevision


def require_child_accepted(view_func):
    @wraps(view_func, assigned=available_attrs(view_func))
    def _wrapped_view(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def require_not_pending_review(ids):
    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            """
            namespace = kwargs.get('namespace', None)
            auth_key = request.REQUEST.get('auth_key')
            """
            return view_func(request, *args, **kwargs)

        return _wrapped_view
    return decorator


def require_privilege(privilege):
    def decorator(view_func):
        """ for registred and logged user. NO redirect to login"""
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            if request.auth_manager.has_privilege(privilege):
                return view_func(request, *args, **kwargs)
            else:
                raise InsufficientPrivilegesException(required_privileges=[privilege])

        return _wrapped_view
    return decorator


def requires_if_publish(resource):
    """ En la edicion de recursos quizas se intente publicar, en esos casos
    es necesario validar si el usuario tiene permiso de publicacion """
    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            # check for new status
            if request.POST.get('status', StatusChoices.DRAFT) == StatusChoices.PUBLISHED:
                privilege = 'can_publish_%s' % resource
                if request.auth_manager.has_privilege(privilege):
                    return view_func(request, *args, **kwargs)
                else:
                    raise InsufficientPrivilegesException(required_privileges=[privilege])
            return view_func(request, *args, **kwargs)

        return _wrapped_view
    return decorator


def requires_published_parent():
    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            # check for new status
            if request.POST.get('status', StatusChoices.DRAFT) == StatusChoices.PUBLISHED:
                # new status is published the check the related resource
                if request.POST.get('dataset_revision_id', False):
                    dataset_revision_id=request.POST['dataset_revision_id']
                    resource = DatasetLifeCycleManager(user = request.user.id, dataset_revision_id=dataset_revision_id)
                    if resource.dataset_revision.status != StatusChoices.PUBLISHED:
                        raise DatastreamParentNotPublishedException(resource.dataset_revision)
                elif request.POST.get('datastream_revision_id', False):
                    datastream_revision_id=request.POST['datastream_revision_id']
                    resource = DatastreamLifeCycleManager(user = request.user.id, resource_revision_id=datastream_revision_id)
                    if resource.dataset_revision.status != StatusChoices.PUBLISHED:
                        raise VisualizationParentNotPublishedException(resource.dataset_revision)
                else:
                    raise ParentNotPublishedException()

            return view_func(request, *args, **kwargs)

        return _wrapped_view
    return decorator


def requires_dataset():
    """ requiere a dataset_revision_id POST param """
    def decorator(view_func):
        """ for registred and logged user. NO redirect to login"""
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            if request.method == 'POST':
                if not request.POST.get('dataset_revision_id', request.POST.get('datastream-dataset_revision_id', None)):
                    raise DatasetRequiredException()

            return view_func(request, *args, **kwargs)

        return _wrapped_view
    return decorator


def requires_any_dataset():
    """ require account with almost one dataset """
    def decorator(view_func):
        """ for registred and logged user. NO redirect to login"""
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            dao = DatasetDBDAO()
            query, total_resources = dao.query(account_id=request.account.id, language=request.user.language)
            if total_resources == 0 or request.GET.get('test-no-datasets', False) == '1':
                raise AnyDatasetRequiredException()
            return view_func(request, *args, **kwargs)

        return _wrapped_view
    return decorator


def requires_any_datastream():
    """ require account with almost one dataset """
    def decorator(view_func):
        """ for registred and logged user. NO redirect to login"""
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            dao = DataStreamDBDAO()
            query, total_resources = dao.query(account_id=request.account.id, language=request.user.language)
            if total_resources == 0 or request.GET.get('test-no-dataviews', False) == '1':
                raise AnyDatastreamRequiredException()
            return view_func(request, *args, **kwargs)

        return _wrapped_view
    return decorator


def requires_review(a_view):
    def _wrapped_view(request, *args, **kwargs):
        if "dataset_revision_id" in kwargs:
            if DatasetRevision.objects.get(pk=kwargs["dataset_revision_id"]).is_pending_review() and \
                    request.user.is_editor():
                raise RequiresReviewException()

        if "datastream_revision_id" in kwargs:
            if DataStreamRevision.objects.get(pk=kwargs["datastream_revision_id"]).is_pending_review() and \
                    request.user.is_editor():
                raise RequiresReviewException()
                
        return a_view(request, *args, **kwargs)
    return _wrapped_view


#TODO implementar tambien
"""

requires_account_stats()
requires_dataset()
requires_datastream()
"""
