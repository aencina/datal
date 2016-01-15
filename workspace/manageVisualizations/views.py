# -*- coding: utf-8 -*-
import json
import urllib

from django.http import HttpResponse
from django.db import transaction
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.template.loader import render_to_string
from django.utils.translation import ugettext


from core.http import JSONHttpResponse
from core.shortcuts import render_to_response
from core.auth.decorators import login_required,privilege_required
from core.helpers import RequestProcessor
from core.utils import DateTimeEncoder
from core.choices import *
from core.models import VisualizationRevision
from core.daos.visualizations import VisualizationDBDAO
from core.lifecycle.visualizations import VisualizationLifeCycleManager
from core.exceptions import VisualizationNotFoundException
from core.exceptions import DataStreamNotFoundException
from core.signals import visualization_changed, visualization_removed, visualization_unpublished, \
    visualization_rev_removed
from workspace.manageVisualizations import forms
from workspace.decorators import *
from .forms import VisualizationForm, ViewChartForm

logger = logging.getLogger(__name__)


@login_required
@requires_any_datastream()
@require_GET
def index(request):
    """ list all dataviews
    :param request:
    """
    dao = VisualizationDBDAO()

    resources, total_resources = dao.query(account_id=request.account.id, language=request.user.language)

    for resource in resources:
        resource['url'] = reverse('manageVisualizations.view', urlconf='workspace.urls', kwargs={'revision_id': resource['id']})

    filters = dao.query_filters(account_id=request.user.account.id,
                                    language=request.user.language)

    return render_to_response('manageVisualizations/index.html', locals())


@login_required
@require_GET
@require_privilege("workspace.can_query_visualization")
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
        filters_dict['visualization__user__nick'] = filters.get('author')
        filters_dict['status'] = filters.get('status')

    if bb_request.get('page') is not None and bb_request.get('page') != '':
        page = int(bb_request.get('page'))
    if bb_request.get('q') is not None and bb_request.get('q') != '':
        filter_name = bb_request.get('q')
    if bb_request.get('itemxpage') is not None and bb_request.get('itemxpage') != '':
        itemsxpage = int(bb_request.get('itemxpage'))


    if sort_by:
        if sort_by == "title":
            sort_by ="visualizationi18n__title"
        elif sort_by == "dataset_title":
            sort_by ="visualization__datastream__datastreamrevision__dataset__datasetrevision__dataseti18n__title"
        elif sort_by == "author":
            sort_by ="visualization__user__nick"

        if order=="desc":
            sort_by = "-"+ sort_by
    else:
        sort_by='-id'

    total_resources = request.stats['account_total_visualizations']

    resources,total_entries = VisualizationDBDAO().query(
        account_id=request.account.id,
        language=request.user.language,
        page=page,
        itemsxpage=itemsxpage,
        filters_dict=filters_dict,
        sort_by=sort_by,
        filter_name=filter_name
    )

    for resource in resources:
        resource['url'] = reverse('manageVisualizations.view', kwargs=dict(revision_id=resource['id']))
        resource['datastream_url'] = reverse('manageDataviews.view', kwargs={'revision_id': resource['visualization__datastream__last_revision__id']})

    data = render_to_string('manageVisualizations/visualization_list.json', dict(items=resources, total_entries=total_entries, total_resources=total_resources))
    return HttpResponse(data, mimetype="application/json")


@login_required
@require_privilege("workspace.can_delete_visualization")
@requires_review
@transaction.commit_on_success
def remove(request, visualization_revision_id, type="resource"):
    """ remove resource
    :param type:
    :param visualization_revision_id:
    :param request:
    """
    lifecycle = VisualizationLifeCycleManager(user=request.user, visualization_revision_id=visualization_revision_id)

    if type == 'revision':
        lifecycle.remove()
        # si quedan revisiones, redirect a la ultima revision, si no quedan, redirect a la lista.
        if lifecycle.visualization.last_revision_id:
            last_revision_id = lifecycle.visualization.last_revision_id
        else:
            last_revision_id = -1

        # Send signal
        visualization_rev_removed.send_robust(sender='remove_view', id=lifecycle.visualization.id,
                                       rev_id=visualization_revision_id)

        return JSONHttpResponse(json.dumps({
            'status': True,
            'messages': [ugettext('APP-DELETE-VISUALIZATION-REV-ACTION-TEXT')],
            'revision_id': last_revision_id
        }))
        
    else:
        lifecycle.remove(killemall=True)

        # Send signal
        visualization_removed.send_robust(sender='remove_view', id=lifecycle.visualization.id,
                                   rev_id=lifecycle.visualization_revision.id)

        return HttpResponse(json.dumps({
            'status': True,
            'messages': [ugettext('APP-DELETE-VISUALIZATION-ACTION-TEXT')],
            'revision_id': -1,
        }), content_type='text/plain')


@login_required
@require_POST
@transaction.commit_on_success
def change_status(request, visualization_revision_id=None):
    """
    Change visualization status
    :param request:
    :param visualization_revision_id:
    :return: JSON Object
    """
    if visualization_revision_id:
        lifecycle = VisualizationLifeCycleManager(
            user=request.user,
            visualization_revision_id=visualization_revision_id
        )
        action = request.POST.get('action')
        action = 'accept' if action == 'approve'else action # fix para poder llamar dinamicamente al metodo de lifecycle
        killemall = True if request.POST.get('killemall', False) == 'true' else False

        if action not in ['accept', 'reject', 'publish', 'unpublish', 'send_to_review']:
            raise NoStatusProvidedException()

        if action == 'unpublish':
            getattr(lifecycle, action)(killemall)
            # Signal
            visualization_unpublished.send_robust(sender='change_status_view', id=lifecycle.visualization.id,
                                                  rev_id=lifecycle.visualization_revision.id)
        else:
            getattr(lifecycle, action)()

        if action == 'accept':
            title = ugettext('APP-VISUALIZATION-APPROVED-TITLE'),
            description = ugettext('APP-VISUALIZATION-APPROVED-TEXT')
        elif action == 'reject':
            title = ugettext('APP-VISUALIZATION-REJECTED-TITLE'),
            description = ugettext('APP-VISUALIZATION-REJECTED-TEXT')
        elif action == 'publish':
            title = ugettext('APP-VISUALIZATION-PUBLISHED-TITLE'),
            description = ugettext('APP-VISUALIZATION-PUBLISHED-TEXT')
        elif action == 'unpublish':
            title = ugettext('APP-VISUALIZATION-UNPUBLISH-TITLE'),
            description = ugettext('APP-VISUALIZATION-UNPUBLISH-TEXT')
        elif action == 'send_to_review':
            title = ugettext('APP-VISUALIZATION-SENDTOREVIEW-TITLE'),
            description = ugettext('APP-VISUALIZATION-SENDTOREVIEW-TEXT')

        response = dict(
            status='ok',
            messages={'title': title, 'description': description }
        )

        # Limpio un poco
        response['result'] = VisualizationDBDAO().get(request.user.language, visualization_revision_id=visualization_revision_id)
        account = request.account
        msprotocol = 'https' if account.get_preference('account.microsite.https') else 'http'
        response['result']['public_url'] = msprotocol + "://" + request.preferences['account.domain'] + reverse('chart_manager.view', urlconf='microsites.urls', 
            kwargs={'id': response['result']['visualization_id'], 'slug': '-'})
        response['result'].pop('parameters')
        response['result'].pop('tags')
        response['result'].pop('sources')
        response['result'].pop('visualization')

        return JSONHttpResponse(json.dumps(response, cls=DateTimeEncoder))

@login_required
@require_http_methods(['POST','GET'])
@require_privilege("workspace.can_create_visualization")
@requires_published_parent()
@transaction.commit_on_success
def create(request):
    
    if request.method == 'GET':
        datastream_revision_id = request.GET.get('datastream_revision_id', None)
        try:
            datastream_rev = DataStreamDBDAO().get(
                request.user.language,
                datastream_revision_id=datastream_revision_id,
                published=False
            )
        except DataStreamRevision.DoesNotExist:
            raise DataStreamNotFoundException()

        return render_to_response('createVisualization/index.html', dict(
            request=request,
            datastream_revision=datastream_rev
        ))

    elif request.method == 'POST':
        """ save new or update dataset """
        # Valido que llegue el ID de la revision del datastream
        datastream_rev_id = request.GET.get('datastream_revision_id', None)
        if not datastream_rev_id:
            raise Http404
        datastream_rev = DataStreamRevision.objects.get(pk=datastream_rev_id)

        # Formulario
        form = VisualizationForm(request.POST)
        if not form.is_valid():
            logger.info(form._errors)
            raise VisualizationSaveException('Invalid form data: %s' % str(form.errors.as_text()))

        response = form.save(request, datastream_rev=datastream_rev)

        return JSONHttpResponse(json.dumps(response))
    

@login_required
@require_GET
def retrieve_childs(request):
    visualization_revision_id = request.GET.get('revision_id', '')
    visualization_id = request.GET.get('visualization_id', '')
    visualizations = VisualizationDBDAO().query_childs(
        visualization_id=visualization_id,
        language=request.auth_manager.language
    )

    list_result = [associated_visualization for associated_visualization in visualizations]
    return HttpResponse(json.dumps(list_result), mimetype="application/json")


@login_required
@require_GET
def view(request, revision_id):

    try:
        visualization_revision = VisualizationDBDAO().get(
            request.auth_manager.language,
            visualization_revision_id=revision_id
        )
    except VisualizationRevision.DoesNotExist:
        logger.info("VisualizationRevision ID %s does not exist" % revision_id)
        raise VisualizationNotFoundException()

    return render_to_response('viewVisualization/index.html', locals())


@login_required
@require_http_methods(['POST', 'GET'])
@require_privilege("workspace.can_edit_datastream")
@requires_published_parent()
@requires_review
@transaction.commit_on_success
def edit(request, revision_id=None):
    if request.method == 'GET':
        visualization_rev = VisualizationDBDAO().get(
            request.auth_manager.language,
            visualization_revision_id=revision_id
        )
        datastream_rev = DataStreamDBDAO().get(
            request.auth_manager.language,
            datastream_revision_id=visualization_rev['datastream_revision_id'])
        return render_to_response('createVisualization/index.html', dict(
            request=request,
            datastream_revision=datastream_rev,
            visualization_revision=visualization_rev
        ))

    elif request.method == 'POST':
        """ save new or update dataset """
        # Formulario
        form = VisualizationForm(request.POST)
        if not form.is_valid():
            logger.info(form.errors)
            raise VisualizationSaveException('Invalid form data: %s' % str(form.errors.as_text()))

        visualization_rev = VisualizationDBDAO().get(
            request.auth_manager.language,
            visualization_revision_id=revision_id
        )
        response = form.save(request, visualization_rev=visualization_rev)

        # Signal
        visualization_changed.send_robust(sender='edit_view', id=visualization_rev['visualization_id'],
                                          rev_id=visualization_rev['visualization_revision_id'])

        return JSONHttpResponse(json.dumps(response))

@login_required
@require_privilege("workspace.can_query_visualization")
@require_GET
def get_filters_json(request):
    """ List all Filters available
    :param request:
    """
    filters = VisualizationDBDAO().query_filters(account_id=request.user.account.id, language=request.user.language)
    return JSONHttpResponse(json.dumps(filters))
