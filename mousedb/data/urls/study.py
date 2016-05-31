"""This URLconf defines the routing of pages for study objects.

This includes generic views for study list, study details and create, change and delete studies."""

from django.conf.urls import url

from mousedb.data import views

urlpatterns = [
	url(r'^$', views.StudyList.as_view(), name="study-list"),
	url(r'^new/$', views.StudyCreate.as_view(), name="study-new"),
	url(r'^(?P<pk>\d*)/$', views.StudyDetail.as_view(), name="study-detail"),
	url(r'^(?P<pk>\d*)/edit/$', views.StudyUpdate.as_view(), name="study-edit"),
	url(r'^(?P<pk>\d*)/delete/$', views.StudyDelete.as_view(), name = "study-delete"),
	url(r'^(?P<pk>\d*)/experiment/new/$', views.study_experiment, name="study-experiment-new"),
	url(r'^aging$', views.StudyAgeing.as_view(), name="study-aging-detail"),
    url(r'^aging/all.csv', views.aging_csv, name="aging-csv"),
    url(r'^litters/all.csv', views.litters_csv, name="litters-csv")
]
