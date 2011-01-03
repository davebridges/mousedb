"""This package describes forms used by the Timed Mating app."""

from django import forms

from mousedb.timed_mating.models import PlugEvents

class BreedingPlugForm(forms.ModelForm):
    """This form is used to enter Plug Events from a specific breeding cage."""
    class Meta:
        model = PlugEvents
        exclude = ['Breeding']

