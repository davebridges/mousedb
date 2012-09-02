"""Forms for use in manipulating objects in the animal app."""

from django.forms import ModelForm
from django import forms

from ajax_select.fields import AutoCompleteSelectMultipleField, AutoCompleteSelectField

from mousedb.animal.models import Animal, Breeding
	
class AnimalForm(ModelForm):
	"""This modelform provides fields for modifying animal data.
	
	This form also automatically loads javascript and css for the datepicker jquery-ui widget.  It also includes auto"""
	Father = AutoCompleteSelectField('animal', required=False)
	Mother = AutoCompleteSelectField('animal', required=False)
	class Meta:
		model = Animal
	class Media:
		css = {
			'all': ('javascript/jquery-autocomplete/jquery.autocomplete.css', 'css/autocomplete.css')
				}
		js = ('javascript/jquery-ui/js/jquery-ui-1.8.2.custom.min.js', 'javascript/jquery-autocomplete/jquery.autocomplete.js')
		
class MultipleAnimalForm(ModelForm):
	"""This modelform provides fields for entering multiple identical copies of a set of mice.
	
	This form only includes the required fields Background and Strain."""
	count = forms.IntegerField(required=True, help_text="Enter the number of mice to be added")
	class Meta:
		model = Animal
		fields = ['Background', 'Strain', 'Breeding', 'Cage','Rack','Rack_Position','Strain', 'Background', 'Genotype', 'Gender', 'Born', 'Weaned', 'Backcross','Generation', 'Breeding', 'Father', 'Mother', 'Markings', 'Notes']

class MultipleBreedingAnimalForm(ModelForm):
	"""This modelform provides fields for entering multiple pups within a breeding set.
	
	The only fields presented are Born, Weaned, Gender and Count.  Several other fields will be automatically entered based on the Breeding Set entries."""
	count = forms.IntegerField(required=True, help_text="Enter the number of mice to be added")
	class Meta:
		model = Animal
		fields = ['Born', 'Weaned', 'Gender']
	
class BreedingForm(ModelForm):
    """This form provides most fields for creating and entring breeding cage data.
	
    This form is used from the url /mousedb/breeding/new and is a generic create view.  This view includes a datepicker widget for Stat and End dates and autocomplete fields for the Females and Male fields
    """
    Male = AutoCompleteSelectMultipleField('animal-male', required=False)
    Females = AutoCompleteSelectMultipleField('animal-female', required=False)
    class Meta:
        model = Breeding
    class Media:
		css = {
			'all': ('javascript/jquery-autocomplete/jquery.autocomplete.css', 'css/autocomplete.css')
				}
		js = ('javascript/jquery-ui/js/jquery-ui-1.8.2.custom.min.js', 'javascript/jquery-autocomplete/jquery.autocomplete.js')




