from core.settings import *

LOCALE_PATHS = (
    os.path.join(PROJECT_PATH, 'microsites', 'locale'),
) + LOCALE_PATHS


TEMPLATE_CONTEXT_PROCESSORS += (
    "microsites.context_processors.request_context",
)

MIDDLEWARE_CLASSES += (
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'microsites.middlewares.auth.AccessManager',
    'microsites.middlewares.ioc.DependencyInjector',
    'microsites.middlewares.catch.ExceptionManager',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware'
)

ROOT_URLCONF = 'microsites.urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, 'microsites', 'templates'),
) + TEMPLATE_DIRS

SEARCH_MAX_RESULTS = 100
PAGINATION_RESULTS_PER_PAGE = 10
PAGINATION_COMMENTS_PER_PAGE  = 10

INSTALLED_APPS += (
    'microsites',
    'django.contrib.sessions',
    'django.contrib.humanize',
)

BASE_URI = 'microsites'
MEDIA_URI = BASE_URI
WORKSPACE_URI = 'workspace'

BOTS = ['Googlebot', 'AdsBot-Google'] #, 'Googlebot-Mobile', 'Googlebot-Image', 'Mediapartners-Google', 'Slurp', 'YahooSeeker/M1A1-R2D2', 'MSNBot', 'MSNBot-Media', 'MSNBot-NewsBlogs', 'MSNBot-Products', 'MSNBot-Academic', 'Teoma']

STATICFILES_DIRS += ( os.path.join(PROJECT_PATH,'microsites/media/'),)
STATICFILES_DIRS += ( os.path.join(PROJECT_PATH,'microsites/static/'),)

REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] = (
    'core.rest.auth.RestAuthentication',
)

REST_FRAMEWORK['DEFAULT_PERMISSION_CLASSES'] = (
    'rest_framework.permissions.IsAuthenticated',
)

try:
    from microsites.local_settings import *
except ImportError:
    pass

try:    
    from plugins.local_settings import *
except ImportError:
    pass