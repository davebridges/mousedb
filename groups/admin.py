from django.contrib import admin
from groups.models import License, Group

class GroupAdmin(admin.ModelAdmin):
	pass
admin.site.register(Group, GroupAdmin)

class LicenseAdmin(admin.ModelAdmin):
	pass
admin.site.register(License, LicenseAdmin)