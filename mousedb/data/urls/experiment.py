'''This is the urlconf for experiment urls.

It takes the root /experiment/ plust whatever is shown below'''

from django.conf.urls.defaults import *

from mousedb.data import views

urlpatterns = patterns('',
	url(r'^$', views.ExperimentList.as_view(), name="experiment-list"),
	url(r'^(?P<pk>\d*)/$', views.ExperimentDetail.as_view(), name="experiment-detail"),
	url(r'^(?P<pk>\d*)/csv', views.experiment_details_csv, name="experiment-detail-csv"),
	url(r'^(?P<pk>\d*)/data_entry/$', views.add_measurement, name="data-entry"),
	url(r'^new/$', views.ExperimentCreate.as_view(), name="experiment-new"),
	url(r'^(?P<pk>\d*)/edit/$', views.ExperimentUpdate.as_view(), name="experiment-edit"),		
	url(r'^data/all$', views.MeasurementList.as_view(), name="measurement_list"),
	url(r'^data/all.csv$', views.all_data_csv, name="measurement_list_csv"),        
	url(r'^data/(?P<pk>\d*)/edit/$', views.MeasurementUpdate.as_view(), name="measurement-edit"),
	url(r'^(?P<pk>\d*)/delete/$', views.MeasurementDelete.as_view(), name = "measurement-delete"),
)
