from core.settings import *

MIDDLEWARE_CLASSES += (
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'admin.urls'

INSTALLED_APPS += (
    'admin',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'redisboard',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.i18n',
    'django.contrib.messages.context_processors.messages',
    'django.contrib.auth.context_processors.auth',
)

STATIC_URL = '/media/'

PAGINATION_RESULTS_PER_PAGE = 10

SESSION_ENGINE = 'django.contrib.sessions.backends.db'

try:
    from admin.local_settings import *
except ImportError:
    pass
