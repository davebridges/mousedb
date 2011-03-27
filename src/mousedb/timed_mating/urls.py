"""This urlconf sets the directions for the timed_mating app.

It comprises of create, update, delete, detail and list of plug events."""

from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_detail
from django.views.generic.create_update import create_object, update_object, delete_object
from django.contrib.auth.decorators import login_required, permission_required

from mousedb.timed_mating.models import PlugEvents
from mousedb.timed_mating.views import PlugEventsListView, StrainPlugEventsListView, PlugEventsDetailView


@login_required
def limited_object_detail(*args, **kwargs):
	return object_detail(*args, **kwargs)

@permission_required('timed_mating.add_plugevents')
def create_plugevents(*args, **kwargs):
	return create_object(*args, **kwargs)

@permission_required('timed_mating.change_plugevents')
def change_plugevents(*args, **kwargs):
	return update_object(*args, **kwargs)

@permission_required('timed_mating.delete_plugevents')
def delete_plugevents(*args, **kwargs):
	return delete_object(*args, **kwargs)

urlpatterns = patterns('',
    url(r'^$', PlugEventsListView.as_view(), name="plugevents-list"),
    url(r'^strain/(\w+)/$', StrainPlugEventsListView.as_view(), name="strain-plugevents-list"),
	url(r'^(?P<pk>\d*)/$', PlugEventsDetailView.as_view(), name="plugevents-detail"),
	url(r'^new/$', create_plugevents, {
		'model': PlugEvents, 
		'template_name': 'plug_form.html', 
		'login_required':True,
		'post_save_redirect':'/mousedb/plug_events/'
		}, name="plugevents-new"),
	url(r'^(?P<object_id>\d*)/edit/$', change_plugevents, {
		'model': PlugEvents, 
		'template_name': 'plug_form.html', 
		'login_required':True,
		'post_save_redirect':'/mousedb/plug_events/'
		}, name="plugevents-edit"),
	url(r'^(?P<object_id>\d*)/delete/$', delete_plugevents, {
		'model': PlugEvents, 
		'login_required':True,
		'post_delete_redirect':'/mousedb/plug_events/',
		'template_name':'confirm_delete.html'
		}, name="plugevents-delete"),
	url(r'^breeding/(?P<breeding_id>\d*)/new', 'mousedb.timed_mating.views.breeding_plugevent', name="breeding-plugevents-new"),
)
