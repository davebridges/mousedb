'''This module generates the views for the veterinary app.

There is one generic home view for the entire app as well as detail, create update and delete views for these models:

* :class:`~mousedb.veterinary.models.MedicalIssue`
* :class:`~mousedb.veterinary.models.MedicalCondition`
* :class:`~mousedb.veterinary.models.MedicalTreatment`

'''

from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy

from braces.views import LoginRequiredMixin, PermissionRequiredMixin

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
    
    It passes an object **medical_issue** when the url **/veterinary/medical-issue/<pk#>** is requested.'''

    model = MedicalIssue
    context_object_name = 'medical_issue'
    template_name = 'medical_issue_detail.html'
    
class MedicalIssueCreate(PermissionRequiredMixin, CreateView):
    '''This view is for creating a new :class:`~mousedb.veterinary.MedicalIssue`.
    
    It requires the permissions to create a new medical issue and is found at the url **/veterinary/medical-issue/new**.'''
    
    permission_required = 'veterinary.create_medicalissue'
    model = MedicalIssue
    fields = '__all__'
    template_name = 'medical_issue_form.html'
    
class MedicalIssueUpdate(PermissionRequiredMixin, UpdateView):
    '''This view is for updating a :class:`~mousedb.veterinary.MedicalIssue`.
    
    It requires the permissions to update a medical issue and is found at the url **/veterinary/medical-issue/<pk$>/edit**.'''
    
    permission_required = 'veterinary.update_medicalissue'
    model = MedicalIssue
    fields = '__all__'
    context_object_name = 'medical_issue'
    template_name = 'medical_issue_form.html'   
    
class MedicalIssueDelete(PermissionRequiredMixin, DeleteView):
    '''This view is for deleting a :class:`~mousedb.veterinary.MedicalIssue`.
    
    It requires the permissions to delete a medical issue and is found at the url **/veterinary/medical-issue/<pk$>/delete**.'''
    
    permission_required = 'veterinary.delete_medicalissue'
    model = MedicalIssue
    template_name = 'confirm_delete.html' 
    success_url = reverse_lazy('veterinary-home')        
    
class MedicalConditionDetail(LoginRequiredMixin, DetailView):
    '''This view is for details of a particular :class:`~mousedb.veterinary.MedicalCondition`.
    
    It passes an object **medical_condition** when the url **/veterinary/medical-condition/<slug>** is requested.'''

    model = MedicalCondition
    context_object_name = 'medical_condition'
    template_name = 'medical_condition_detail.html'
    
class MedicalConditionCreate(PermissionRequiredMixin, CreateView):
    '''This view is for creating a new :class:`~mousedb.veterinary.MedicalCondition`.
    
    It requires the permissions to create a new medical issue and is found at the url **/veterinary/medical-condition/new**.'''
    
    permission_required = 'veterinary.create_medicalcondition'
    model = MedicalCondition
    fields = '__all__'
    template_name = 'medical_condition_form.html'
    
class MedicalConditionUpdate(PermissionRequiredMixin, UpdateView):
    '''This view is for updating a :class:`~mousedb.veterinary.MedicalCondition`.
    
    It requires the permissions to update a medical issue and is found at the url **/veterinary/medical-condition/<slug>/edit**.'''
    
    permission_required = 'veterinary.update_medicalcondition'
    model = MedicalCondition
    fields = '__all__'
    context_object_name = 'medical_condition'
    template_name = 'medical_condition_form.html'   
    
class MedicalConditionDelete(PermissionRequiredMixin, DeleteView):
    '''This view is for deleting a :class:`~mousedb.veterinary.MedicalCondition`.
    
    It requires the permissions to delete a medical issue and is found at the url **/veterinary/medical-condition/<slug>/delete**.'''
    
    permission_required = 'veterinary.delete_medicalcondition'
    model = MedicalCondition
    template_name = 'confirm_delete.html' 
    success_url = reverse_lazy('veterinary-home')     
    
class MedicalTreatmentDetail(LoginRequiredMixin, DetailView):
    '''This view is for details of a particular :class:`~mousedb.veterinary.MedicalTreatment`.
    
    It passes an object **medical_treatment** when the url **/veterinary/medical-treatment/<slug>** is requested.'''

    model = MedicalTreatment
    context_object_name = 'medical_treatment'
    template_name = 'medical_treatment_detail.html' 
    
class MedicalTreatmentCreate(PermissionRequiredMixin, CreateView):
    '''This view is for creating a new :class:`~mousedb.veterinary.MedicalTreatment`.
    
    It requires the permissions to create a new medical issue and is found at the url **/veterinary/medical-treatment/new**.'''
    
    permission_required = 'veterinary.create_medicaltreatment'
    model = MedicalTreatment
    fields = '__all__'
    template_name = 'medical_treatment_form.html'
    
class MedicalTreatmentUpdate(PermissionRequiredMixin, UpdateView):
    '''This view is for updating a :class:`~mousedb.veterinary.MedicalTreatment`.
    
    It requires the permissions to update a medical issue and is found at the url **/veterinary/medical-treatment/<slug>/edit**.'''
    
    permission_required = 'veterinary.update_medicaltreatment'
    model = MedicalTreatment
    fields = '__all__'
    context_object_name = 'medical_treatment'
    template_name = 'medical_treatment_form.html'   
    
class MedicalTreatmentDelete(PermissionRequiredMixin, DeleteView):
    '''This view is for deleting a :class:`~mousedb.veterinary.MedicalTreatment`.
    
    It requires the permissions to delete a medical issue and is found at the url **/veterinary/medical-treatment/<slug>/delete**.'''
    
    permission_required = 'veterinary.delete_medicaltreatment'
    model = MedicalTreatment
    template_name = 'confirm_delete.html' 
    success_url = reverse_lazy('veterinary-home')               
