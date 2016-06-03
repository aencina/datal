import logging
from django.http import Http404

from core.shortcuts import render_to_response
from core.models import Dataset, DatasetRevision
from core.daos.datasets import DatasetDBDAO
from core.templatetags.core_components import permalink as get_permalink
from core.exceptions import *
from microsites.exceptions import *
from core import choices
from core.decorators import has_preference
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods
from django.core.exceptions import PermissionDenied

import urllib2

logger = logging.getLogger(__name__)

@has_preference("account.dataset.show")
def view(request, dataset_id, slug):
    """ Show dataset """
    account = request.account
    preferences = request.preferences

    dataset = DatasetDBDAO().get(request.user, dataset_id=dataset_id, published=True)

    if request.GET.get('embedded', False) == 'true':
        return render_to_response('viewDataset/embedded.html', locals())
    else:
        return render_to_response('viewDataset/index.html', locals())

@has_preference("account.dataset.download")
@require_http_methods(["GET"])
def download(request, dataset_id, slug):
    """ download internal dataset file """
    try:
        dataset = DatasetDBDAO().get(request.user, dataset_id=dataset_id, published=True)
    except:
        raise DatasetDoesNotExist
    else:
        if dataset['collect_type'] == choices.CollectTypeChoices.SELF_PUBLISH:
            try:
                return redirect(dataset['end_point_full_url'])
            except Exception as e:
                logger.exception("Error en descarga de archivo %s" % dataset['end_point_full_url'])
        elif dataset['collect_type'] == choices.CollectTypeChoices.URL:
            try:
                return redirect(dataset['end_point'])
            except Exception as e:
                logger.exception("Error en descarga de archivo %s" % dataset['end_point'])
        raise PermissionDenied 
