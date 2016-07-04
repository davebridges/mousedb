# Django settings for experimentdb project.
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

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DEBUG = True
TEMPLATE_DEBUG = DEBUG
LOGIN_URL = '/accounts/login/' #this presumes that apache is pointing at /mousedb and may need to be changed if a different root is being used

MEDIA_URL = '/mousedb-media/'
STATIC_URL = '/mousedb-static/'

import os.path
PROJECT_DIR = os.path.dirname(__file__)
#these locations can be absolue paths or relative to the installation (as is shown here)
MEDIA_ROOT = os.path.join(PROJECT_DIR, "served-media") #set to where pictures and files will be stored.  Default is media folder and this is where MEDIA_URL on your webserver should point
STATIC_ROOT = os.path.join(PROJECT_DIR, "served-static") #this folder is populated by the collectstatic command and is where STATIC_URL on your webserver should point
MEDIA_URL = '/mousedb-media/'
STATIC_URL = '/mousedb-static/'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

DATABASES = {
    'default': {
        'NAME': 'mousedb.db', # Or path to database file if using sqlite3.
        'ENGINE': 'django.db.backends.sqlite3', #  Choose one of 'django.db.backends.postgresql_psycopg2','django.db.backends.postgresql', 'django.db.backends.mysql', 'django.db.backends.sqlite3', 'django.db.backends.oracle'
        'USER': '',  # Not used with sqlite3.
        'PASSWORD': '', # Not used with sqlite3
	'HOST':'', # Set to empty string for localhost. Not used with sqlite3.
	'PORT':'', # Set to empty string for default. Not used with sqlite3.
    }
}

WEAN_AGE = 21 #this is the earliers age at which pups can be weaned from their parents.
GENOTYPE_AGE = 14 #this is the earliest age at which pups can be genotyped or ear tagged.




