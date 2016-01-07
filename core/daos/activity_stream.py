# -*- coding: utf-8 -*-
from core import choices
from core.cache import Cache
from django.conf import settings
from core.models import User
from core import http as LocalHelper
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext
from core.plugins_point import DatalPluginPoint
import redis
import datetime
import logging


logger = logging.getLogger(__name__)


class ActivityStreamDAO:
    """ class for integrated managment of resource ativities """

    def create(self, account_id, user_id, revision_id, resource_type, resource_id, action_id, resource_title, resource_category):
        """ Create a redis-hash and then addit to a redis-lits"""
        if settings.DEBUG: logger.info('Create ActivityStreamDAO %d %s' % (action_id, resource_title))
        c = Cache(db=settings.CACHE_DATABASES['activity_resources'])

        timeformat = "%s %s %s %s" % (ugettext('APP-ON-TEXT'), "%Y-%m-%d,", ugettext('APP-AT-TEXT'), "%H:%M")
        now = datetime.datetime.now()
        time = now.strftime(timeformat)
        l_permalink=""

        #TODO check and fix al urls.
        if int(action_id) != int(choices.ActionStreams.DELETE):
            if resource_type == settings.TYPE_DATASTREAM:
                l_permalink = reverse('manageDataviews.view', urlconf='workspace.urls',
                                      kwargs={'revision_id': revision_id})
            elif resource_type == settings.TYPE_VISUALIZATION:
                l_permalink = reverse('manageVisualizations.view', urlconf='workspace.urls',
                                      kwargs={'revision_id': revision_id})
            elif resource_type == settings.TYPE_DATASET:
                l_permalink = reverse('manageDatasets.view', urlconf='workspace.urls',
                                      kwargs={'revision_id': revision_id})
            else:
                for plugin in DatalPluginPoint.get_plugins():
                    if (plugin.is_active() and hasattr(plugin, 'doc_type') and 
                        plugin.doc_type == resource_type and 
                        hasattr(plugin, 'workspace_permalink')):
                        l_permalink = plugin.workspace_permalink(revision_id)
            
        list_key = 'activity_stream::%s' % str(account_id)
        n=c.incr("%s_counter" % list_key) # count any use of the list indexing hash and never repeat an ID
        activity_key = 'activity.stream_%s:%s' % (str(account_id), str(n))
        activity_value = {"user_id": user_id, "revision_id": revision_id
                        , "type": resource_type, "resource_id": resource_id
                        ,"action_id": action_id
                        , "title": resource_title, "time":time
                        , "resource_link": l_permalink
                        , "category": resource_category }

        r1 = c.hmset(activity_key, activity_value)
        r2 = c.lpush(str(list_key), activity_key)
        if settings.DEBUG: logger.info('Saved ActivityStreamDAO {} {} {} {} {}'.format(str(r1), str(r2), list_key, activity_key, activity_value))
        return list_key, activity_key, activity_value

    def query(self, account_id, limit=21):
        """ query for last 20 records of activity lists"""
        if settings.DEBUG: logger.info('Query ActivityStreamDAO %d' % account_id)

        c = Cache(db=settings.CACHE_DATABASES['activity_resources'])
        list_key = 'activity_stream::%s' % str(account_id)
        activity_keys = c.lrange(str(list_key),0, limit)
        r = redis.Redis(host=settings.REDIS_READER_HOST, port=settings.REDIS_PORT,
            db=settings.CACHE_DATABASES['activity_resources'])
        pipeline=r.pipeline()

        for key in activity_keys:
            pipeline.hgetall(key)
        activities = []
        users = {} # avoid duplicated sql queries
        for h in pipeline.execute():
            user_id = h.get('user_id', None)
            if user_id:
                if not users.get(user_id, None):
                    user = User.objects.get(pk=user_id)
                    users[user_id] = user
                else:
                    user = users[user_id]
                h['user_nick'] = user.nick
                h['user_email'] = user.email
                h['user_name'] = user.name
                
                activities.append(h)

        # if settings.DEBUG: logger.info('Returned activities %s' % str(activities))
        return activities
