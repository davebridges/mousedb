import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'mousedb.settings'

sys.path.append('C:/Documents and Settings/davebrid/My Documents/SRC/mousedb/')
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mousedb.settings")