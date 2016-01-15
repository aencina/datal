from django import template
from core.models import *
from core.daos.datastreams import DataStreamDBDAO
from django.conf import settings
from core.choices import *
from core.forms import MetaForm
from workspace.manageDataviews.forms import CreateDataStreamForm

register = template.Library()


def workspace_open_data_metrics(auth_manager):
    from core.cache import Cache
    from datetime import date, timedelta
    from django.db import connection
    cursor = connection.cursor()

    user_id = auth_manager.id
    account_id = auth_manager.account_id
    language = auth_manager.language

    last_7_days = date.today() - timedelta(days=7)
    c = Cache(db=0)

    published_datasets = c.get('published_datasets_' + str(account_id))
    if not published_datasets:
        cursor.execute("SELECT COUNT(1) as val FROM ao_datasets d JOIN ao_users u ON u.id=d.user_id JOIN ao_accounts ac ON u.account_id=ac.id WHERE ac.id = %s and EXISTS(SELECT * FROM ao_dataset_revisions b WHERE b.dataset_id = d.id AND NOT EXISTS(SELECT * FROM ao_dataset_revisions c WHERE c.created_at > b.created_at AND c.status = 4 AND b.dataset_id = c.dataset_id) AND b.status = 3)", [str(account_id)])
        row = cursor.fetchone()
        published_datasets = row[0]
        c.set('published_datasets_' + str(account_id), published_datasets, settings.REDIS_STATS_TTL)

    total_datasets = c.get('total_datasets_' + str(account_id))
    if not total_datasets:
        total_datasets = Dataset.objects.filter(user__account=account_id).count()
        c.set('total_datasets_' + str(account_id), total_datasets, settings.REDIS_STATS_TTL)

    published_datastreams = c.get('published_datastreams_' + str(account_id))
    if not published_datastreams:
        cursor.execute("SELECT COUNT(1) as val FROM ao_datastreams d JOIN ao_users u ON u.id=d.user_id JOIN ao_accounts ac ON u.account_id=ac.id WHERE ac.id = %s and EXISTS(SELECT * FROM ao_datastream_revisions b WHERE b.datastream_id = d.id AND NOT EXISTS(SELECT * FROM ao_datastream_revisions c WHERE c.created_at > b.created_at AND c.status = 4 AND b.datastream_id = c.datastream_id) AND b.status = 3)", [str(account_id)])
        row = cursor.fetchone()
        published_datastreams = row[0]
        c.set('published_datastreams_' + str(account_id), published_datastreams, settings.REDIS_STATS_TTL)

    total_datastreams = c.get('total_datastreams_' + str(account_id))
    if not total_datastreams:
        total_datastreams = DataStream.objects.filter(user__account=account_id).count()
        c.set('total_datastreams_' + str(account_id), total_datastreams, settings.REDIS_STATS_TTL)

    published_visualizations = c.get('published_visualizations_' + str(account_id))
    if not published_visualizations:
        cursor.execute("SELECT COUNT(1) as val FROM ao_visualizations d JOIN ao_users u ON u.id=d.user_id JOIN ao_accounts ac ON u.account_id=ac.id WHERE ac.id = %s and EXISTS(SELECT * FROM ao_visualizations_revisions b WHERE b.visualization_id = d.id AND NOT EXISTS(SELECT * FROM ao_visualizations_revisions c WHERE c.created_at > b.created_at AND c.status = 4 AND b.visualization_id = c.visualization_id) AND b.status = 3)", [str(account_id)])
        row = cursor.fetchone()
        published_visualizations = row[0]
        c.set('published_visualizations_' + str(account_id), published_visualizations, settings.REDIS_STATS_TTL)

    total_visualizations = c.get('total_visualizations_' + str(account_id))
    if not total_visualizations:
        total_visualizations = Visualization.objects.filter(user__account=account_id).count()
        c.set('total_visualizations_' + str(account_id), total_visualizations, settings.REDIS_STATS_TTL)

    return locals()

register.inclusion_tag('viewLandingPage/workspace_data_metrics.html')(workspace_open_data_metrics)


def get_activity_type(activity):

    from core.choices import ActionStreams
    
    activity_name=""

    # 0 - CREATE
    if int(activity) == (ActionStreams.CREATE):
        activity_name = ugettext_lazy('LANDINGPAGE-ACTIVITY-HASCREATED')
    # 1 - DELETE
    elif int(activity) == int(ActionStreams.DELETE):
        activity_name = ugettext_lazy('LANDINGPAGE-ACTIVITY-HASDELETED')
    # 2 - PUBLISH
    elif int(activity) == int(ActionStreams.PUBLISH):
        activity_name = ugettext_lazy('LANDINGPAGE-ACTIVITY-HASPUBLISHED')
    # 3 - UNPUBLISH
    elif int(activity) == int(ActionStreams.UNPUBLISH):
        activity_name = ugettext_lazy('LANDINGPAGE-ACTIVITY-HASUNPUBLISHED')
    # 4 - REJECT
    elif int(activity) == int(ActionStreams.REJECT):
        activity_name = ugettext_lazy('LANDINGPAGE-ACTIVITY-HASREJECTED')
    # 5 - ACCEPT
    elif int(activity) == int(ActionStreams.ACCEPT):
        activity_name = ugettext_lazy('LANDINGPAGE-ACTIVITY-HASACCEPTED')
    # 6 - REVIEW
    elif int(activity) == int(ActionStreams.REVIEW):
        activity_name = ugettext_lazy('LANDINGPAGE-ACTIVITY-HASSENTTOREVIEW')
    # 7 - EDIT
    elif int(activity) == int(ActionStreams.EDIT):
        activity_name = ugettext_lazy('LANDINGPAGE-ACTIVITY-HASEDITED')

    return activity_name

register.assignment_tag(get_activity_type)
