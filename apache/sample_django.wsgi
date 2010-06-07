#Fill in the sys.path.append entry (INSTALL PATH) with the location of your mousedb.  This is the folder which contains mousedb (should not end in mousedb, and should not have a trailing slash.  Save this file as django.wsgi

import os
import sys
sys.path.append('INSTALL PATH') #replace with path where mousedb directory is

os.environ['DJANGO_SETTINGS_MODULE'] = 'mousedb.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
