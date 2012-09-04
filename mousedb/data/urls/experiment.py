from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, update_object, delete_object
from django.contrib.auth.decorators import login_required, permission_required

from mousedb.data.forms import ExperimentForm, MeasurementForm
from mousedb.data.models import Measurement, Experiment
from mousedb.data.views import all_data_csv

@login_required
def limited_object_list(*args, **kwargs):
	return object_list(*args, **kwargs)

@login_required
def limited_object_detail(*args, **kwargs):
	return object_detail(*args, **kwargs)

@permission_required('data.add_experiment')
def create_experiment(*args, **kwargs):
	return create_object(*args, **kwargs)

@permission_required('data.change_experiment')
def change_experiment(*args, **kwargs):
	return update_object(*args, **kwargs)

@permission_required('data.delete_experiment')
def delete_experiment(*args, **kwargs):
	return delete_object(*args, **kwargs)
	
@permission_required('data.change_measurement')
def change_measurement(*args, **kwargs):
	return update_object(*args, **kwargs)

@permission_required('data.delete_measurement')
def delete_measurement(*args, **kwargs):
	return delete_object(*args, **kwargs)	

urlpatterns = patterns('',
	url(r'^$', 'mousedb.data.views.experiment_list', name="experiment-list"),
	url(r'^(?P<object_id>\d*)/$', limited_object_detail, {
		'queryset': Experiment.objects.all(),
		'template_name': 'experiment_detail.html',
		'template_object_name': 'experiment',
		}, name="experiment-detail"),
	url(r'^(?P<experiment_id>\d*)/csv', 'mousedb.data.views.experiment_details_csv', name="experiment-detail-csv"),
	url(r'^(?P<experiment_id>\d*)/data_entry/$', 'mousedb.data.views.add_measurement', name="data-entry"),
	url(r'^new/$', create_experiment, {
		'form_class': ExperimentForm, 
		'template_name': 'experiment_form.html', 
		'login_required':True,
		'post_save_redirect':'/mousedb/experiment/'
		}, name="experiment-new"),
	url(r'^(?P<object_id>\d*)/edit/$', change_experiment, {
		'form_class': ExperimentForm,
		'template_name': 'experiment_form.html',
		}, name="experiment-edit"),		
	url(r'^data/all$', limited_object_list, {
		'queryset': Measurement.objects.all(),
		'template_name': 'data.html',
		'template_object_name': 'data',
		}, name="measurement_list"),
	url(r'^data/all.csv$', all_data_csv, name="measurement_list_csv"),        
	url(r'^data/(?P<object_id>\d*)/edit/$', change_measurement, {
		'form_class': MeasurementForm,
		'template_name': 'measurement_form.html',
		}, name="measurement-edit"),
	url(r'^(?P<object_id>\d*)/delete/$', delete_measurement, {
		'model': Measurement,
		'post_delete_redirect': '/mousedb/data/',
		'template_name' : 'confirm_delete.html',
		}, name = "measurement-delete"),
)
