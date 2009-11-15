from django.forms import ModelForm
from django import forms
from django.contrib.admin import widgets   

from mousedb.animal.models import Animal

class AnimalChangeForm(ModelForm):
	class Meta:
		model = Animal
		fields = ['Strain','Background','MouseID', 'Markings', 'Cage', 'Rack', 'Rack_Position', 'Genotype', 'Death', 'Cause_of_Death']

class AnimalForm(ModelForm):
	CageID = forms.IntegerField()
	class Meta:
		model = Animal
		exclude = ['Cage',]






