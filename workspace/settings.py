# -*- coding: utf-8 -*-
from core.settings import *

IS_WORKSPACE = True

LOCALE_PATHS = (
    os.path.join(PROJECT_PATH, 'workspace', 'locale'),
) + LOCALE_PATHS

MIDDLEWARE_CLASSES += (
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'workspace.middlewares.nocache.NoCacheMiddleware',
    'workspace.middlewares.auth.AccessManager',
    'workspace.middlewares.ioc.DependenciesInjector',
    'workspace.middlewares.catch.ExceptionManager',
)

ROOT_URLCONF = 'workspace.urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, 'workspace', 'templates'),
) + TEMPLATE_DIRS

SEARCH_MAX_RESULTS = 40
PAGINATION_RESULTS_PER_PAGE = 10

SECOND_LANGUAGE = 'es'

INSTALLED_APPS += (
    'django.contrib.messages',
    'workspace',
    'django.contrib.sessions',
)

BASE_URI = 'workspace'
MEDIA_URI = BASE_URI

DEFAULT_CATEGORIES = {
    'en': [u'Education', u'Entertainment', u'World', u'Business', u'Economy', u'Technology', u'Culture', u'Health', u'Sports', u'Weather', u'Earth', u'Science'],
    'es': [u'Educación', u'Entretenimiento', u'Mundo', u'Negocios', u'Economía', u'Tecnología', u'Cultura', u'Salud', u'Deportes', u'Clima', u'Planeta', u'Ciencia'],
}

SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

STATICFILES_DIRS += (os.path.join(PROJECT_PATH, 'workspace/media/'),)

if DEBUG:
    INSTALLED_APPS += (
        'selenium',
)

TEMPLATE_CONTEXT_PROCESSORS += (
    'django.contrib.messages.context_processors.messages',
)

REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] = (
    'core.rest.auth.RestAuthentication',
)

REST_FRAMEWORK['DEFAULT_PERMISSION_CLASSES'] = (
    'rest_framework.permissions.IsAuthenticated',
)

try:
    from workspace.local_settings import *
except ImportError:
    pass

try:
    MIDDLEWARE_CLASSES += WORKSPACE_PLUGIN_MIDDLEWARE_CLASSES
except:
    pass

try:    
    from plugins.local_settings import *
except ImportError:
    pass