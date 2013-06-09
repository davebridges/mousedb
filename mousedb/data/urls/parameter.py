'''This is the urlconf for a variety of experimental parameters.'''

from django.conf.urls.defaults import *

from mousedb.data import views


urlpatterns = patterns('',
    url(r'^pharmaceuticals?/?$', views.PharmaceuticalList.as_view(), name="pharmaceutical-list"),
	url(r'^pharmaceuticals?/new/?$', views.PharmaceuticalCreate.as_view(), name="pharmaceutical-new"),    
	url(r'^pharmaceuticals?/(?P<pk>\d*)/?$', views.PharmaceuticalDetail.as_view(), name="pharmaceutical-detail"),
	url(r'^pharmaceuticals?/(?P<pk>\d*)/edit/?$', views.PharmaceuticalUpdate.as_view(), name="pharmaceutical-edit"),
	url(r'^pharmaceuticals?/(?P<pk>\d*)/delete/?$', views.PharmaceuticalDelete.as_view(), name="pharmaceutical-delete"),
	url(r'^diets?/$', views.StudyList.as_view(), name="diet-list"),
	url(r'^diets?/^new/$', views.StudyCreate.as_view(), name="diet-new"),
	url(r'^diets?/^(?P<pk>\d*)/$', views.StudyDetail.as_view(), name="diet-detail"),
	url(r'^diets?/^(?P<pk>\d*)/edit/$', views.StudyUpdate.as_view(), name="diet-edit"),
	url(r'^diets?/^(?P<pk>\d*)/delete/$', views.DietDelete.as_view(), name = "diet-delete")
)
