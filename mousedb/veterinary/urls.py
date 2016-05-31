"""This urlconf sets the directions for the veterinary app.

It takes a url in the form of **/veterinary/something** and sends it to the appropriate view class or function based on that something."""

from django.conf.urls import url

from mousedb.veterinary.views import *

urlpatterns = [
    url(r'$', VeterinaryHome.as_view(), name="veterinary-home"),
    
    url(r'^medical-issue/new/?$', MedicalIssueCreate.as_view(), name="medical-issue-new"),    
    url(r'^medical-issue/(?P<pk>[\d]+)/?$', MedicalIssueDetail.as_view(), name="medical-issue-detail"),
    url(r'^medical-issue/(?P<pk>[\d]+)/edit/?$', MedicalIssueUpdate.as_view(), name="medical-issue-edit"),
    url(r'^medical-issue/(?P<pk>[\d]+)/delete/?$', MedicalIssueDelete.as_view(), name="medical-issue-delete"), 
           
    url(r'^medical-condition/new/?$', MedicalConditionCreate.as_view(), name="medical-condition-new"), 
    url(r'^medical-condition/(?P<slug>[\w\-]+)/?$', MedicalConditionDetail.as_view(), name="medical-condition-detail"), 
    url(r'^medical-condition/(?P<slug>[\w\-]+)/edit/?$', MedicalConditionUpdate.as_view(), name="medical-condition-edit"), 
    url(r'^medical-condition/(?P<slug>[\w\-]+)/delete/?$', MedicalConditionDelete.as_view(), name="medical-condition-delete"),         

    url(r'^medical-treatment/new/?$', MedicalTreatmentCreate.as_view(), name="medical-treatment-new"),
    url(r'^medical-treatment/(?P<slug>[\w\-]+)/?$', MedicalTreatmentDetail.as_view(), name="medical-treatment-detail"),
    url(r'^medical-treatment/(?P<slug>[\w\-]+)/edit/?$', MedicalTreatmentUpdate.as_view(), name="medical-treatment-edit"),
    url(r'^medical-treatment/(?P<slug>[\w\-]+)/delete/?$', MedicalTreatmentDelete.as_view(), name="medical-treatment-delete")      
]
