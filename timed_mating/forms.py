from django import forms

from timed_mating.models import PlugEvents

class BreedingPlugForm(forms.ModelForm):
        class Meta:
                model = PlugEvents
                exclude = ['Breeding']

