"""This module is the url dispatcher for strain related views.

It takes the root */strain...* and generates strain-list, strain-new, strain-edit, strain-delete, strain-detail and strain-detail-all views from animal.views."""

from django.conf.urls.defaults import *

from mousedb.animal import views

urlpatterns = patterns('',
    url(r'^$', views.StrainList.as_view(), name="strain-list"),
	url(r'^new/?$', views.StrainCreate.as_view(), name="strain-new"),
	url(r'^(?P<pk>\d*)/edit/?$', views.StrainUpdate.as_view(), name="strain-edit"),
	url(r'^(?P<pk>\d*)/update/?$', views.StrainUpdate.as_view(), name="strain-edit"),    
	url(r'^(?P<pk>\d*)/delete/?$', views.StrainDelete.as_view(), name="strain-delete"),
    url(r'^(?P<slug>[\w-]+)/all/?$', views.StrainDetailAll.as_view(), name="strain-detail-all"),
    url(r'^(?P<slug>[\w-]+)/?$', views.StrainDetail.as_view(), name="strain-detail"),
)
