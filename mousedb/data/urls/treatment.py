"""Url redirections for treatment objects.

This includes gneeric create, update, delete, list and detail views.
These are restricted by login required (for detail and list) and appropriate permissions for forms."""

from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, update_object, delete_object
from django.contrib.auth.decorators import login_required, permission_required

from mousedb.data.models import Treatment
from mousedb.data.forms import TreatmentForm

from mousedb.data import views

@login_required
def limited_object_list(*args, **kwargs):
	return object_list(*args, **kwargs)

@login_required
def limited_object_detail(*args, **kwargs):
	return object_detail(*args, **kwargs)

@permission_required('data.add_treatment')
def create_treatment(*args, **kwargs):
	return create_object(*args, **kwargs)

@permission_required('data.change_treatment')
def change_treatment(*args, **kwargs):
	return update_object(*args, **kwargs)

@permission_required('data.delete_treatment')
def delete_treatment(*args, **kwargs):
	return delete_object(*args, **kwargs)

urlpatterns = patterns('',
	url(r'^$', limited_object_list, {
		'queryset': Treatment.objects.all(),
		'template_name': 'treatment_list.html',
		'template_object_name': 'treatment',
		}, name="treatment-list"),
	url(r'^new/$', create_treatment, {
		'form_class': TreatmentForm,
		'template_name': 'treatment_form.html',
		}, name="treatment-new"),
    url(r'^(?P<pk>\d*)/?$', views.TreatmentDetail.as_view(), name="treatment-detail"),    
	url(r'^(?P<object_id>\d*)/edit/$', change_treatment, {
		'model': Treatment,
		'template_name': 'treatment_form.html',
		}, name="treatment-edit"),
	url(r'^(?P<object_id>\d*)/delete/$', delete_treatment, {
		'model': Treatment,
		'post_save_redirect': '/mousedb/treatment',
		'template_name' : 'confirm_delete.html',
		}, name="treatment-delete"),
)
