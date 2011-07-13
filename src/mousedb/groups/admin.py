from django.contrib import admin
from django.contrib.admin.models import LogEntry

from mousedb.groups.models import License, Group


class GroupAdmin(admin.ModelAdmin):
    """Defines the admin interface for Groups.

    Currently set as default."""    
    pass
admin.site.register(Group, GroupAdmin)

class LicenseAdmin(admin.ModelAdmin):
    """Defines the admin interface for Licences.

    Currently set as default."""
    pass
admin.site.register(License, LicenseAdmin)

class LogEntryAdmin(admin.ModelAdmin):
    """Defines the admin interface for the LogEntry objects."""
    
    list_display = ('user', 'content_type', 'object_id')
admin.site.register(LogEntry, LogEntryAdmin)
