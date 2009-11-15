from mousedb.data.models import Experiment, Measurement
from mousedb.animal.models import Animal
from django.forms import ModelForm
from django import forms


class ExperimentForm(ModelForm):
	class Meta:
		model = Experiment

class MeasurementForm(ModelForm):
	animal = forms.ModelChoiceField(queryset=Animal.objects.all())
	class Meta:
		model = Measurement


