# -*- coding: utf-8 -*-
import memcache, logging

from django.conf import settings

from core import choices
from core.models import Preference

logger = logging.getLogger(__name__)

class Preferences():
    """ 
    account's preferences. 
    In database always use '.' as separator, never '_'
    """ 
    
    def __init__(self, account_id):
        self.data = dict()
        self.data['account.id'] = account_id
        self.memcached = settings.MEMCACHED_ENGINE_END_POINT
        self.engine_cache = False
        if self.memcached:
            try:
                self.engine_cache = memcache.Client(self.memcached, debug=0)
            except:
                #TODO raise an memcache error (?)
                logger.error('No memcached client could be created')

    def __getitem__(self, key):
        """ get item from internal data, or cache or readed from database """
        key = key.replace('_', '.')
        
        if not self.data.has_key(key):
            # try from memcache
            value = self.get_from_cache(key)
            if value is not None:
                self.data[key] = value
            else:
                # then try from database
                try:
                    self.data[key] = Preference.objects.get_value_by_account_id_and_key(
                        self.data['account.id'],
                        key=key
                    )
                    #if settings.DEBUG: logger.info('Get from DB %s=%s' % (key, self.data[key]))
                except Preference.DoesNotExist:
                    self.data[key] = ''
                else:
                    self.save_on_cache(str(key), self.data[key])

        # fix booleans
        if type(self.data[key]) == str or type(self.data[key]) == unicode:
            pref = self.data[key].lower()
            if pref in ['true', 'on']:
                self.data[key] = True
            elif pref in ['false', 'off']:
                self.data[key] = False
            
        return self.data[key] 

    def load(self, keys):
        preferences = Preference.objects.filter(key__in=keys, account_id=self.data['account.id']).values('key', 'value')
        for preference in preferences:
            key = preference['key']

            # fix booleans
            if type(preference['value']) == str or type(preference['value']) == unicode:
                pref = preference['value'].lower()
                if pref in ['true', 'on']:
                    preference['value'] = True
                elif pref in ['false', 'off']:
                    preference['value'] = False
                
            self.data[key.replace('_', '.')] = preference['value']
            try:
                keys.remove(key)
            except ValueError:
                logger.error("[load preferences] error key '%s' no esta en keys" % key)

        for key in keys:
            self.data[key.replace('_', '.')] = ''

    def keys(self):
        return self.data.keys()

    def __setitem__(self, key, value):
        key = key.replace('_', '.')
        self.data[key] = value

        if value:
            pref, is_new = Preference.objects.get_or_create(account_id = self.data['account.id'], key = key, defaults={'value': value})
            self.save_on_cache(str(key), value)
            if not is_new:
                pref.value = value
                pref.save()
            return pref
        else:
            try:
                Preference.objects.get(account_id = self.data['account.id'], key = key).delete()
            except Preference.DoesNotExist:
                pass
            return None

    def load_all(self):
        keys = [pref[0] for pref in choices.ACCOUNT_PREFERENCES_AVAILABLE_KEYS]
        self.load(keys)

    def get_from_cache(self, key):
        key = key.replace('_', '.')
        if self.engine_cache:
            key = 'preference_%s_%s' % (str(self.data['account.id']), key)
            value = self.engine_cache.get(str(key))
            #if settings.DEBUG: logger.info('Get from cache %s=%s' % (key, value))
            return value

        return None

    def save_on_cache(self, key, value):
        key = key.replace('_', '.')
        if self.engine_cache:
            try:
                key = 'preference_%s_%s' % (str(self.data['account.id']), key)
                self.engine_cache.set(key, value, settings.MEMCACHED_DEFAULT_TTL)    
                #if settings.DEBUG: logger.info('Save on cache %s=%s' % (key, value))
                return True
            except Exception, e:
                logger.error('No se grabo la preferencia (%s) en cache: %s' % (str(key), str(e)))
                
        return False
