"""This module is the url dispatcher for strain related views.

It takes the root */strain...* and generates strain-list, strain-new, strain-edit, strain-delete, strain-detail and views from animal.views."""

from django.conf.urls import *

from mousedb.animal import views
from mousedb.data.views import StrainData, StrainDataCSV

urlpatterns = patterns('',
    url(r'^$', views.StrainList.as_view(), name="strain-list"),
	url(r'^new/?$', views.StrainCreate.as_view(), name="strain-new"),
	url(r'^(?P<slug>[-\w]+)/edit/?$', views.StrainUpdate.as_view(), name="strain-edit"),
	url(r'^(?P<slug>[-\w]+)/update/?$', views.StrainUpdate.as_view(), name="strain-edit"),    
	url(r'^(?P<slug>[-\w]+)/delete/?$', 
	    views.StrainDelete.as_view(), 
	    name="strain-delete"),
    url(r'^(?P<slug>[-\w]+)/all/?$', views.StrainDetailAll.as_view(), name="strain-all"),
    url(r'^(?P<strain_slug>[-\w]+)/data/?$', StrainData.as_view(), name="strain-data"), 
    url(r'^(?P<strain_slug>[-\w]+)/data.csv$', 
        StrainDataCSV.as_view(), 
        name="strain-data-csv"),        
    url(r'^(?P<strain_slug>[-\w]+)/(?P<breeding_type>[\w-]+)/?$', 
        views.CrossTypeAnimalList.as_view(), 
        name="strain-crosstype"),
    url(r'^(?P<slug>[-\w]+)/?$', views.StrainDetail.as_view(), name="strain-detail"),

)
