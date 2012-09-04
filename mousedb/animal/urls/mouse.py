"""This url dispatcher for animal objects

controls views in the form */mouse...*, */mice...* or */animal...*

This includes create, update, delete views as well as animal-list, and animal-list all and animal-multiple-new."""

from django.conf.urls.defaults import *

from mousedb.animal import views

urlpatterns = patterns('',
    url(r'^$', views.AnimalListAlive.as_view(), name="animal-list"),
    url(r'^all/?$', views.AnimalList.as_view(), name="animal-list-all"),    
	url(r'^(?P<pk>\d*)/?$', views.AnimalDetail.as_view(), name="animal-detail"),
	url(r'^new/?$', views.AnimalCreate.as_view(), name="animal-new"),
	url(r'^(?P<pk>\d*)/update/?$', views.AnimalUpdate.as_view(), name="animal-update"),
	url(r'^(?P<pk>\d*)/edit/?$', views.AnimalUpdate.as_view(), name="animal-update"),    
	url(r'^(?P<pk>\d*)/delete/?$', views.AnimalDelete.as_view(), name="animal-delete"),
	url(r'^new/multiple/?$', 'mousedb.animal.views.multiple_pups', name="animal-multiple-new"),			
		)

