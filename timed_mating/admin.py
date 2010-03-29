from django.contrib import admin

from timed_mating.models import PlugEvents


class PlugEventsAdmin(admin.ModelAdmin):
	list_display = ('PlugDate', 'PlugFemale', 'PlugMale', 'SacrificeDate', 'Researcher', 'Active')
admin.site.register(PlugEvents, PlugEventsAdmin)
