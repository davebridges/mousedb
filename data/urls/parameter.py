from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list, object_detail
from django.contrib.auth.decorators import login_required

from mousedb.data.models import Pharmaceutical, Diet

@login_required
def limited_object_list(*args, **kwargs):
	return object_list(*args, **kwargs)

@login_required
def limited_object_detail(*args, **kwargs):
	return object_detail(*args, **kwargs)

@permission_required('data.add_experiment')
def create_experiment(*args, **kwargs):
	return django.views.generic.create_update.create_object(*args, **kwargs)

@permission_required('data.change_experiment')
def change_experiment(*args, **kwargs):
	return django.views.generic.create_update.update_object(*args, **kwargs)

@permission_required('data.delete_experiment')
def delete_experiment(*args, **kwargs):
	return django.views.generic.create_update.update_object(*args, **kwargs)


urlpatterns = patterns('',
	(r'^pharmaceuticals?/(?P<object_id>\d*)', limited_object_detail, {
		'queryset': Pharmaceutical.objects.all(),
		'template_name': 'pharmaceutical_detail.html',
		'template_object_name': 'pharmaceutical',
		}),
	(r'^diets?/(?P<object_id>\d*)', limited_object_detail, {
		'queryset': Diet.objects.all(),
		'template_name': 'diet_detail.html',
		'template_object_name': 'diet',
		}),
)
