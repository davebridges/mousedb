from django.forms import ModelForm
from django import forms
from django.contrib.admin import widgets
from django.forms.models import inlineformset_factory

from mousedb.data.models import Experiment, Measurement, Study, Treatment
from mousedb.animal.models import Animal

class ExperimentForm(ModelForm):
	#animals = forms.ModelMultipleChoiceField(queryset=Animal.objects.all(), widget=widgets.FilteredSelectMultiple("animals",True))
	class Meta:
		model = Experiment

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
	class Meta:
		model = Study

class TreatmentForm(ModelForm):
	"""Form class for study treatment groups.

	In the case of studies, animals are defined in the treatment group rather than in the study group.  A treatment consists of a study, a set of animals and the conditions which define that treatment.  This includes related fields for environment, diet, implants and transplants."""
	class Meta:
		model = Treatment
