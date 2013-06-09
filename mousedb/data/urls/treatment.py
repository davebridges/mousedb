"""This URLconf defines the routing of pages for treatment objects.

This includes generic views for treatment-list, treatment-details and create, change and delete studies."""

from django.conf.urls import *

from mousedb.data import views

urlpatterns = patterns('',
	url(r'^$', views.TreatmentList.as_view(), name="treatment-list"),
	url(r'^new/$', views.TreatmentCreate.as_view(), name="treatment-new"),
    url(r'^(?P<pk>\d*)/?$', views.TreatmentDetail.as_view(), name="treatment-detail"),    
	url(r'^(?P<pk>\d*)/edit/$', views.TreatmentUpdate.as_view(), name="treatment-edit"),
	url(r'^(?P<pk>\d*)/delete/$', views.TreatmentDelete.as_view(), name="treatment-delete"),
)
