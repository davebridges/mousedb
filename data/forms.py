from django.forms import ModelForm
from django import forms
from django.contrib.admin import widgets

from data.models import Experiment, Measurement, Study, Treatment
from animal.models import Animal

class ExperimentForm(ModelForm):
	animals = forms.ModelMultipleChoiceField(queryset=Animal.objects.all(), widget=widgets.FilteredSelectMultiple("animals",True))
	class Meta:
		model = Experiment

class StudyExperimentForm(ModelForm):
	class Meta:
		model = Experiment
		exclude = ['study',]


class MeasurementForm(ModelForm):
	animal = forms.ModelChoiceField(queryset=Animal.objects.all())
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
