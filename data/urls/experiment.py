from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, update_object, delete_object
from django.contrib.auth.decorators import login_required, permission_required

from mousedb.data.forms import ExperimentForm
from mousedb.data.models import Measurement, Experiment

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

urlpatterns = patterns('',
	(r'^$', 'mousedb.data.views.experiment_list'),
	(r'^(?P<object_id>\d*)/$', limited_object_detail, {
		'queryset': Experiment.objects.all(),
		'template_name': 'experiment_detail.html',
		'template_object_name': 'experiment',
		}),
	(r'^(?P<experiment_id>\d*)/data_entry/$', 'mousedb.data.views.add_measurement'),
	(r'^new/$', create_experiment, {
		'form_class': ExperimentForm, 
		'template_name': 'experiment_form.html', 
		'login_required':True,
		'post_save_redirect':'/mousedb/experiment/'
		}),
	(r'^data/all$', limited_object_list, {
		'queryset': Measurement.objects.all(),
		'template_name': 'data.html',
		'template_object_name': 'data',
		}),
)
