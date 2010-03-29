from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, update_object, delete_object
from django.contrib.auth.decorators import login_required, permission_required

from data.models import Study

@login_required
def limited_object_list(*args, **kwargs):
	return object_list(*args, **kwargs)

@login_required
def limited_object_detail(*args, **kwargs):
	return object_detail(*args, **kwargs)

@permission_required('data.add_study')
def create_study(*args, **kwargs):
	return create_object(*args, **kwargs)

@permission_required('data.change_study')
def change_study(*args, **kwargs):
	return update_object(*args, **kwargs)

@permission_required('data.delete_study')
def delete_study(*args, **kwargs):
	return delete_object(*args, **kwargs)

urlpatterns = patterns('',
	(r'^$', limited_object_list, {
		'queryset': Study.objects.all(),
		'template_name': 'study_list.html',
		'template_object_name': 'study',
		}),
	(r'^new/$', create_study, {
		'model': Study,
		'template_name': 'study_form.html',
		}),
	(r'^(?P<object_id>\d*)/$', limited_object_detail, {
		'queryset': Study.objects.all(),
		'template_name': 'study_detail.html',
		'template_object_name': 'study',
		}),
	(r'^(?P<object_id>\d*)/edit/$', change_study, {
		'model': Study,
		'template_name': 'study_form.html',
		}),
	(r'^(?P<object_id>\d*)/delete/$', delete_study, {
		'model': Study,
		'post_save_redirect': '/mousedb/study',
		'template_name' : 'confirm_delete.html',
		}),
	(r'^(?P<study_id>\d*)/experiment/new/$', 'mousedb.data.views.study_experiment'),
)
