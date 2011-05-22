"""This URLconf defines the routing of pages for breeding objects.

This includes generic views for breeding, breeding details and create, change and delete breeding cages."""

from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list
from django.views.generic.create_update import create_object, update_object, delete_object
from django.contrib.auth.decorators import login_required, permission_required

from mousedb.animal import views
from mousedb.animal.models import Breeding
from mousedb.animal.forms import BreedingForm

@login_required
def limited_object_list(*args, **kwargs):
	return object_list(*args, **kwargs)

@permission_required('animal.add_breeding')
def create_breeding(*args, **kwargs):
	return create_object(*args, **kwargs)

@permission_required('animal.change_breeding')
def change_breeding(*args, **kwargs):
	return update_object(*args, **kwargs)

@permission_required('animal.delete_breeding')
def delete_breeding(*args, **kwargs):
	return delete_object(*args, **kwargs)

urlpatterns = patterns('',
	url(r'^$', views.BreedingList.as_view(), name="breeding-list"),
	url(r'all/?$', views.BreedingListAll.as_view(), name="breeding-list-all"),
	url(r'timed_mating/?$', views.BreedingListTimedMating.as_view(), name="breeding-list-timed-matings"),    
	url(r'^(?P<pk>\d*)/?$', views.BreedingDetail.as_view(), name="breeding-detail"),
	url(r'^(?P<breeding_id>\d*)/pups/?$', 'mousedb.animal.views.breeding_pups', name="breeding-pups"),
	url(r'^(?P<breeding_id>\d*)/change/?$', 'mousedb.animal.views.breeding_change', name="breeding-pups-change"),
	url(r'^(?P<breeding_id>\d*)/wean/?$', 'mousedb.animal.views.breeding_wean', name="breeding-pups-wean"),	
	url(r'^(?P<breeding_id>\d*)/multiple/?$', 'mousedb.animal.views.multiple_breeding_pups', name="animal-multiple-pups-new"),	
	url(r'^new/?$', views.BreedingCreate.as_view(), name="breeding-new"),
	url(r'^(?P<pk>\d*)/edit/?$', views.BreedingUpdate.as_view(), name="breeding-edit"),
	url(r'^(?P<pk>\d*)/delete/?$', views.BreedingDelete.as_view(), name="breeding-delete"),
)
