from django.contrib import admin

from mousedb.data.models import Experiment, Assay, Measurement, Researcher, Study, Treatment, Vendor, Diet, Environment, Implantation, Transplantation, Pharmaceutical


class MeasurementInline(admin.TabularInline):
	model = Measurement
	extra = 14
	radio_fields = {"assay": admin.VERTICAL}
	raw_id_fields = ('animal', )
	
class TreatmentInline(admin.TabularInline):
	model = Treatment
	extra = 1
	fields = ('treatment', 'animals', 'diet', 'environment', 'implantation', 'transplantation', 'pharmaceutical', 'researchers')
	raw_id_fields = ('animals', )
	
class MeasurementAdmin(admin.ModelAdmin):
	fieldsets = [
		('Measurement Information',	{'fields': ['experiment', 'assay']}),
		('Data Entry',	{'fields': ['animal', 'values']})
		]
	list_display = ('experiment', 'animal', 'assay', 'values')
	list_filter = ('assay', 'animal','experiment')
admin.site.register(Measurement, MeasurementAdmin)

class AssayAdmin(admin.ModelAdmin):
	fields = ('assay', 'measurement_units','notes', 'assay_slug')
	prepopulated_fields = {"assay_slug" : ("assay",)}
	list_display = ('assay','measurement_units','notes')
admin.site.register(Assay,AssayAdmin)

class ExperimentAdmin(admin.ModelAdmin):
	fields = ('study', 'date', 'feeding_state', 'researchers','fasting_time', 'injection', 'concentration', 'experimentID','notes')
	radio_fields = {"feeding_state": admin.VERTICAL, "injection":admin.HORIZONTAL}
	list_display = ('date','study', 'feeding_state', 'experimentID', 'injection')
	list_filter = ('feeding_state', 'injection')
	inlines = [MeasurementInline,]
admin.site.register(Experiment, ExperimentAdmin)
	

class ResearcherAdmin(admin.ModelAdmin):
	list_display = ('last_name', 'first_name', 'email', 'active')
	fields = ('last_name', 'first_name', 'email', 'active', 'name_slug')
	list_filter = ('active',)
	prepopulated_fields = {"name_slug": ("first_name","last_name")}
admin.site.register(Researcher, ResearcherAdmin)

class StudyAdmin(admin.ModelAdmin):
	list_display =( 'description','start_date', 'stop_date')
	fields = ('description', 'strain', 'start_date', 'stop_date', 'notes')
	list_filter = ('strain',)
	inlines = [TreatmentInline,]
admin.site.register(Study, StudyAdmin)

class TreatmentAdmin(admin.ModelAdmin):
	pass
admin.site.register(Treatment, TreatmentAdmin)

class VendorAdmin(admin.ModelAdmin):
	pass
admin.site.register(Vendor, VendorAdmin)

class DietAdmin(admin.ModelAdmin):
	pass
admin.site.register(Diet, DietAdmin)

class EnvironmentAdmin(admin.ModelAdmin):
	pass
admin.site.register(Environment, EnvironmentAdmin)

class ImplantationAdmin(admin.ModelAdmin):
	pass
admin.site.register(Implantation, ImplantationAdmin)

class TransplantationAdmin(admin.ModelAdmin):
	pass
admin.site.register(Transplantation, TransplantationAdmin)

class PharmaceuticalAdmin(admin.ModelAdmin):
	pass
admin.site.register(Pharmaceutical, PharmaceuticalAdmin)
