'''This module generates the views for the veterinary app.

There is one generic home view for the entire app as well as detail views for these models:

* :class:`~mousedb.veterinary.models.MedicalIssue`
* :class:`~mousedb.veterinary.models.MedicalCondition`
* :class:`~mousedb.veterinary.models.MedicalTreatment`

'''

from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView

from mousedb.veterinary.models import MedicalIssue,MedicalCondition,MedicalTreatment

class VeterinaryHome(TemplateView):

    template_name = "veterinary_home.html"

    def get_context_data(self, **kwargs):
        context = super(VeterinaryHome, self).get_context_data(**kwargs)
        context['medical_issues'] = MedicalIssue.objects.all()
        context['medical_conditions'] = MedicalCondition.objects.all()
        context['medical_treatments'] = MedicalTreatment.objects.all()               
        return context
        
class MedicalIssueDetail(DetailView):
    pass  
    
class MedicalConditionDetail(DetailView):
    pass
    
class MedicalTreatmentDetail(DetailView):
    pass              
