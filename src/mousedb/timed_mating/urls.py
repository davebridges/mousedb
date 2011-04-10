"""This urlconf sets the directions for the timed_mating app.

It takes a url in the form of /plug/something and sends it to the appropriate view class or function."""

from django.conf.urls.defaults import *

from mousedb.timed_mating.views import PlugEventsList, StrainPlugEventsList, PlugEventsDetail, PlugEventsCreate, PlugEventsUpdate, PlugEventsDelete

urlpatterns = patterns('',
    url(r'^$', PlugEventsList.as_view(), name="plugevents-list"),
    url(r'^strain/(\w*)/$', StrainPlugEventsList.as_view(), name="strain-plugevents-list"),
    url(r'^(?P<pk>\d*)/$', PlugEventsDetail.as_view(), name="plugevents-detail"),
    url(r'^new/$', PlugEventsCreate.as_view(), name="plugevents-new"),
    url(r'^(?P<pk>\d*)/edit/$', PlugEventsUpdate.as_view(), name="plugevents-edit"),
    url(r'^(?P<pk>\d*)/delete/$', PlugEventsDelete.as_view(), name="plugevents-delete"),
    url(r'^breeding/(?P<breeding_id>\d*)/new', 'mousedb.timed_mating.views.breeding_plugevent', name="breeding-plugevents-new"),
)
