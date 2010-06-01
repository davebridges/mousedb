import os
import sys
sys.path.append("C:\Documents and Settings\Dave Bridges\My Documents\Source") #replace with path where mousedb directory is

os.environ['DJANGO_SETTINGS_MODULE'] = 'mousedb.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
