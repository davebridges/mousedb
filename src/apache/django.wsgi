import os
import sys
sys.path.append('/usr/src/django') #replace with path where mousedb directory is

os.environ['DJANGO_SETTINGS_MODULE'] = 'mousedb.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
