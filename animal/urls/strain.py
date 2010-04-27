from django.conf.urls.defaults import *
from django.contrib.auth.decorators import permission_required
from django.views.generic.create_update import create_object, update_object, delete_object

from mousedb.animal.models import Strain

@permission_required('animal.add_strain')
def create_strain(*args, **kwargs):
	return create_object(*args, **kwargs)

@permission_required('animal.change_strain')
def change_strain(*args, **kwargs):
	return update_object(*args, **kwargs)

@permission_required('animal.delete_strain')
def delete_strain(*args, **kwargs):
	return delete_object(*args, **kwargs)

urlpatterns = patterns('',
    url(r'^$', 'mousedb.animal.views.strain_list', name="strain-list"),
	url(r'^new/$', create_strain, {
		'model': Strain, 
		'template_name': 'strain_form.html', 
		'login_required':True,
		'post_save_redirect':'/mousedb/strain/'
		}, name="strain-new"),
	url(r'^(?P<object_id>\d*)/update/$', change_strain, {
		'model': Strain, 
		'template_name': 'strain_form.html', 
		'login_required':True,
		'post_save_redirect':'/mousedb/strain/',
		}, name="strain-edit"),
	url(r'^(?P<object_id>\d*)/delete/$', delete_strain, {
		'model': Strain, 
		'login_required':True,
		'post_delete_redirect':'/mousedb/strain/',
		}, name="strain-delete"),
    url(r'^(?P<strain>.*)/$', 'mousedb.animal.views.strain_detail', name="strain-detail"),
    url(r'^(?P<strain>.*)/all$', 'mousedb.animal.views.strain_detail_all', name="strain-detail-all"),
)
