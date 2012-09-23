"""This urlconf sets the directions for the veterinary app.

It takes a url in the form of **/veterinary/something** and sends it to the appropriate view class or function based on that something."""

from django.conf.urls.defaults import *

from mousedb.veterinary import views

urlpatterns = patterns('',
    url(r'^/?$', views.VeterinaryHome.as_view(), name="veterinary-home"),
    
    url(r'^medical-issue/new/?$', views.MedicalIssueCreate.as_view(), name="medical-issue-new"),    
    url(r'^medical-issue/(?P<pk>[\d]+)/?$', views.MedicalIssueDetail.as_view(), name="medical-issue-detail"),
    url(r'^medical-issue/(?P<pk>[\d]+)/edit/?$', views.MedicalIssueUpdate.as_view(), name="medical-issue-edit"),
    url(r'^medical-issue/(?P<pk>[\d]+)/delete/?$', views.MedicalIssueDelete.as_view(), name="medical-issue-delete"), 
           
    url(r'^medical-condition/(?P<slug>[\w\-]+)/?$', views.MedicalConditionDetail.as_view(), name="medical-condition-detail"),    
    url(r'^medical-treatment/(?P<slug>[\w\-]+)/?$', views.MedicalTreatmentDetail.as_view(), name="medical-treatment-detail"),

)
