ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DEBUG = False
TEMPLATE_DEBUG = DEBUG
LOGIN_URL = '/mousedb/accounts/login/' #this presumes that apache is pointing at /mousedb and may need to be changed if a different root is being used

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
# This presumes that media is being served at mousedb-media.  If it is not then change this setting.
MEDIA_URL = '/mousedb-media/'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Detriot'

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

