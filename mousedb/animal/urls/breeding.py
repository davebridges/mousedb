"""This URLconf defines the routing of pages for breeding objects.

This includes generic views for breeding, breeding details and create, change, search and delete breeding cages."""

from django.conf.urls import url

from mousedb.animal import views

urlpatterns = [
	url(r'^$', views.BreedingList.as_view(), name="breeding-list"),
	url(r'all/?$', views.BreedingListAll.as_view(), name="breeding-list-all"),
	url(r'timed_mating/?$', views.BreedingListTimedMating.as_view(), name="breeding-list-timed-matings"),    
	url(r'^(?P<pk>\d*)/?$', views.BreedingDetail.as_view(), name="breeding-detail"),
	url(r'^(?P<breeding_id>\d*)/pups/?$', views.breeding_pups, name="breeding-pups"),
	url(r'^(?P<breeding_id>\d*)/change/?$', views.breeding_change, name="breeding-pups-change"),
	url(r'^(?P<breeding_id>\d*)/wean/?$', views.breeding_wean, name="breeding-pups-wean"),	
	url(r'^(?P<breeding_id>\d*)/multiple/?$', views.multiple_breeding_pups, name="animal-multiple-pups-new"),	
	url(r'^new/?$', views.BreedingCreate.as_view(), name="breeding-new"),
	url(r'^(?P<pk>\d*)/edit/?$', views.BreedingUpdate.as_view(), name="breeding-edit"),
	url(r'^(?P<pk>\d*)/update/?$', views.BreedingUpdate.as_view(), name="breeding-edit"),    
	url(r'^(?P<pk>\d*)/delete/?$', views.BreedingDelete.as_view(), name="breeding-delete"),
    url(r'^search/?', views.BreedingSearch.as_view(), name="breeding-search")
]
