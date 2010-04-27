"""Forms for use in manipulating objects in the animal app."""

from django.forms import ModelForm
from django import forms

from mousedb.animal.models import Animal, Breeding
	
class AnimalForm(ModelForm):
	"""This modelform provides fields for modifying animal data.
	
	It includes all fields except CageID (will be deprecated) and Alive (which is automattically set upon saving the animal).
	This form also automatically loads javascript and css for the datepicker jquery-ui widget."""
	class Meta:
		model = Animal
		exclude = ['CageID', 'Alive']
	class Media:
		css = {
			'all': ('javascript/jquery-ui/css/custom-theme/jquery-ui-1.7.2.custom.css',)
				}
		js = ('javascript/jquery-1.3.2.js','javascript/jquery-ui/js/jquery-ui-1.7.2.custom.min.js')


class BreedingForm(ModelForm):
    """This form provides most fields for creating and entring breeding cage data.
	
    This form is used from the url /mousedb/breeding/new and is a generic create view.  The only excluded field is CageID, as this feature will be deprecated.
    """
    class Meta:
        model = Breeding
        exclude = ['CageID', 'Active']




