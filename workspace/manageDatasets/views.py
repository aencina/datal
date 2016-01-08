# -*- coding: utf-8 -*-
import urllib2
import logging
from django.conf import settings

from django.db import transaction
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.core.urlresolvers import reverse
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.translation import ugettext
from django.http import Http404, HttpResponse

from core.http import JSONHttpResponse
from core.shortcuts import render_to_response
from core.auth.decorators import login_required
from core.choices import *
from core.exceptions import DatasetSaveException
from core.models import DatasetRevision, Dataset
from core.templates import DefaultAnswer, DefaultDictToJson
from core.daos.datasets import DatasetDBDAO
from core.utils import DateTimeEncoder
from core.lib.datastore import active_datastore
from core.forms import MimeTypeForm
from core.signals import dataset_removed, dataset_changed, dataset_unpublished, dataset_rev_removed
from workspace.decorators import *
from workspace.templates import DatasetList
from workspace.manageDatasets.forms import *

logger = logging.getLogger(__name__)


@require_http_methods(["GET"])
def download(request, dataset_id, slug):
    """ download dataset file directly
    :param slug:
    :param dataset_id:
    :param request:
    """
    logger = logging.getLogger(__name__)

    # get public url for datastream id
    try:
        dataset_revision_id = Dataset.objects.get(pk=dataset_id).last_published_revision.id
        dataset = DatasetDBDAO().get(request.auth_manager.language, dataset_revision_id=dataset_revision_id)
    except Exception, e:
        logger.info("Can't find the dataset: %s [%s]" % (dataset_id, str(e)))
        raise Http404
    else:
        filename = dataset['filename'].encode('utf-8')
        # ensure it's a downloadable file on S3
        if dataset['end_point'][:7] != "file://":
            return HttpResponse("No downloadable file!")

        url = active_datastore.build_url(request.bucket_name, dataset['end_point'].replace("file://", ""))

        impl_type = settings.IMPL_TYPES.get(str(dataset['impl_type']))
        content_type = settings.CONTENT_TYPES.get(impl_type)
        if settings.DEBUG: logger.info('Dataset download %s -- %s -- %s -- %s -- %s' % (filename, content_type, url, dataset['impl_type'], impl_type))

        """ no funciona asi 
        redirect = HttpResponse(status=302, content_type=content_type)
        redirect['Location'] = url
        redirect['Content-Disposition'] = 'attachment; filename="{0}"'.format(filename)
        """

        redirect = HttpResponse(content_type=content_type) # si no funcionara => redirect = HttpResponse(mimetype='application/force-download')
        redirect['Content-Disposition'] = 'attachment; filename="{0}"'.format(filename)
        redir = urllib2.urlopen(url)
        status = redir.getcode()
        resp = redir.read()
        if settings.DEBUG: logger.info('REDIR %d %s -- %s' % (status, redir.geturl(), redir.info()))
        redirect.write(resp)

        return redirect


@login_required
@require_privilege("workspace.can_query_dataset")
@require_GET
def download_file(request):
    form = RequestFileForm(request.GET)

    if form.is_valid():
        dataset_revision = DatasetRevision.objects.get(pk=form.cleaned_data['dataset_revision_id'])
        try:
            response = HttpResponse(mimetype='application/force-download')
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(dataset_revision.filename.encode('utf-8'))
            response.write(urllib2.urlopen(dataset_revision.get_endpoint_full_url()).read())
        except Exception:
            logger.error(dataset_revision.end_point)
    else:
        response = dict(
            status='error',
            messages=[ugettext('URL-RETRIEVE-ERROR')]
        )

    return response


@login_required
@require_privilege("workspace.can_query_dataset")
@require_GET
def index(request):
    """ List all Datasets
    :param request:
    """
    account_domain = request.preferences['account.domain']
    ds_dao = DatasetDBDAO()
    filters = ds_dao.query_filters(account_id=request.user.account.id, language=request.user.language)
    datastream_impl_valid_choices = DATASTREAM_IMPL_VALID_CHOICES

    return render_to_response('manageDatasets/index.html', locals())


@login_required
@require_GET
def view(request, revision_id):
    account_id = request.auth_manager.account_id
    credentials = request.auth_manager
    user_id = request.auth_manager.id
    language = request.auth_manager.language
    try:
        dataset = DatasetDBDAO().get(language=language, dataset_revision_id=revision_id)
    except DatasetRevision.DoesNotExist:
        raise DatasetNotFoundException()

    datastream_impl_not_valid_choices = DATASTREAM_IMPL_NOT_VALID_CHOICES
    return render_to_response('viewDataset/index.html', locals())


@login_required
@require_privilege("workspace.can_query_dataset")
@require_GET
def filter(request, page=0, itemsxpage=settings.PAGINATION_RESULTS_PER_PAGE):
    """ filter resources
    :param itemsxpage:
    :param page:
    :param request:
    """
    bb_request = request.GET
    filters_param = bb_request.get('filters')
    filters_dict = dict()
    filter_name = ''
    sort_by = bb_request.get("sort_by",None)
    order = bb_request.get("order","asc")
    exclude = None

    if filters_param is not None and filters_param != '':
        filters = json.loads(filters_param)
        filters_dict['impl_type'] = filters.get('type')
        filters_dict['category__categoryi18n__name'] = filters.get('category')
        filters_dict['dataset__user__nick'] = filters.get('author')
        filters_dict['status'] = filters.get('status')

    if bb_request.get('page') is not None and bb_request.get('page') != '':
        page = int(bb_request.get('page'))
    if bb_request.get('q') is not None and bb_request.get('q') != '':
        filter_name = bb_request.get('q')
    if bb_request.get('itemxpage') is not None and bb_request.get('itemxpage') != '':
        itemsxpage = int(bb_request.get('itemxpage'))


    if bb_request.get('collect_type', None) is not None:
        # If File Dataset, set impl_types as valid ones. File = 0
        if bb_request.get('collect_type') in map(lambda x: str(x), COLLECT_TYPE_FILTERABLES):
            exclude = {
                'dataset__type__in': COLLECT_TYPE_FILTERABLES,
                'impl_type__in': DATASTREAM_IMPL_NOT_VALID_CHOICES
            }

    # define la forma de ordenamiento
    if sort_by:
        if sort_by == "category":
            sort_by ="category__categoryi18n__name"
        elif sort_by == "title":
            sort_by ="dataseti18n__title"
        elif sort_by == "author":
            sort_by ="dataset__user__nick"

        if order == "desc":
            sort_by = "-"+ sort_by
    else:
        # no se por que setea un orden de este tipo si no
        # se envia el parametro
        sort_by='-id'

    total_resources = request.stats['account_total_datasets']
            
    resources,total_entries = DatasetDBDAO().query(
        account_id=request.account.id,
        language=request.user.language,
        page=page,
        itemsxpage=itemsxpage,
        filters_dict = filters_dict,
        sort_by=sort_by,
        filter_name=filter_name,
        exclude=exclude
    )

    for resource in resources:
        resource['url'] = reverse('manageDatasets.view', urlconf='workspace.urls', kwargs={'revision_id': resource['id']})

    data = {'total_entries': total_entries, 'total_resources': total_resources, 'resources': resources}
    if settings.DEBUG: logger.info('filter dataset: %d, %s' % (total_entries, str(total_resources)))

    response = DatasetList().render(data)

    return HttpResponse(response, mimetype="application/json")


@login_required
@require_privilege("workspace.can_query_dataset")
@require_GET
def get_filters_json(request):
    """ List all Filters available
    :param request:
    """
    if settings.DEBUG: logger.info('GET FILTERs')
    filters = DatasetDBDAO().query_filters(account_id=request.user.account.id,
                                    language=request.user.language)
                                    
    response = DefaultDictToJson().render(data=filters) # normalize=True #TODO check
    
    return HttpResponse(response, mimetype="application/json")


@requires_review
@login_required
@require_privilege("workspace.can_delete_dataset")
@transaction.commit_on_success
def remove(request, dataset_revision_id, type="resource"):
    """ remove resource
    :param type:
    :param dataset_revision_id:
    :param request:
    """

    lifecycle = DatasetLifeCycleManager(user=request.user, dataset_revision_id=dataset_revision_id)

    if type == 'revision':
        lifecycle.remove()
        # si quedan revisiones, redirect a la ultima revision, si no quedan, redirect a la lista.
        if lifecycle.dataset.last_revision_id:
            last_revision_id = lifecycle.dataset.last_revision_id
        else:
            last_revision_id = -1

        # Send signal
        dataset_rev_removed.send_robust(sender='remove_view', id=lifecycle.dataset.id, rev_id=dataset_revision_id)

        response = DefaultAnswer().render(
            status=True,
            messages=[ugettext('APP-DELETE-DATASET-REV-ACTION-TEXT')],
            extras=[{"field": 'revision_id', "value": last_revision_id, "type": "literal"}])
        return HttpResponse(response, mimetype="application/json")
        
    else:
        lifecycle.remove(killemall=True)

        # Send signal
        dataset_removed.send_robust(sender='remove_view', id=lifecycle.dataset.id, rev_id=lifecycle.dataset_revision.id)

        response = DefaultAnswer().render(
            status=True,
            messages=[ugettext('APP-DELETE-DATASET-ACTION-TEXT')],
            extras=[{"field": 'revision_id', "value": -1, "type": "literal"}])
        return HttpResponse(response, mimetype="application/json")


@login_required
@require_privilege("workspace.can_create_dataset")
@requires_if_publish('dataset') #
@require_http_methods(['POST', 'GET'])
@transaction.commit_on_success
def create(request, collect_type='index'):

    auth_manager = request.auth_manager
    account_id = auth_manager.account_id
    language = auth_manager.language
    extensions_list = SOURCE_EXTENSION_LIST

    # TODO: Put line in a common place
    collect_types = {'index': -1, 'file': 0, 'url': 1, 'webservice': 2}

    collect_type_id = collect_types[collect_type]

    if request.method == 'GET':
        form = DatasetFormFactory(collect_type_id).create(
            account_id=account_id,
            language=language,
            status_choices=auth_manager.get_allowed_actions()
        )
        form.label_suffix = ''
        url = 'createDataset/{0}.html'.format(collect_type)
        return render_to_response(url, locals())

    elif request.method == 'POST':
        """update dataset """
        form = DatasetFormFactory(collect_type_id).create(request, account_id=account_id, language=language,
                                                          status_choices=auth_manager.get_allowed_actions())

        if form.is_valid():
            lifecycle = DatasetLifeCycleManager(user=request.user)
            dataset_revision = lifecycle.create(collect_type=request.POST.get('collect_type'), language=language,
                                                **form.cleaned_data)

            # TODO: Create a CreateDatasetResponse object
            data = dict(status='ok', messages=[ugettext('APP-DATASET-CREATEDSUCCESSFULLY-TEXT')],
                        dataset_revision_id=dataset_revision.id)
            return HttpResponse(json.dumps(data), content_type='text/plain')
        else:
            raise DatasetSaveException(form)


@login_required
@require_privilege("workspace.can_edit_dataset")
@requires_if_publish('dataset')
@requires_review
@require_http_methods(['POST', 'GET'])
@transaction.commit_on_success
def edit(request, dataset_revision_id=None):
    account_id = request.auth_manager.account_id
    auth_manager = request.auth_manager
    language = request.auth_manager.language
    user_id = request.auth_manager.id
    extensions_list = SOURCE_EXTENSION_LIST

    # TODO: Put line in a common place
    collect_types = {0: 'file', 1: 'url', 2: 'webservice'}

    # TODO: Review. Category was not loading options from form init.
    category_choices = [[category['category__id'], category['name']] for category in CategoryI18n.objects.filter(language=language, category__account=account_id).values('category__id', 'name')]

    # Get data set and the right template depending on the collected type
    dataset = DatasetDBDAO().get(language=language, dataset_revision_id=dataset_revision_id)

    initial_values = dict(
        # Dataset Form
        dataset_id=dataset.get('id'), title=dataset.get('title'), description=dataset.get('description'),
        category=dataset.get('category_id'), status=dataset.get('status'),
        notes=dataset.get('notes'), file_name=dataset.get('filename'), end_point=dataset.get('end_point'),
        impl_type=dataset.get('impl_type'), license_url=dataset.get('license_url'), spatial=dataset.get('spatial'),
        frequency=dataset.get('frequency'), mbox=dataset.get('mbox'), sources=dataset.get('sources'),
        tags=dataset.get('tags')
    )

    if request.method == 'GET':
        status_options = auth_manager.get_allowed_actions()
        url = 'editDataset/{0}.html'.format(collect_types[dataset['collect_type']])


        # Import the form that we really need
        if collect_types[dataset['collect_type']] is not 'url':
            className = [collect_types[dataset['collect_type']].capitalize(), "Form"]
        else:
            className = ['Dataset', "Form"]

        className = ''.join(str(elem) for elem in className)
        mod = __import__('workspace.manageDatasets.forms', fromlist=[className])

        form = getattr(mod, className)(status_options=status_options)
        form.label_suffix = ''
        form.fields['category'].choices = category_choices
        form.initial = initial_values

        return render_to_response(url, locals())
    elif request.method == 'POST':
        """ Update dataset """
        form = DatasetFormFactory(request.POST.get('collect_type')).create(
            request, account_id=account_id, language=language, status_choices=auth_manager.get_allowed_actions()
        )

        # Agrego los valores iniciales para que el changed_data de correctamente
        form.initial = initial_values

        if form.is_valid():
            lifecycle = DatasetLifeCycleManager(user=request.user, dataset_revision_id=dataset_revision_id)

            dataset_revision = lifecycle.edit(collect_type=request.POST.get('collect_type'),
                                              changed_fields=form.changed_data, language=language,  **form.cleaned_data)

            # Signal
            dataset_changed.send_robust(sender='edit_view', id=lifecycle.dataset.id,
                                        rev_id=lifecycle.dataset_revision.id)

            data = dict(status='ok', messages=[ugettext('APP-DATASET-CREATEDSUCCESSFULLY-TEXT')],
                        dataset_revision_id=dataset_revision.id)
            return HttpResponse(json.dumps(data), content_type='text/plain')
        else:
            raise DatasetSaveException(form)


@login_required
@require_GET
def retrieve_childs(request):
    language = request.auth_manager.language
    dataset_id = request.GET.get('dataset_id', '')

    # For now, we'll fetch datastreams
    associated_resources = DatasetDBDAO().query_childs(dataset_id=dataset_id, language=language)

    list_result = []
    for associated_resource in associated_resources['datastreams']:
        associated_resource['type'] = 'dataview'
        list_result.append(associated_resource)

    for associated_resource in associated_resources['visualizations']:
        associated_resource['type'] = 'visualization'
        list_result.append(associated_resource)

    dump = json.dumps(list_result, cls=DjangoJSONEncoder)
    return HttpResponse(dump, mimetype="application/json")


@login_required
@require_POST
@transaction.commit_on_success
def change_status(request, dataset_revision_id=None):
    """
    Change dataset status
    :param request:
    :param dataset_revision_id:
    :return: JSON Object
    """
    if dataset_revision_id:
        lifecycle = DatasetLifeCycleManager(
            user=request.user,
            dataset_revision_id=dataset_revision_id
        )
        action = request.POST.get('action')
        action = 'accept' if action == 'approve'else action # fix para poder llamar dinamicamente al metodo de lifecycle
        killemall = True if request.POST.get('killemall', False) == 'true' else False

        if action not in ['accept', 'reject', 'publish', 'unpublish', 'send_to_review']:
            raise NoStatusProvidedException()

        if action == 'unpublish':
            getattr(lifecycle, action)(killemall)
            # Signal
            dataset_unpublished.send_robust(sender='change_status_view', id=lifecycle.dataset.id,
                                            rev_id=lifecycle.dataset_revision.id)
        else:
            getattr(lifecycle, action)()

        if action == 'accept':
            title= ugettext('APP-DATASET-APPROVED-TITLE'),
            description= ugettext('APP-DATASET-APPROVED-TEXT')
        elif action == 'reject':
            title= ugettext('APP-DATASET-REJECTED-TITLE'),
            description= ugettext('APP-DATASET-REJECTED-TEXT')
        elif action == 'publish':
            title= ugettext('APP-DATASET-PUBLISHED-TITLE'),
            description= ugettext('APP-DATASET-PUBLISHED-TEXT')
        elif action == 'unpublish':
            if killemall:
                description = ugettext('APP-DATASET-UNPUBLISHALL-TEXT')
            else:
                description = ugettext('APP-DATASET-UNPUBLISH-TEXT')
            title= ugettext('APP-DATASET-UNPUBLISH-TITLE'),
        elif action == 'send_to_review':
            title= ugettext('APP-DATASET-SENDTOREVIEW-TITLE'),
            description= ugettext('APP-DATASET-SENDTOREVIEW-TEXT')

        response = dict(
            status='ok',
            messages={'title': title, 'description': description }
        )

        # Limpio un poco
        response['result'] = DatasetDBDAO().get(request.user.language, dataset_revision_id=dataset_revision_id)
        account = request.account
        msprotocol = 'https' if account.get_preference('account.microsite.https') else 'http'
        response['result']['public_url'] = msprotocol + "://" + request.preferences['account.domain'] + reverse('manageDatasets.view', urlconf='microsites.urls', 
            kwargs={'dataset_id': response['result']['dataset_id'], 'slug': '-'})
        response['result'].pop('datastreams')
        response['result'].pop('visualizations')
        response['result'].pop('tags')
        response['result'].pop('sources')

        return JSONHttpResponse(json.dumps(response, cls=DateTimeEncoder))


@login_required
@require_privilege("workspace.can_create_datastream")
@require_http_methods(["GET"])
def check_endpoint_url(request):

    mimetype_form = MimeTypeForm(request.GET)
    status = ''

    if mimetype_form.is_valid():
        url = mimetype_form.cleaned_data['url']
        mimetype, status, url = mimetype_form.get_mimetype(url)
        sources = {"mimetype" : mimetype, "status" : status, "url" : url }

        return HttpResponse(json.dumps(sources), content_type='application/json')
    else:
        raise Http404
