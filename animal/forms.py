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
		
class AnimalForm(ModelForm):
    """This form provides all fields for altering animal data.
	
	This is expected to be used as part of the migration to CageID rather than Cage.  Therefore, in this form, Cage is excluded and CageID is set as an integer field.
	The CageID will be set based on that integer, and a pre-save step will generate that foreignkey field if necesssary."""
    CageID = forms.IntegerField()
    class Meta:
        model = Animal
        exclude = ['Cage',]


class BreedingForm(ModelForm):
    """This form provides for creating and modifying breeding cage information.

    This form is called by using /mousedb/breeding/new and is a generic create view.  It excludes CageID until this feature is fully implemented.  It also excludes Active as this value is automatically set upon setting and End date."""
    class Meta:
        model = Breeding
        exclude = ['CageID', 'Active']
