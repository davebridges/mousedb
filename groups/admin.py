from django.contrib import admin
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
