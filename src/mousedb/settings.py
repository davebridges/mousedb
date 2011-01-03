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

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_DIR, "media")

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/mousedb-media/admin-media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'ci%^08ig-0qu*&b(kz_=n6lvbx*puyx6=8!yxzm0+*z)w@7+%6'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware'
)

ROOT_URLCONF = 'mousedb.urls'

TEMPLATE_DIRS = (
	os.path.join(PROJECT_DIR, "templates"),
)

TEMPLATE_CONTEXT_PROCESSORS =(
	"django.core.context_processors.auth",
	"django.core.context_processors.debug",
	"django.core.context_processors.i18n",
	"django.core.context_processors.media",
	'django.contrib.messages.context_processors.messages',
	"mousedb.context_processors.group_info",
)


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.admin',
	'mousedb.data',
	'mousedb.animal',
	'mousedb.timed_mating',
	'mousedb.groups',
	'django.contrib.admin',
	'ajax_select',
	'south'
)

MESSAGE_STORAGE = 'django.contrib.messages.storage.fallback.FallbackStorage'

AJAX_LOOKUP_CHANNELS = {
    'animal' : ('mousedb.animal.lookups', 'AnimalLookup'),
    'animal-male' : ('mousedb.animal.lookups', 'AnimalLookupMale'),
	'animal-female' : ('mousedb.animal.lookups', 'AnimalLookupFemale'),
}

try:
    from localsettings import *
except ImportError:
    print 'localsetting could not be imported'
    pass #Or raise



