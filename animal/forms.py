"""Forms for use in manipulating objects in the animal app."""

from django.forms import ModelForm
from django import forms

from mousedb.animal.models import Animal, Breeding

class AnimalChangeForm(ModelForm):
    """This form provides fields for altering animal fields.
	
    This form us used with the mouse/(MouseID)/change url.
	This modelform excludes the fields CageID (not yet implemented), Gender, Born, Weaned, Backcross, Generation, Mother, Father, Notes and Alive (automatically set upon death)."""
    class Meta:
        model = Animal
        fields = ['Strain','Background','MouseID', 'Markings', 'Cage', 'Rack', 'Rack_Position', 'Genotype', 'Death', 'Cause_of_Death']
		
class AnimalFormCageID(ModelForm):
    """This form provides all fields for altering animal data.
	
	This is expected to be used as part of the migration to CageID rather than Cage.  Therefore, in this form, Cage is excluded and CageID is set as an integer field.
	The CageID will be set based on that integer, and a pre-save step will generate that foreignkey field if necesssary."""
    class Meta:
        model = Animal
        exclude = ['Cage', 'Alive', 'Cause_of_Death', 'Death']
		
class AnimalForm(ModelForm):
	"""This modelform provides fields for modifying animal data.
	
	It includes all fields except CageID (not yet implemented) and Alive (which is automattically set upon saving the animal)."""
	class Meta:
		model = Animal
		exclude = ['CageID', 'Alive']

class BreedingForm(ModelForm):
    """This form provides most fields for creating and entring breeding cage data.
	
    This form is used from the url /mousedb/breeding/new and is a generic create view.  The only excluded field is CageID, as this feature is not implemented yet.
    """
    class Meta:
        model = Breeding
        exclude = ['CageID',]




