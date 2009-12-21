from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list
from django.contrib.auth.decorators import login_required

from mousedb.animal.models import Breeding

@login_required
def limited_object_list(*args, **kwargs):
	return object_list(*args, **kwargs)

urlpatterns = patterns('',
	(r'^$', 'mousedb.animal.views.breeding'),
	(r'^all/$', 'mousedb.animal.views.breeding_all'),
	(r'^(?P<breeding_id>\d*)/$', 'mousedb.animal.views.breeding_detail'),
	(r'^(?P<breeding_id>\d*)/pups/$', 'mousedb.animal.views.breeding_pups'),
	(r'^(?P<breeding_id>\d*)/change/$', 'mousedb.animal.views.breeding_change'),
	(r'^new/$', 'django.views.generic.create_update.create_object', {
		'model': Breeding, 
		'template_name': 'breeding_form.html', 
		'login_required':True,
		'post_save_redirect':'/mousedb/breeding/'
		}),
	(r'^(?P<object_id>\d*)/update/$', 'django.views.generic.create_update.update_object', {
		'model': Breeding, 
		'template_name': 'breeding_form.html', 
		'login_required':True,
		'post_save_redirect':'/mousedb/breeding/',
		}),
	(r'^(?P<object_id>\d*)/delete/$', 'django.views.generic.create_update.delete_object', {
		'model': Breeding, 
		'login_required':True,
		'post_delete_redirect':'/mousedb/breeding/',
		}),
	(r'timed_mating/$', limited_object_list, {
		'queryset': Breeding.objects.filter(Timed_Mating=True),
		'template_name': 'breeding.html',
		'template_object_name': 'breeding',
		}),
)
