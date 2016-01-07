# coding=utf-8
import os
PROJECT_PATH, FILENAME = os.path.split(os.path.abspath(os.path.dirname(__file__)))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Webmaster', 'webmaster@junar.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'datal',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '3306',
        'SUPPORTS_TRANSACTIONS': True
    },
}

USE_DATASTORE = 'sftp' # uses s3 | sftp
USE_SEARCHINDEX = 'elasticsearch'

PAGINATION_RESULTS_PER_PAGE = 10

TIME_ZONE = 'America/Santiago'

LANGUAGES = (
    ('en', 'English'),
    ('es', 'Spanish'),
    ('pt', 'Portuguese'),
)

USE_I18N = True
USE_L10N = True

SECRET_KEY = '1'

INSTALLED_APPS = (
    'sass_processor',
    'south',
    'django_nose',
    'django.contrib.staticfiles',
    'django_extensions',
    'core',
    'raven.contrib.django',
    "compressor",
    "post_office",
    'djangobower',
    "rest_framework",
    'djangoplugins',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "core.context_processors.request_context",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.i18n"
)

MIDDLEWARE_CLASSES = ()

LOCALE_PATHS = (
    os.path.join(PROJECT_PATH, 'core', 'locale'),
)

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, 'core', 'templates'),
)

CACHE_DATABASES = {
    'dataviews': 0,
    'alerts': 1,
    'pipes': 1,
    'history': 1,
    'api_stats': 2,
    'resources_stats': 3,
    'sessions': 4,
    # 6 & 7 used by the engine
    # 10 used by Marco (backups)
    'activity_resources': 5,
}

REDIS_READER_HOST = 'localhost'
REDIS_WRITER_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB   = 0
REDIS_STATS_TTL = 1
MEMCACHED_ENGINE_END_POINT = ['127.0.0.1:11211']
MEMCACHED_API_END_POINT = ['127.0.0.1:11211']
MEMCACHED_DEFAULT_TTL = 60 # seconds
MEMCACHED_LONG_TTL = 86400 # one day

VERSION_JS_CSS = 666

SESSION_COOKIE_NAME = 'localhostsessionid'
#SESSION_ENGINE = 'redis_sessions.session'
SESSION_REDIS_HOST = REDIS_WRITER_HOST
SESSION_REDIS_PORT = REDIS_PORT
SESSION_REDIS_DB = 4

AWS_ACCESS_KEY = 'your-aws-acc-key'
AWS_SECRET_KEY = 'your-aws-secret-key'
AWS_BUCKET_NAME = 'your-buecket-1'
AWS_CDN_BUCKET_NAME = 'your-public-bucket'
REQUESTS_QUEUE = 'test_requests_queue'

LOGIN_URL = '/signin'

END_POINT_SERVLET = '/AgileOfficeServer/DataStreamRequesterServlet'
END_POINT_CHART_SERVLET = '/AgileOfficeServer/ChartInvokeServlet'
END_POINT_LOADER_SERVLET= '/AgileOfficeServer/DataSourceLoaderServlet'
END_POINT_PREVIEWER_SERVLET = '/AgileOfficeServer/DataStreamPreviewerServlet'
END_POINT_CHART_PREVIEWER_SERVLET = '/AgileOfficeServer/ChartPreviewerServlet'


BASE_URI = 'localhost'
MEDIA_URI = BASE_URI
API_URI = 'http://api'
WORKSPACE_URI = 'http://workspace'
API_KEY = ''
PUBLIC_KEY = '' # To be filled with DATAL's PUBLIC KEY


OPENDATA_ACCOUNT = 'opendata'
PRIVATE_ACCOUNT = 'private'

ACCOUNT_DOMAIN_PREFERENCE_NAME = 'account.domain'

DOMAINS = {
    'api': 'api',
    'microsites': 'microsites',
    'workspace': 'workspace',
    'engine': '',
    'website': 'website',
    'cdn': '',
}

CONTENT_TYPES = {
    'json': 'application/json;charset=utf-8',
    'prettyjson': 'application/json;charset=utf-8',
    'json_array': 'application/json;charset=utf-8',
    'csv': 'text/csv;charset=utf-8',
    'html': 'text/html;charset=utf-8',
    'xml': 'text/xml;charset=utf-8',
    'xls': 'application/json;charset=utf-8',
    'kml': 'application/vnd.google-earth.kml+xml',
    'kmz': 'application/vnd.google-earth.kmz',
    'pdf': 'application/pdf',
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg',
    'png': 'image/png',
    'gif': 'image/gif',
    'zip': 'application/zip',
    'tar': 'application/x-tar',
    'gz': 'application/x-gzip'
}

IMPL_TYPES = {
    '4': 'xls',
    '5': 'pdf',
    '10': 'csv',
    '11': 'kml',
    '12': 'kmz',
    '18': 'jpg', #maybe we need a special value for each file type who has different mime type
    '19': 'zip'
}

GRAVATAR = {
    'url': 'https://www.gravatar.com/avatar/%s?s=%d&d=%s',
    'default_image': 'http://workspace.junar.com/media_core/images/common/im_avatarNotDefined.gif',
    'sizes': {
        'small': 22,
        'medium': 44,
        'large': 88,
    }
}

TYPE_DATASET = 'dt'
TYPE_DATASTREAM = 'ds'
TYPE_VISUALIZATION = 'vz'

# Term exclusion lists for searches and usernames
ENGLISH_EXCLUSION_LIST = ['abaft', 'aboard', 'about', 'above', 'absent', 'across', 'afore', 'after', 'against', 'along',
                          'alongside', 'amid', 'amidst', 'among', 'amongst', 'an', 'apropos', 'around', 'as', 'aside',
                          'astride', 'at', 'athwart', 'atop', 'barring', 'before', 'behind', 'below', 'beneath',
                          'beside', 'besides', 'between', 'betwixt', 'beyond', 'but', 'by', 'circa', 'concerning',
                          'despite', 'down', 'during', 'except', 'excluding', 'failing', 'following', 'for', 'from',
                          'given', 'in', 'including', 'inside', 'into', 'like', 'mid', 'midst', 'minus', 'near', 'next',
                          'notwithstanding', 'of', 'off', 'on', 'onto', 'opposite', 'out', 'outside', 'over', 'pace',
                          'past', 'per', 'plus', 'pro', 'qua', 'regarding', 'round', 'sans', 'save', 'since', 'than',
                          'through', 'thru', 'throughout', 'thruout', 'the', 'till', 'times', 'to', 'toward', 'towards',
                          'under', 'underneath', 'unlike', 'until', 'up', 'upon', 'versus', 'vs', 'via', 'vice', 'with',
                          'within', 'without', 'worth', 'it', 'the', 'a', 'an'
]
SPANISH_EXCLUSION_LIST = ['a', 'con', 'contra', 'de', 'desde', 'durante', 'en', 'entre', 'hacia', 'hasta', 'mediante',
                          'para', 'por', 'segun', 'sin', 'so', 'sobre', 'tras', 'via', 'excepto', 'el', 'la', 'los',
                          'las', 'un', 'una', 'unos', 'unas'
]
SEARCH_TERMS_EXCLUSION_LIST = ENGLISH_EXCLUSION_LIST + SPANISH_EXCLUSION_LIST
BLOCKED_USERNAMES = ['accounts', 'account', 'blog', 'contact', 'css', 'faq', 'form', 'email', 'error', 'help', 'home',
                     'images', 'image', 'js', 'privacy', 'news', 'rss', 'search', 'services', 'service', 'support',
                     'video', 'junardata', 'junar_data', 'junar-data', 'junar.data', 'NN', 'anonymous', 'datastreams',
                     'datastream', 'data-streams', 'data-stream', 'data_streams', 'data_stream', 'data.streams',
                     'data.stream', 'data'
]

# unificamos toda la config de los indexadores en una sola
# para indextank usamos una sola url
# pero para ES se puede utilizar una lista de hosts
SEARCH_INDEX = {
                'url': ['http://localhost:9200',],
                'index': 'datal'
                }

# Settings Keys
HOT_DATASTREAMS = 'HOT_DATASTREAMS'
HOT_VISUALIZATIONS = 'HOT_VISUALIZATIONS'
DOC_API_URL = 'https://github.com/datal-org/datal/tree/develop/docs/api'

# develop & staging sentry
SENTRY_DSN = 'http://sentrydsn@sentry.com/1'

TWITTER_PROFILE_URL = 'https://twitter.com/tuCuenta'
FACEBOOK_PROFILE_URL = 'https://facebook.com/tuFanPage'
MAIL_LIST = {'LIST_COMPANY' : '', 'LIST_DESCRIPTION': '', 
             'LIST_UNSUBSCRIBE': '', 'LIST_UPDATE_PROFILE': '',
             'WELCOME_TEMPLATE_ES': 'template_name',
             'WELCOME_TEMPLATE_EN': 'template_name'}

#EMAIL_SERVICE = 'core.lib.mail.mailchimp_backend.MailchimpMailService'
EMAIL_SERVICE = 'core.lib.mail.django_backend.DjangoMailService'

# solo si usas mailchimp/mandrill para enviar emails
MAILCHIMP = {
            'uri': 'https://us2.api.mailchimp.com/2.0/',
            'api_key': '',
            'lists': {'workspace_users_list': # listas a la cual suscribir a los usuarios del sistema
                            {
                             'es': {'id': ''},
                             'en': {'id': ''}
                             }
                     }
            }

MANDRILL = {'api_key': ''}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
        },
        'simple': {
            'format': '[%(levelname)s] %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file':{
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/tmp/datal.log',
            'formatter': 'verbose'
        },
        'mail_admins': {
            'filters': ['require_debug_false'],
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        },
         'sentry': {
            'filters': ['require_debug_false'],
            'level': 'DEBUG',
            'class': 'raven.contrib.django.handlers.SentryHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers':['file'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['file'],
            'propagate': False,
            'level': 'INFO',
        },
        'workspace': {'handlers': ['file'], 'level': 'INFO'},
        'api': {'handlers': ['file'], 'level': 'INFO'},
        'microsites': {'handlers': ['file'], 'level': 'INFO'},
        'admin': {'handlers': ['file'], 'level': 'INFO'},
        'core': {'handlers': ['file'], 'level': 'INFO'},
        'plugins': {'handlers': ['file'], 'level': 'INFO'},
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['file'],
            'propagate': False,
        },

        'elasticsearch.trace': {
            'level': 'INFO',
            'handlers': ['file'],
            'propagate': False,
        },
    }
}

IS_WORKSPACE = False

STATIC_ROOT = os.path.join(PROJECT_PATH, 'static/')
STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(PROJECT_PATH, 'core/media/'),)

# Django Compress y SASS
COMPRESS_PRECOMPILERS = (
    #('text/x-scss', 'core.lib.SCSSPreCompiler.PatchedSCSSCompiler'),
    #('text/scss', 'sass --scss {infile} {outfile}'),
)

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
    'djangobower.finders.BowerFinder',
    'sass_processor.finders.CssFinder',
)

SASS_PROCESSOR_INCLUDE_DIRS = (
    os.path.join(PROJECT_PATH, 'core/media/styles'),
    os.path.join(PROJECT_PATH, 'microsites/media/styles'),
    os.path.join(PROJECT_PATH, 'workspace/media/styles'),
)

EMAIL_BACKEND = 'post_office.EmailBackend'
EMAIL_FILE_PATH = '/tmp/datal-emails'
POST_OFFICE = {
    'EMAIL_BACKEND': 'django.core.mail.backends.filebased.EmailBackend'
}
SOUTH_MIGRATION_MODULES = {
    "post_office": "post_office.south_migrations",
}

DEFAULT_FROM_EMAIL = 'noreply@datal.org'

SUBSCRIBE_NEW_USERS_TO_MAIL_LIST = False

BOWER_COMPONENTS_ROOT = os.path.join(PROJECT_PATH, 'components')

BOWER_INSTALLED_APPS = (
    'jquery#>=2.1.4',
    'underscore#>= 1.8.3',
    'handsontable#>=0.16.1'
)

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'EXCEPTION_HANDLER': 'core.rest.exceptions.datal_exception_handler',
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'TIMEOUT': 600,
        'OPTIONS': {
            'MAX_ENTRIES': 300, # Default
        }
    },
    'engine': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'TIMEOUT': 60,
        'KEY_FUNCTION': 'core.decorators.datal_make_key',
        'OPTIONS': {
            'MAX_ENTRIES': 300, # Default
        }
    }
}

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

APPLICATION_DETAILS = {
    'name': 'Datal',
    'website': 'http://www.datal.org',
    'mail':'alguien@datal.org'
}

try:
    from core.local_settings import *
except ImportError:
    pass

try:
    INSTALLED_APPS += INSTALLED_PLUGINS
except:
    pass

try:
    LOCALE_PATHS += PLUGIN_LOCALES
except:
    pass

try:
    STATICFILES_DIRS += PLUGIN_STATIC_DIRS
except:
    pass

try:    
    from plugins.settings import *
except ImportError:
    pass

try:    
    from plugins.local_settings import *
except ImportError:
    pass