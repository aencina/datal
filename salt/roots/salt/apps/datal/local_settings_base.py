{% set user = pillar['system']['user'] %}

SECRET_KEY = '{{ pillar["application"]["settings"]["secret_key"] }}'
ROOT_URLCONF = '{{ pillar["application"]["settings"]["root_urlconf"] }}'

PAGINATION_RESULTS_PER_PAGE = {{ pillar["application"]["settings"]["pagination_results_per_page"] }}

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

DOMAINS = {'api': '{{  pillar["application"]["settings"]["domains"]["api"] }}',
           'microsites': '{{  pillar["application"]["settings"]["domains"]["microsites"] }}',
           'workspace': '{{  pillar["application"]["settings"]["domains"]["workspace"] }}',
           'cdn': '{{  pillar["application"]["cdn"] }}',
}

DOMAINS_ENGINE = {'api': '{{  pillar["application"]["settings"]["domains_engine"]["api"] }}',
           'microsites': '{{  pillar["application"]["settings"]["domains_engine"]["microsites"] }}',
           'workspace': '{{  pillar["application"]["settings"]["domains_engine"]["workspace"] }}',
}

WORKSPACE_URI = '{{pillar["application"]["settings"]["workspace_protocol"]}}://{{  pillar["application"]["settings"]["domains"]["workspace"] }}'

EMAIL_HOST = '{{  pillar["email"]["host"] }}'
EMAIL_HOST_USER = '{{  pillar["email"]["user"] }}'
EMAIL_HOST_PASSWORD = '{{  pillar["email"]["password"] }}'
EMAIL_PORT = '{{ pillar["email"]["port"] }}'
EMAIL_USE_TLS = {{ pillar["email"]["tls"] }}

BIGDATA_HOSTS = ()
BIGDATA_PORT = ''
BIGDATA_API_ENDPOINT = ''

AWS_ACCESS_KEY = '{{ pillar["amazon"]["S3"]["accesskey"] }}'
AWS_SECRET_KEY = '{{ pillar["amazon"]["S3"]["secretkey"] }}'
AWS_BUCKET_NAME = '{{ pillar["amazon"]["S3"]["bucket"] }}'
AWS_CDN_BUCKET_NAME = '{{ pillar["amazon"]["S3"]["cdn_bucket"] }}'

REQUESTS_QUEUE = '{{ pillar["queues"]["request_queue"] }}'

API_KEY = '{{ pillar["application"]["api_key"] }}'
PUBLIC_KEY = '{{ pillar["application"]["public_key"] }}'

SENTRY_DSN = '{{ pillar["sentry_dns"] }}'

STATIC_ROOT= "{{ pillar['application']['statics_dir'] }}"

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
SFTP_BASE_URL = "{{ pillar['datastore']['sftp']['base_url'] }}" # url for donwloading resources
SFTP_DATASTORE_HOSTNAME = "{{ pillar['datastore']['sftp']['host'] }}"
SFTP_DATASTORE_PORT = {{ pillar['datastore']['sftp']['port'] }}
SFTP_DATASTORE_USER = "{{ pillar['datastore']['sftp']['user'] }}"
SFTP_DATASTORE_PASSWORD = "{{ pillar['datastore']['sftp']['password'] }}"
