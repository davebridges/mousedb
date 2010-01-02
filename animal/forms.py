"""Forms for use in manipulating objects in the animal app."""

from django.forms import ModelForm
from django import forms

from mousedb.animal.models import Animal

class AnimalChangeForm(ModelForm):
    """This form provides fields for altering animal fields.
	
    This form us used with the mouse/(MouseID)/change url.
	This modelform excludes the fields CageID (not yet implemented), Gender, Born, Weaned, Backcross, Generation, Mother, Father, Notes and Alive (automatically set upon death)."""
    class Meta:
        model = Animal
        fields = ['Strain','Background','MouseID', 'Markings', 'Cage', 'Rack', 'Rack_Position', 'Genotype', 'Death', 'Cause_of_Death']
		
class AnimalForm(ModelForm):
    CageID = forms.IntegerField()
    class Meta:
        model = Animal
        exclude = ['Cage',]






