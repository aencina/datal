{% set environment = salt['pillar.get']('environment', None) %}
{% set user = pillar['system']['user'] %}
import os
PROJECT_PATH, FILENAME = os.path.split(os.path.abspath(os.path.dirname(__file__)))

SECRET_KEY = '{{ pillar["application"]["settings"]["secret_key"] }}'
ROOT_URLCONF = '{{ pillar["application"]["settings"]["root_urlconf"] }}'

DEBUG = {{ pillar["application"]["settings"]["debug"]}}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '{{ pillar["database"]["name"] }}',
        'USER': '{{ pillar["database"]["user"] }}',
        'PASSWORD': '{{ pillar["database"]["password"] }}',
        'HOST': '{{ pillar["database"]["host"] }}',
        'PORT': '{{ pillar["database"]["port"] }}',
        'SUPPORTS_TRANSACTIONS': True
    },
}

SEARCHIFY = {
    'api_url': '{{  pillar["searchers"]["searchify"]["api_url"] }}',
    'index': '{{  pillar["searchers"]["searchify"]["index"] }}'
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '{{ pillar["memcached"]["microsites"] }}',
        'TIMEOUT': 600,
        # 'KEY_FUNCTION': 'core.decorators.datal_make_key',
        'KEY_PREFIX': 'default',
        'OPTIONS': {
            'MAX_ENTRIES': 300, # Default
        }
    },
    'engine': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '{{ pillar["memcached"]["engine"] }}',
        'TIMEOUT': 60,
        # 'KEY_FUNCTION': 'core.decorators.datal_make_key',
        'KEY_PREFIX': 'default',
        'OPTIONS': {
            'MAX_ENTRIES': 300, # Default
        }
    }
}

DOMAINS = {'api': '{{  pillar["application"]["settings"]["domains"]["api"] }}',
           'microsites': '{{  pillar["application"]["settings"]["domains"]["microsites"] }}',
           'workspace': '{{  pillar["application"]["settings"]["domains"]["workspace"] }}',
           'cdn': '{{  pillar["application"]["cdn"] }}',
}

DOMAINS_ENGINE = {'api': '{{  pillar["application"]["settings"]["domains_engine"]["api"] }}',
           'microsites': '{{  pillar["application"]["settings"]["domains_engine"]["microsites"] }}',
           'workspace': '{{  pillar["application"]["settings"]["domains_engine"]["workspace"] }}',
}

WORKSPACE_URI = '{{ pillar["application"]["settings"]["workspace_protocol"] }}://{{  pillar["application"]["settings"]["domains"]["workspace"] }}'

EMAIL_HOST = '{{  pillar["email"]["host"] }}'
EMAIL_HOST_USER = '{{  pillar["email"]["user"] }}'
EMAIL_HOST_PASSWORD = '{{  pillar["email"]["password"] }}'
EMAIL_PORT = '{{ pillar["email"]["port"] }}'
EMAIL_USE_TLS = {{ pillar["email"]["tls"] }}

{% if environment == 'prod' %}
POST_OFFICE = {
    'EMAIL_BACKEND': 'django.core.mail.backends.smtp.EmailBackend'
}
{% endif %}

BIGDATA_HOST = 'http://bigdata.junar.com'
BIGDATA_PORT = '8080'
BIGDATA_API_ENDPOINT = '/bigdata'

AWS_ACCESS_KEY = '{{ pillar["amazon"]["accesskey"] }}'
AWS_SECRET_KEY = '{{ pillar["amazon"]["secretkey"] }}'
AWS_BUCKET_NAME = '{{ pillar["datastore"]["bucket"] }}'
AWS_CDN_BUCKET_NAME = '{{ pillar["datastore"]["cdn_bucket"] }}'

REQUESTS_QUEUE = '{{ pillar["queues"]["request_queue"] }}'

API_KEY = '{{ pillar["application"]["api_key"] }}'
PUBLIC_KEY = '{{ pillar["application"]["public_key"] }}'

STATIC_ROOT= "{{ pillar['application']['install_dir'] }}{{ pillar['application']['statics_dir'] }}"

TWITTER_PROFILE_URL = "{{ pillar['social']['twitter_profile_url'] }}"
FACEBOOK_PROFILE_URL= "{{ pillar['social']['facebook_profile_url'] }}"
MAIL_LIST = {'LIST_COMPANY' : "{{ pillar['mail_list']['list_company'] }}",
             'LIST_DESCRIPTION': "{{ pillar['mail_list']['list_description'] }}",
             'LIST_UNSUBSCRIBE': "{{ pillar['mail_list']['list_unsubscribe'] }}",
             'LIST_UPDATE_PROFILE': "{{ pillar['mail_list']['list_update_profile'] }}",
             'WELCOME_TEMPLATE_ES': "{{ pillar['mail_list']['welcome_template_es'] }}",
             'WELCOME_TEMPLATE_EN': "{{ pillar['mail_list']['welcome_template_en'] }}"}

MAILCHIMP = {
            'uri': "{{ pillar['mail_list']['mailchimp']['uri'] }}",
            'api_key': "{{ pillar['mail_list']['mailchimp']['api_key'] }}",
            'lists': {'workspace_users_list':
                            {
                             'es': {'id': "{{ pillar['mail_list']['mailchimp']['lists']['workspace_users_list']['es_id'] }}"},
                             'en': {'id': "{{ pillar['mail_list']['mailchimp']['lists']['workspace_users_list']['en_id'] }}"}
                             }
                     }
            }

MANDRILL = {'api_key': "{{ pillar['mail_list']['mandrill']['api_key'] }}"}

USE_DATASTORE = "{{ pillar['datastore']['use'] }}"
SFTP_DATASTORE_REMOTEBASEFOLDER = "{{ salt['user.info'](user).home }}/{{ pillar['datastore']['sftp']['remote_base_folder'] }}" # remote path for saving all resources
SFTP_DATASTORE_LOCALTMPFOLDER = "{{ salt['user.info'](user).home }}/{{ pillar['datastore']['sftp']['local_tmp_folder'] }}" # local base folder for saving temporary files before upload
SFTP_BASE_URL = "{{ pillar['datastore']['sftp']['public_base_url'] }}" # url for donwloading resources
SFTP_DATASTORE_HOSTNAME = "{{ pillar['datastore']['sftp']['host'] }}"
SFTP_DATASTORE_PORT = {{ pillar['datastore']['sftp']['port'] }}
SFTP_DATASTORE_USER = "{{ pillar['datastore']['sftp']['user'] }}"
SFTP_DATASTORE_PASSWORD = "{{ pillar['datastore']['sftp']['password'] }}"

# REDIS
REDIS_READER_HOST = '{{ pillar["redis"]["read_host"] }}'
REDIS_WRITER_HOST = '{{ pillar["redis"]["write_host"] }}'
REDIS_PORT = {{ pillar["redis"]["read_port"] }}
REDIS_DB   = 0
REDIS_STATS_TTL = 1

# MEMCACHED
MEMCACHED_DEFAULT_TTL = 60 # seconds
MEMCACHED_LONG_TTL = 86400 # one day
MEMCACHED_ENGINE_END_POINT = ['{{ pillar["memcached"]["engine"] }}']
MEMCACHED_API_END_POINT = ['{{ pillar["memcached"]["api"] }}']

# Listado de los plugins disponibles
INSTALLED_PLUGINS = (
    'plugins.advanced_filtering',
    'plugins.dashboards',
    'plugins.reports',
    'plugins.apiv1',
    'plugins.theme_junar',
    'plugins.kpi',
    'plugins.faceapp',
)

PLUGIN_LOCALES = (
    os.path.join(PROJECT_PATH, 'plugins', 'advanced_filtering', 'locale'),
    os.path.join(PROJECT_PATH, 'plugins', 'dashboards', 'locale'),
    os.path.join(PROJECT_PATH, 'plugins', 'reports', 'locale'),
    os.path.join(PROJECT_PATH, 'plugins', 'apiv1', 'locale'),
    os.path.join(PROJECT_PATH, 'plugins', 'theme_junar', 'locale'),
    os.path.join(PROJECT_PATH, 'plugins', 'kpi', 'locale'),
    os.path.join(PROJECT_PATH, 'plugins', 'faceapp', 'locale'),
)

PLUGIN_STATIC_DIRS = (
    os.path.join(PROJECT_PATH, 'plugins', 'advanced_filtering', 'static'),
    os.path.join(PROJECT_PATH, 'plugins', 'dashboards', 'static'),
    os.path.join(PROJECT_PATH, 'plugins', 'reports', 'static'),
    os.path.join(PROJECT_PATH, 'plugins', 'apiv1', 'static'),
    os.path.join(PROJECT_PATH, 'plugins', 'theme_junar', 'static'),
    os.path.join(PROJECT_PATH, 'plugins', 'kpi', 'static'),
    os.path.join(PROJECT_PATH, 'plugins', 'faceapp', 'static'),
)

APPLICATION_DETAILS = {
    'name': 'Junar',
    'website': 'http://www.junar.com',
    'mail':'contact@junar.com'
}

SEARCH_INDEX = { 'url': ['{{  pillar["searchers"]["elastic"]["url"] }}',], 'index': '{{  pillar["searchers"]["elastic"]["index"] }}' }

COMPRESS_CSS_HASHING_METHOD = None

{% if environment == 'prod' %}
#AWS_ACCESS_KEY_ID = 'AKIAI652OHJ6H2VI25OA'
#AWS_SECRET_ACCESS_KEY = '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'
#AWS_STORAGE_BUCKET_NAME = 'statics.junar'

#COMPRESS_URL = "https://s3.amazonaws.com/statics.junar/"
#COMPRESS_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

#STATIC_URL = COMPRESS_URL
#COMPRESS_ROOT = STATIC_ROOT
#STATICFILES_STORAGE = COMPRESS_STORAGE
#AWS_S3_HOST = "s3.amazonaws.com"
{% endif %}