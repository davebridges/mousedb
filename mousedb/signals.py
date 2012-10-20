'''This package contains generic signals.

Currently there is a signal so when a User is saved, an API key is created
'''

from django.contrib.auth.models import User
from django.db import models
from tastypie.models import create_api_key

#create api key for each time a user is saved
models.signals.post_save.connect(create_api_key, sender=User)