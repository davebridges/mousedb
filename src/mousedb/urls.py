"""Generic base url directives.

These directives will redirect requests to app specific pages, and provide redundancy in possible names."""

from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	#(r'^', 'django.views.generic.simple.direct_to_template', {'template': 'maintenance.html'}),
	(r'^ajax_select/', include('ajax_select.urls')),	
	(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	(r'^admin/', include(admin.site.urls)),
	url(r'^accounts/login/', 'django.contrib.auth.views.login', name="login"),

	url(r'^mouse/', include('mousedb.animal.urls.mouse')),
	url(r'^mice/', include('mousedb.animal.urls.mouse')),
	url(r'^animals?/', include('mousedb.animal.urls.mouse')),
	url(r'^strains?/', include('mousedb.animal.urls.strain')),
	url(r'^dates?/', include('mousedb.animal.urls.date')),
	url(r'^breedings?/', include('mousedb.animal.urls.breeding')),
	url(r'^breeding_cages?/', include('mousedb.animal.urls.breeding')),
	url(r'^todo/', include('mousedb.animal.urls.todo')),
	url(r'^cages?/', include('mousedb.animal.urls.cage')),
	
	url(r'^experiments?/', include('mousedb.data.urls.experiment')),
	url(r'^study/', include('mousedb.data.urls.study')),
	url(r'^studies/', include('mousedb.data.urls.study')),
	url(r'^treatments?/', include('mousedb.data.urls.treatment')),
	url(r'^parameters?/', include('mousedb.data.urls.parameter')),

	url(r'^plugs?/', include('mousedb.timed_mating.urls')),
	url(r'^plugevents?/', include('mousedb.timed_mating.urls')),
	url(r'^plug_events?/', include('mousedb.timed_mating.urls')),
	url(r'^timedmatings?/', include('mousedb.timed_mating.urls')),
	url(r'^timed_matings?/', include('mousedb.timed_mating.urls')),
	
	url(r'^specs?/$', 'django.views.generic.simple.direct_to_template', {'template': 'specs.html'}, name="specs"),
	url(r'^index/$', 'mousedb.views.home', name="home"),
	url(r'^/?$', 'mousedb.views.home')
)

