ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DEBUG = False
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
TIME_ZONE = 'America/Detroit'

DATABASES = {
    'default': {
        'NAME': '', # Or path to database file if using sqlite3.
        'ENGINE': '', #  Choose one of 'django.db.backends.postgresql_psycopg2','django.db.backends.postgresql', 'django.db.backends.mysql', 'django.db.backends.sqlite3', 'django.db.backends.oracle'
        'USER': '',  # Not used with sqlite3.
        'PASSWORD': '', # Not used with sqlite3
	'HOST':'', # Set to empty string for localhost. Not used with sqlite3.
	'PORT':'', # Set to empty string for default. Not used with sqlite3.
    }
}

WEAN_AGE = 21 #this is the earliers age at which pups can be weaned from their parents.
GENOTYPE_AGE = 14 #this is the earliest age at which pups can be genotyped or ear tagged.
