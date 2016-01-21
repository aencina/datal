import logging
from django.http import Http404

from core.shortcuts import render_to_response
from core.models import Dataset, DatasetRevision
from core.daos.datasets import DatasetDBDAO
from core.templatetags.core_components import permalink as get_permalink
from microsites.daos.datasets import DatasetDAO
from core.exceptions import *
from microsites.exceptions import *
from django.views.decorators.http import require_http_methods
import urllib2

logger = logging.getLogger(__name__)

def view(request, dataset_id, slug):
    """ Show dataset """
    account = request.account
    preferences = request.preferences

    try:
        dataset_orig = Dataset.objects.get(pk=dataset_id)
    except Dataset.DoesNotExist, DatasetRevision.DoesNotExist:
        logger.error('Dataset doesn\'t exists [%s|%s]' % (str(dataset_id), str(account.id)))
        raise DatasetDoesNotExist
    except Exception, e:
        logger.error('Dataset error [%s|%s]=%s' % (str(dataset_id), str(account.id), repr(e)))
        raise DatasetError

    if not dataset_orig.last_published_revision:
        logger.error('Dataset {} has no published revision'.format(dataset_id))
        raise Http404

    dataset = DatasetDBDAO().get(
        request.user,
        dataset_revision_id=dataset_orig.last_published_revision.id
    )

    return render_to_response('viewDataset/index.html', locals())

@require_http_methods(["GET"])
def download(request, dataset_id, slug):
    """ download internal dataset file """
    try:
        dataset = DatasetDBDAO().get(request.user, dataset_id=dataset_id, published=True)
    except:
        raise DatasetDoesNotExist
    else:
        try:
            response = HttpResponse(mimetype='application/force-download')
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(dataset['filename'].encode('utf-8'))
            response.write(urllib2.urlopen(dataset['end_point_full_url']).read())
        except Exception as e:
            logger.exception("Error en descarga de archivo %s" % dataset['end_point'])
        return response
