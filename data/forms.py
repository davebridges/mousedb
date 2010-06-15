from django.forms import ModelForm
from django import forms
from django.contrib.admin import widgets
from django.forms.models import inlineformset_factory

from ajax_select.fields import AutoCompleteSelectMultipleField, AutoCompleteSelectField

from mousedb.data.models import Experiment, Measurement, Study, Treatment
from mousedb.animal.models import Animal

class ExperimentForm(ModelForm):
    """This is the configuration for the experiment form.

    This form is used to set up and modify an experiment.  It uses a datepicker widget for the date, and autocomplete forms for the animals.
    """
    animals = AutoCompleteSelectMultipleField('animal')
    class Meta:
        model = Experiment
    class Media:
		css = {
			'all': ('javascript/jquery-ui/css/custom-theme/jquery-ui-1.7.2.custom.css','javascript/jquery-autocomplete/jquery.autocomplete.css', 'css/autocomplete.css')
				}
		js = ('javascript/jquery-1.3.2.js','javascript/jquery-ui/js/jquery-ui-1.7.2.custom.min.js', 'javascript/jquery-autocomplete/jquery.autocomplete.js')
 

class StudyExperimentForm(ModelForm):
	class Meta:
		model = Experiment
		exclude = ['study',]

MeasurementFormSet = inlineformset_factory(Experiment, Measurement, extra=10, can_delete=True)

class MeasurementForm(ModelForm):
	"""Form definition for adding and editing measurements.
	
	This form excludes experiment, which must be passed as a filtering parameter from the view.  
	This form is used for formsets to add or modify measurements from within an experiment."""

	class Meta:
		model = Measurement
	
class StudyForm(ModelForm):
    """This is the configuration for the study form.

    This form is used to create and modify studies.  It uses an autocomplete widget for the animals."""
    animals = AutoCompleteSelectMultipleField('animal')
    class Meta:
         model = Study
    class Media:
        css = {
	'all': ('javascript/jquery-ui/css/custom-theme/jquery-ui-1.7.2.custom.css','javascript/jquery-autocomplete/jquery.autocomplete.css', 'css/autocomplete.css')
		}
        js = ('javascript/jquery-1.3.2.js','javascript/jquery-ui/js/jquery-ui-1.7.2.custom.min.js', 'javascript/jquery-autocomplete/jquery.autocomplete.js')
                

class TreatmentForm(ModelForm):
	"""Form class for study treatment groups.

	In the case of studies, animals are defined in the treatment group rather than in the study group.  A treatment consists of a study, a set of animals and the conditions which define that treatment.  This includes related fields for environment, diet, implants and transplants."""
	class Meta:
		model = Treatment
