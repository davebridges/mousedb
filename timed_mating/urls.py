from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list, object_detail
from django.contrib.auth.decorators import login_required

from mousedb.timed_mating.models import PlugEvents

@login_required
def limited_object_list(*args, **kwargs):
	return object_list(*args, **kwargs)

@login_required
def limited_object_detail(*args, **kwargs):
	return object_detail(*args, **kwargs)

urlpatterns = patterns('',
	(r'^$', limited_object_list, {
		'queryset': PlugEvents.objects.all(),
		'template_name': 'plug_list.html',
		'template_object_name': 'plug',
		}),
	(r'^(?P<object_id>\d*)/$', limited_object_detail, {
		'queryset': PlugEvents.objects.all(),
		'template_name': 'plug_detail.html',
		'template_object_name': 'plug',
		}),
	(r'^new/$', 'django.views.generic.create_update.create_object', {
		'model': PlugEvents, 
		'template_name': 'plug_form.html', 
		'login_required':True,
		'post_save_redirect':'/mousedb/plug_events/'
		}),
	(r'^(?P<object_id>\d*)/edit/$', 'django.views.generic.create_update.update_object', {
		'model': PlugEvents, 
		'template_name': 'plug_form.html', 
		'login_required':True,
		'post_save_redirect':'/mousedb/plug_events/'
		}),
	(r'^(?P<object_id>\d*)/delete/$', 'django.views.generic.create_update.delete_object', {
		'model': PlugEvents, 
		'login_required':True,
		'post_delete_redirect':'/mousedb/plug_events/'
		}),
	(r'^breeding/(?P<breeding_id>\d*)/new', 'mousedb.timed_mating.views.breeding_plugevent'),
)
