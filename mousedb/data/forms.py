from django.forms import ModelForm
from django import forms
from django.contrib.admin import widgets
from django.forms.models import inlineformset_factory

from ajax_select.fields import AutoCompleteSelectMultipleField, AutoCompleteSelectField

from mousedb.data.models import Experiment, Measurement, Study, Treatment, Cohort
from mousedb.animal.models import Animal

class ExperimentForm(ModelForm):
    """This is the configuration for the experiment form.

    This form is used to set up and modify an experiment.  It uses a datepicker widget for the date.
    """
    class Meta:
        model = Experiment

		

class StudyExperimentForm(ModelForm):
    """This is the configuration for a study form (From an experiment).
	
    This hides the study field which will be automatically set upon save."""
    class Meta:
        model = Experiment
        exclude = ['study',]

		
MeasurementFormSet = inlineformset_factory(Experiment, Measurement, extra=10, can_delete=True)

class MeasurementForm(ModelForm):
    """Form definition for adding and editing measurements.
	
    This form is used for adding or modifying single measurements from within an experiment.
    It has an autocomplete field for animal."""
    
    animal = AutoCompleteSelectField('animal', required=False)
    
    class Meta:
        model = Measurement
	
class StudyForm(ModelForm):
    """This is the configuration for the study form.

    This form is used to create and modify studies.  It uses an autocomplete widget for the animals."""
    class Meta:
        model = Study
           

class TreatmentForm(ModelForm):
    """Form class for study treatment groups.

<<<<<<< HEAD
    In the case of studies, animals are defined in the treatment group rather than in the study group.  
    A treatment consists of a study, a set of animals and the conditions which define that treatment.  
    This includes related fields for environment, diet, implants and transplants."""
    animals = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,
        queryset=Animal.objects.all())
    class Meta:
        model = Treatment

class CohortForm(ModelForm):
    """This form is for entering and editing cohort information.

    The form over-rides the animals field and replaces it with a checkbox.
    This is to prevent accidental unclicking of animals."""
    
    animals = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,
        queryset=Animal.objects.filter(Alive=True))
    class Meta:
        model = Cohort
=======
    In the case of studies, animals are defined in the treatment group rather than in the study group.  A treatment consists of a study, a set of animals and the conditions which define that treatment.  This includes related fields for environment, diet, implants and transplants."""
    animals = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,
        queryset=Animal.objects.all())
    class Meta:
        model = Treatment
>>>>>>> b08f77528cf3648df7c5a4cccae0ef4c4c908b5d
