from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list, object_detail
from django.contrib.auth.decorators import login_required

from mousedb.data.forms import ExperimentForm
from mousedb.data.models import Measurement, Experiment

@login_required
def limited_object_list(*args, **kwargs):
	return object_list(*args, **kwargs)

@login_required
def limited_object_detail(*args, **kwargs):
	return object_detail(*args, **kwargs)


urlpatterns = patterns('',
	(r'^$', 'mousedb.data.views.experiment_list'),
	(r'^(?P<object_id>\d*)/$', limited_object_detail, {
		'queryset': Experiment.objects.all(),
		'template_name': 'experiment_detail.html',
		'template_object_name': 'experiment',
		}),
	(r'^(?P<experiment_id>\d*)/data_entry/$', 'mousedb.data.views.add_measurement'),
	(r'^new/$', 'django.views.generic.create_update.create_object', {
		'form_class': ExperimentForm, 
		'template_name': 'experiment_new.html', 
		'login_required':True,
		'post_save_redirect':'/mousedb/experiment/'
		}),
	(r'^data/all$', limited_object_list, {
		'queryset': Measurement.objects.all(),
		'template_name': 'data.html',
		'template_object_name': 'data',
		}),
)
