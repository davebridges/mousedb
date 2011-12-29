"""Settings to control the admin interface for the timed_mating app.

This file defines a PlugEventsAdmin object to enter parameters about individual plug events/"""

from django.contrib import admin
from mousedb.timed_mating.models import PlugEvents


class PlugEventsAdmin(admin.ModelAdmin):
    """This class defines the admin interface for the PlugEvents model."""
    list_display = ('PlugDate', 'PlugFemale', 'PlugMale', 'SacrificeDate', 'Researcher', 'Active')
admin.site.register(PlugEvents, PlugEventsAdmin)
