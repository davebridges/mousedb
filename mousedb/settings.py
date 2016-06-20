# Django settings for experimentdb project.

import os.path

PROJECT_DIR = os.path.dirname(__file__)

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True
USE_TZ = True

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'ci%^08ig-0qu*&b(kz_=n6lvbx*puyx6=8!yxzm0+*z)w@7+%6'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = ['django.template.loaders.filesystem.Loader',
 'django.template.loaders.app_directories.Loader']

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware'
)

ROOT_URLCONF = 'mousedb.urls'


STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, "static"),
)


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                "mousedb.context_processors.group_info",
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'mousedb.data',
    'mousedb.animal',
    'mousedb.timed_mating',
    'mousedb.groups',
    'mousedb.veterinary',
    'braces',
    'tastypie'
)

# magically include jqueryUI/js/css for ajax_select
AJAX_SELECT_BOOTSTRAP = True
AJAX_SELECT_INLINES = 'inline'

MESSAGE_STORAGE = 'django.contrib.messages.storage.fallback.FallbackStorage'

AJAX_LOOKUP_CHANNELS = {
    'animal' : ('mousedb.animal.lookups', 'AnimalLookup'),
    'animal-male' : ('mousedb.animal.lookups', 'AnimalLookupMale'),
    'animal-female' : ('mousedb.animal.lookups', 'AnimalLookupFemales')}

from localsettings import *



