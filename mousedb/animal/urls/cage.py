'''This is the urlconf for cage urls.'''

from django.conf.urls import url

from mousedb.animal import views
		
urlpatterns = [
	url(r'^/?$', views.CageList.as_view(), name="cage-list"),
	url(r'^all/?$', views.CageListAll.as_view(), name="cage-list-all"),
	url(r'^(?P<cage_number>\d*)/$', views.CageDetail.as_view(), name="cage-detail"),
]