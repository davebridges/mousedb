'''This is the urlconf for cage urls.'''

from django.conf.urls import *

from mousedb.animal import views
		
urlpatterns = patterns('',
	url(r'^/?$', views.CageList.as_view(), name="cage-list"),
	url(r'^all/?$', views.CageListAll.as_view(), name="cage-list-all"),
	url(r'^(?P<cage_number>\d*)/$', views.CageDetail.as_view(), name="cage-detail"),
		)