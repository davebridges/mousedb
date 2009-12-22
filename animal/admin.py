from mousedb.animal.models import Strain, Animal, Breeding, Cage
from django.contrib import admin
import datetime

class AnimalInline(admin.TabularInline):
	model = Animal
	fields = ('Strain', 'Background', 'MouseID','Cage', 'Genotype', 'Gender', 'Born', 'Weaned', 'Generation', 'Markings', 'Notes', 'Rack', 'Rack_Position')
	radio_fields = {"Gender": admin.HORIZONTAL, "Strain":admin.HORIZONTAL, "Background": admin.HORIZONTAL, "Genotype": admin.HORIZONTAL}

class AnimalAdmin(admin.ModelAdmin):
	fieldsets = (
		(None, {
			'fields': ('Strain', 'Background', 'MouseID','Cage', 'Genotype', 'Gender', 'Born', 'Weaned', 'Backcross', 'Generation', 'Markings', 'Notes', 'Breeding', 'Rack', 'Rack_Position')
		}),
	('Animal Death Information', {
		'classes' : ('collapse',),
		'fields' : ('Death', 'Cause_of_Death', 'Alive'),
		}),
	)
	raw_id_fields = ("Breeding",)
	list_display = ('MouseID', 'Rack', 'Rack_Position', 'Cage', 'Markings','Gender', 'Genotype', 'Strain', 'Background', 'Generation', 'Backcross', 'Born', 'Alive', 'Death')
	list_filter = ('Alive','Strain', 'Background','Gender','Genotype','Backcross')
	search_fields = ['MouseID', 'Cage']
	radio_fields = {"Gender": admin.HORIZONTAL, "Strain":admin.HORIZONTAL, "Background": admin.HORIZONTAL, "Genotype": admin.HORIZONTAL, "Cause_of_Death": admin.HORIZONTAL}
	actions = ['mark_sacrificed']
	def mark_sacrificed(self,request,queryset):
		rows_updated = queryset.update(Alive=False, Death=datetime.date.today(), Cause_of_Death='Sacrificed')
		if rows_updated == 1:
			message_bit = "1 animal was"
		else:
			message_bit = "%s animalss were" % rows_updated
		self.message_user(request, "%s successfully marked as sacrificed." % message_bit)
	mark_sacrificed.short_description = "Mark Animals as Sacrificed"
admin.site.register(Animal, AnimalAdmin)

class StrainAdmin(admin.ModelAdmin):
	fields = ('Strain', 'Strain_slug', 'Comments')
	prepopulated_fields = {"Strain_slug": ("Strain",)}
admin.site.register(Strain, StrainAdmin)

class BreedingAdmin(admin.ModelAdmin):
	list_display = ('Cage', 'CageID', 'Start', 'Rack', 'Rack_Position', 'Strain', 'Crosstype', 'BreedingName', 'Notes', 'Active')
	list_filter = ('Timed_Mating', 'Strain', 'Active', 'Crosstype')
	fields = ('Male', 'Females', 'Timed_Mating', 'Cage', 'CageID', 
'Rack', 
'Rack_Position', 'BreedingName', 'Strain', 'Start', 'End', 'Active', 'Crosstype', 'Notes')
	ordering = ('Active', 'Start')
	search_fields = ['Cage',]
	raw_id_fields = ("Male", "Females")
	radio_fields = {"Crosstype": admin.VERTICAL, "Strain": admin.HORIZONTAL}
admin.site.register(Breeding, BreedingAdmin)

class CageAdmin(admin.ModelAdmin):
	fields = ('Barcode', 'Rack', 'Rack_Position')
	list_display = ('Barcode', 'Rack', 'Rack_Position')
	list_filter = ('Rack',)
admin.site.register(Cage, CageAdmin)

