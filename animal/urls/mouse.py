from django.conf.urls.defaults import *

from django.views.generic.list_detail import object_list, object_detail
from django.contrib.auth.decorators import login_required

@login_required
def limited_object_list(*args, **kwargs):
	return object_list(*args, **kwargs)

from mousedb.animal.models import Animal

urlpatterns = patterns('',
	(r'^$', limited_object_list, {
		'queryset': Animal.objects.filter(Alive=True),
		'template_name': 'animal_list.html', 
		'template_object_name': 'animal',
		}),
	(r'^(?P<id>\d*)/$', 'mousedb.animal.views.animal_detail'),
	(r'^(?P<animal_id>\d*)/change/$', 'mousedb.animal.views.animal_change'),
	(r'^new/$', 'mousedb.animal.views.animal_new'),
	(r'^new/$', 'django.views.generic.create_update.create_object', {
		'model': Animal, 
		'template_name': 'animal_form.html', 
		'login_required':True,
		'post_save_redirect':'/mousedb/mouse/'
		}),
	(r'^(?P<object_id>\d*)/update/$', 'django.views.generic.create_update.update_object', {
		'model': Animal, 
		'template_name': 'animal_form.html', 
		'login_required':True,
		'post_save_redirect':'/mousedb/mouse/',
		}),
	(r'^(?P<object_id>\d*)/delete/$', 'django.views.generic.create_update.delete_object', {
		'model': Animal, 
		'login_required':True,
		'post_delete_redirect':'/mousedb/mouse/',
		}),
)

