# -*- coding: utf-8 -*-
import logging
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.utils.translation import ugettext
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.core.serializers.json import DjangoJSONEncoder
from django.conf import settings
from core.shortcuts import render_to_response
from core.auth.decorators import login_required
from core.daos.datastreams import DataStreamDBDAO
from core.lifecycle.datastreams import DatastreamLifeCycleManager
from core.exceptions import DataStreamNotFoundException, DatasetNotFoundException
from core.models import DatasetRevision, Account, CategoryI18n, DataStreamRevision, Dataset
from core.http import JSONHttpResponse
from core.signals import datastream_changed, datastream_removed, datastream_unpublished, datastream_rev_removed
from core.utils import DateTimeEncoder
from workspace.decorators import *
from workspace.manageDataviews.forms import *
from workspace.templates import *
from workspace.exceptions import DatastreamSaveException

logger = logging.getLogger(__name__)


@login_required
@require_GET
def view(request, revision_id):
    language = request.auth_manager.language
    try:
        datastream = DataStreamDBDAO().get(request.user, datastream_revision_id=revision_id, published=False)
    except DataStreamRevision.DoesNotExist:
        raise DataStreamNotFoundException()

    account_id = request.auth_manager.account_id
    credentials = request.auth_manager
    categories = CategoryI18n.objects.filter(language=language, category__account=account_id).values('category__id',
                                                                                                     'name')
    status_options = credentials.get_allowed_actions()

    try:
        lifecycle = DatastreamLifeCycleManager(user=request.user, datastream_revision_id=revision_id)
        datastream['can_publish_bof_children'] = lifecycle.can_publish_bof_children()
    except Exception as e:
        pass 

    return render_to_response('viewDataStream/index.html', locals())


@login_required
@requires_any_dataset()
@require_privilege("workspace.can_query_datastream")
@require_GET
def index(request):
    """ list all dataviews
    :param request:
    """
    ds_dao = DataStreamDBDAO()
    filters = ds_dao.query_filters(account_id=request.user.account.id, language=request.user.language)

    return render_to_response('manageDataviews/index.html', locals())


@login_required
@require_GET
@require_privilege("workspace.can_query_datastream")
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
    sort_by = bb_request.get("sort_by", None)
    order = bb_request.get("order", "asc")

    if filters_param is not None and filters_param != '':
        filters = json.loads(filters_param)

        filters_dict['impl_type'] = filters.get('type')
        filters_dict['category__categoryi18n__name'] = filters.get('category')
        filters_dict['datastream__user__nick'] = filters.get('author')
        filters_dict['status'] = filters.get('status')

    if bb_request.get('page') is not None and bb_request.get('page') != '':
        page = int(bb_request.get('page'))
    if bb_request.get('itemxpage') is not None and bb_request.get('itemxpage') != '':
        itemsxpage = int(bb_request.get('itemxpage'))
    if bb_request.get('q') is not None and bb_request.get('q') != '':
        filter_name = bb_request.get('q')

    if sort_by:
        if sort_by == "title":
            sort_by = "datastreami18n__title"
        elif sort_by == "dataset_title":
            sort_by = "dataset__last_revision__dataseti18n__title"
        elif sort_by == "author":
            sort_by = "datastream__user__nick"

        if order == "desc":
            sort_by = "-" + sort_by
    else:
        # no se por que setea un orden de este tipo si no
        # se envia el parametro
        sort_by = '-id'

    total_resources = request.stats['account_total_datastreams']

    resources, total_entries = DataStreamDBDAO().query(
        account_id=request.account.id,
        language=request.user.language,
        page=page,
        itemsxpage=itemsxpage,
        filters_dict=filters_dict,
        sort_by=sort_by,
        filter_name=filter_name
    )

    for resource in resources:
        resource['url'] = reverse('manageDataviews.view', urlconf='workspace.urls',
                                  kwargs={'revision_id': resource['id']})
        resource['dataset_url'] = reverse('manageDatasets.view', urlconf='workspace.urls',
                                          kwargs={'revision_id': resource['dataset__last_revision__id']})

    data = {'total_entries': total_entries, 'total_resources': total_resources, 'resources': resources,
            'total_entries': total_entries}
    response = DatastreamList().render(data)

    return JSONHttpResponse(response)


@login_required
@require_privilege("workspace.can_query_dataset")
@require_GET
def get_filters_json(request):
    """ List all Filters available
    :param request:
    """
    filters = DataStreamDBDAO().query_filters(account_id=request.user.account.id, language=request.user.language)
    return JSONHttpResponse(json.dumps(filters))


@login_required
@require_GET
def retrieve_childs(request):
    language = request.auth_manager.language
    revision_id = request.GET.get('datastream_id', '')
    associated_visualizations = DataStreamDBDAO().query_childs(datastream_id=revision_id, language=language)[
        'visualizations']

    list_result = []
    for associated_visualization in associated_visualizations:
        associated_visualization['type'] = 'visualization'
        list_result.append(associated_visualization)

    dump = json.dumps(list_result, cls=DjangoJSONEncoder)
    return HttpResponse(dump, content_type="application/json")


@login_required
@require_privilege("workspace.can_delete_datastream")
@requires_review
@transaction.commit_on_success
def remove(request, datastream_revision_id, type="resource"):
    """ remove resource
    :param type:
    :param datastream_revision_id:
    :param request:
    """
    lifecycle = DatastreamLifeCycleManager(user=request.user, datastream_revision_id=datastream_revision_id)
    resource_id = lifecycle.datastream.id

    if type == 'revision':
        lifecycle.remove()
        # si quedan revisiones, redirect a la ultima revision, si no quedan, redirect a la lista.
        if lifecycle.datastream.last_revision_id:
            last_revision_id = lifecycle.datastream.last_revision.id
        else:
            last_revision_id = -1

        # Send signal
        datastream_removed.send_robust(sender='remove_view', id=resource_id, rev_id=datastream_revision_id)

        return JSONHttpResponse(json.dumps({
            'status': True,
            'messages': [ugettext('APP-DELETE-DATASTREAM-REV-ACTION-TEXT')],
            'revision_id': last_revision_id,
        }))

    else:
        lifecycle.remove(killemall=True)

        # Send signal
        datastream_removed.send_robust(sender='remove_view', id=lifecycle.datastream.id, rev_id=-1)

        return HttpResponse(json.dumps({
            'status': True,
            'messages': [ugettext('APP-DELETE-DATASTREAM-ACTION-TEXT')],
            'revision_id': -1,
        }), content_type='text/plain')


@login_required
@require_http_methods(['POST', 'GET'])
@require_privilege("workspace.can_create_datastream")
@requires_dataset()
@requires_published_parent()
@transaction.commit_on_success
def create(request):
    auth_manager = request.auth_manager
    if request.method == 'POST':
        """ save new or update dataset """
        form = CreateDataStreamForm(request.POST)

        if not form.is_valid():
            raise DatastreamSaveException(form)

        dataset_revision = DatasetRevision.objects.get(pk=form.cleaned_data['dataset_revision_id'])

        if dataset_revision.size > settings.MAX_DATASTREAM_SIZE:
            raise DatasetTooBigException(size=settings.MAX_DATASTREAM_SIZE)

        dataview = DatastreamLifeCycleManager(user=request.user)
        dataview.create(
            dataset=dataset_revision.dataset,
            language=request.auth_manager.language,
            category_id=form.cleaned_data['category'],
            **form.cleaned_data
        )

        response = dict(
            status='ok',
            datastream_revision_id=dataview.datastream_revision.id,
            messages=[ugettext('APP-DATASET-CREATEDSUCCESSFULLY-TEXT')]
        )

        return JSONHttpResponse(json.dumps(response))

    elif request.method == 'GET':
        form = InitalizeCollectForm(request.GET)

        if form.is_valid():
            is_update = False
            is_update_selection = False
            data_set_id = form.cleaned_data['dataset_revision_id']
            datastream_id = None

            if auth_manager.is_level('level_5'):
                meta_data = Account.objects.get(pk=auth_manager.account_id).meta_data

            try:
                dataset_revision = DatasetRevision.objects.get(pk=data_set_id)
            except DatasetRevision.DoesNotExist:
                raise DatasetNotFoundException()

            end_point = dataset_revision.end_point
            type = dataset_revision.dataset.type
            impl_type = dataset_revision.impl_type
            impl_details = dataset_revision.impl_details
            bucket_name = request.bucket_name

            categoriesQuery = CategoryI18n.objects\
                                .filter(language=request.auth_manager.language,
                                        category__account=request.auth_manager.account_id)\
                                .values('category__id', 'name')
            categories = [[category['category__id'], category['name']] for category in categoriesQuery]
            preferences = auth_manager.get_account().get_preferences()
            try:
                default_category = int(preferences['account.default.category'])
            except:
                default_category = categories[0][0]
            # Agregar categoria por defecto
            categories = map(lambda x: x + [int(x[0]) == default_category], categories)

            sources = [source for source in dataset_revision.get_sources()]
            tags = [tag for tag in dataset_revision.get_tags()]

            return render_to_response('createDataview/index.html', locals())
        else:
            raise Http404


@login_required
@require_http_methods(['POST', 'GET'])
@require_privilege("workspace.can_edit_datastream")
@requires_published_parent()
@requires_review
@transaction.commit_on_success
def edit(request, datastream_revision_id=None):
    lifecycle = DatastreamLifeCycleManager(user=request.user, datastream_revision_id=datastream_revision_id)
    dao= DataStreamDBDAO().get(request.user, datastream_revision_id=datastream_revision_id)
    auth_manager = request.auth_manager
    
    if request.method == 'GET':
        is_update = True
        is_update_selection = True
        dataset_revision = Dataset.objects.get(id=dao['dataset_id']).last_revision
        datastream_id = None

        if auth_manager.is_level('level_5'):
            meta_data = Account.objects.get(pk=auth_manager.account_id).meta_data

        end_point = dataset_revision.end_point
        type = dataset_revision.dataset.type
        impl_type = dataset_revision.impl_type
        impl_details = dataset_revision.impl_details
        bucket_name = request.bucket_name

        categoriesQuery = CategoryI18n.objects\
                            .filter(language=request.auth_manager.language,
                                    category__account=request.auth_manager.account_id)\
                            .values('category__id', 'name')
        categories = [[category['category__id'], category['name']] for category in categoriesQuery]
        preferences = auth_manager.get_account().get_preferences()
        try:
            default_category = int(preferences['account.default.category'])
        except:
            default_category = categories[0][0]
        # Agregar categoria por defecto
        categories = map(lambda x: x + [int(x[0]) == default_category], categories)

        sources = [source for source in dataset_revision.get_sources()]
        tags = [tag for tag in dataset_revision.get_tags()]


        return render_to_response('createDataview/index.html', locals())
        
    elif request.method == 'POST':
        """update dataset """

        form = EditDataStreamForm(request.POST)

        if not form.is_valid():
            raise DatastreamSaveException(form)

        if form.is_valid():
            lifecycle = DatastreamLifeCycleManager(user=request.user, datastream_revision_id=datastream_revision_id)

            lifecycle.edit(
                language=request.auth_manager.language,
                changed_fields=form.changed_data,
                **form.cleaned_data
            )

            # Signal
            datastream_changed.send_robust(sender='edit_view', id=lifecycle.datastream.id,
                                           rev_id=lifecycle.datastream_revision.id)

            response = dict(
                status='ok',
                datastream_revision_id=lifecycle.datastream_revision.id,
                messages=[ugettext('APP-DATASET-CREATEDSUCCESSFULLY-TEXT')],
            )

            return JSONHttpResponse(json.dumps(response))


@login_required
@require_POST
@transaction.commit_on_success
def change_status(request, datastream_revision_id=None):
    """
    Change dataview status
    :param request:
    :param datastream_revision_id:
    :return: JSON Object
    """
    if datastream_revision_id:
        lifecycle = DatastreamLifeCycleManager(
            user=request.user,
            datastream_revision_id=datastream_revision_id
        )
        action = request.POST.get('action')
        action = 'accept' if action == 'approve'else action # fix para poder llamar dinamicamente al metodo de lifecycle
        killemall = True if request.POST.get('killemall', False) == 'true' else False

        if action not in ['accept', 'reject', 'publish', 'unpublish', 'send_to_review', 'publish_all']:
            raise NoStatusProvidedException()

        if action == 'unpublish':
            getattr(lifecycle, action)(killemall)
            # Signal
            datastream_unpublished.send_robust(sender='change_status_view', id=lifecycle.datastream.id,
                                               rev_id=lifecycle.datastream_revision.id)
        elif action == 'publish_all':
            getattr(lifecycle, 'publish')(accept_children=True)
        else:
            getattr(lifecycle, action)()

        if action == 'accept':
            title = ugettext('APP-DATAVIEW-APPROVED-TITLE'),
            description = ugettext('APP-DATAVIEW-APPROVED-TEXT')
        elif action == 'reject':
            title = ugettext('APP-DATAVIEW-REJECTED-TITLE'),
            description = ugettext('APP-DATAVIEW-REJECTED-TEXT')
        elif action == 'publish':
            title = ugettext('APP-DATAVIEW-PUBLISHED-TITLE'),
            description = ugettext('APP-DATAVIEW-PUBLISHED-TEXT')
        elif action == 'unpublish':
            if killemall:
                description = ugettext('APP-DATAVIEW-UNPUBLISHALL-TEXT')
            else:
                description = ugettext('APP-DATAVIEW-UNPUBLISH-TEXT')
            title = ugettext('APP-DATAVIEW-UNPUBLISH-TITLE'),
        elif action == 'send_to_review':
            title = ugettext('APP-DATAVIEW-SENDTOREVIEW-TITLE'),
            description = ugettext('APP-DATAVIEW-SENDTOREVIEW-TEXT')
        elif action == 'publish_all':
            title= ugettext('APP-DATASTREAM-PUBLISHALL-TITLE'),
            description= ugettext('APP-DATASTREAM-PUBLISHALL-TEXT')

        response = dict(
            status='ok',
            messages={'title': title, 'description': description }
        )

        # Limpio un poco
        response['result'] = DataStreamDBDAO().get(request.user, datastream_revision_id=datastream_revision_id)
        account = request.account
        msprotocol = 'https' if account.get_preference('account.microsite.https') else 'http'
        response['result']['public_url'] = msprotocol + "://" + request.preferences['account.domain'] + reverse('viewDataStream.view', urlconf='microsites.urls', 
            kwargs={'id': response['result']['datastream_id'], 'slug': '-'})
        response['result'].pop('parameters')
        response['result'].pop('tags')
        response['result'].pop('sources')

        return JSONHttpResponse(json.dumps(response, cls=DateTimeEncoder))
