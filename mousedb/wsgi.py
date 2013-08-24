import os
import sys

sys.path.append('/var/www/internal/mousedb')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mousedb.settings")
