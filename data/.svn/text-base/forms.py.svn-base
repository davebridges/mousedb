from mousedb.data.models import Experiment, Measurement, Study
from mousedb.animal.models import Animal
from django.forms import ModelForm
from django import forms
from django.contrib.admin import widgets


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

