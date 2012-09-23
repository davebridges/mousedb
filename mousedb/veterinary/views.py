'''This module generates the views for the veterinary app.

There is one generic home view for the entire app as well as detail views for these models:

* :class:`~mousedb.veterinary.models.MedicalIssue`
* :class:`~mousedb.veterinary.models.MedicalCondition`
* :class:`~mousedb.veterinary.models.MedicalTreatment`

'''

from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView

from braces.views import LoginRequiredMixin

from mousedb.veterinary.models import MedicalIssue,MedicalCondition,MedicalTreatment

class VeterinaryHome(LoginRequiredMixin, TemplateView):
    '''This view is the main page for the veterinary app.
    
    This view contains links to all medical issues, conditions and treatments.
    If this becomes too unwieldy over time, it might be necessary to limit medical_issues to the most recent few.'''

    template_name = "veterinary_home.html"

    def get_context_data(self, **kwargs):
        '''Adds to the context all issues, conditions and treatments.'''
        context = super(VeterinaryHome, self).get_context_data(**kwargs)
        context['medical_issues'] = MedicalIssue.objects.all()
        context['medical_conditions'] = MedicalCondition.objects.all()
        context['medical_treatments'] = MedicalTreatment.objects.all()               
        return context
        
class MedicalIssueDetail(LoginRequiredMixin, DetailView):
    '''This view is for details of a particular :class:`~mousedb.veterinary.MedicalIssue`.
    
    It passes an object **medical_issue** when the url **/veterinary/medical-issue/1** is requested.'''

    model = MedicalIssue
    context_object_name = 'medical_issue'
    template_name = 'medical_issue_detail.html'
        
class MedicalConditionDetail(LoginRequiredMixin, DetailView):
    '''This view is for details of a particular :class:`~mousedb.veterinary.MedicalCondition`.
    
    It passes an object **medical_condition** when the url **/veterinary/medical-condition/<slug>** is requested.'''

    model = MedicalCondition
    context_object_name = 'medical_condition'
    template_name = 'medical_condition_detail.html'
    
class MedicalTreatmentDetail(LoginRequiredMixin, DetailView):
    '''This view is for details of a particular :class:`~mousedb.veterinary.MedicalTreatment`.
    
    It passes an object **medical_treatment** when the url **/veterinary/medical-treatment/<slug>** is requested.'''

    model = MedicalTreatment
    context_object_name = 'medical_treatment'
    template_name = 'medical_treatment_detail.html'            
