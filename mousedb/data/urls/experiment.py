'''This is the urlconf for experiment urls.

It takes the root /experiment/ plust whatever is shown below'''

from django.conf.urls import *

from mousedb.data import views

urlpatterns = [
	url(r'^$', views.ExperimentList.as_view(), name="experiment-list"),
	url(r'^(?P<pk>\d*)/$', views.ExperimentDetail.as_view(), name="experiment-detail"),
	url(r'^(?P<pk>\d*)/csv', views.experiment_details_csv, name="experiment-detail-csv"),
	url(r'^data_entry/$', views.MeasurementCreate.as_view(), name="data-entry"),
	url(r'^new/$', views.ExperimentCreate.as_view(), name="experiment-new"),
        url(r'^(?P<pk>\d*)/delete/$', views.ExperimentDelete.as_view(), name="experiment-delete"),	
        url(r'^(?P<pk>\d*)/edit/$', views.ExperimentUpdate.as_view(), name="experiment-edit"),		
	url(r'^data/all$', views.MeasurementList.as_view(), name="measurement_list"),
	url(r'^data/all.csv$', views.MeasurementListCSV.as_view(), name="measurement_list_csv"),        
	url(r'^data/(?P<pk>\d*)/edit/$', views.MeasurementUpdate.as_view(), name="measurement-edit"),
	url(r'^data/(?P<pk>\d*)/delete/$', views.MeasurementDelete.as_view(), name = "measurement-delete"),
]
