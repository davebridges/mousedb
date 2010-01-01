from django.conf.urls.defaults import *
from django.contrib.auth.decorators import permission_required

from mousedb.animal.models import Strain

@permission_required('animal.add_strain')
def create_strain(*args, **kwargs):
	return django.views.generic.create_update.create_object(*args, **kwargs)

@permission_required('animal.change_strain')
def change_strain(*args, **kwargs):
	return django.views.generic.create_update.update_object(*args, **kwargs)

@permission_required('animal.delete_strain')
def delete_strain(*args, **kwargs):
	return django.views.generic.create_update.update_object(*args, **kwargs)

urlpatterns = patterns('',
        (r'^$', 'mousedb.animal.views.strain_list'),
		(r'^new/$', create_strain, {
		'model': Strain, 
		'template_name': 'strain_new.html', 
		'login_required':True,
		'post_save_redirect':'/mousedb/strain/'
		}),
	(r'^(?P<object_id>\d*)/update/$', change_strain, {
		'model': Strain, 
		'template_name': 'strain_update.html', 
		'login_required':True,
		'post_save_redirect':'/mousedb/strain/',
		}),
	(r'^(?P<object_id>\d*)/delete/$', delete_strain, {
		'model': Strain, 
		'template_name': 'strain_delete.html', 
		'login_required':True,
		'post_delete_redirect':'/mousedb/strain/',
		}),
        (r'^(?P<strain>.*)/$', 'mousedb.animal.views.strain_detail'),
        (r'^(?P<strain>.*)/all$', 'mousedb.animal.views.strain_detail_all'),
)
