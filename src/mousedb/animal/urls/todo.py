"""URL configuration file for todo subpages.

This controls any page **/mousedb/todo/...** and sends it to the appropriate views."""

from django.conf.urls.defaults import *

from mousedb.animal import views

urlpatterns = patterns('',
	url(r'^/?$', 'mousedb.animal.views.todo', name="todo-list"),
    url(r'^eartag/?$', views.EarTagList.as_view(), name="todo-eartags"),
	url(r'^genotype/$', views.GenotypeList.as_view(), name="todo-genotype"),
	url(r'^wean/$',views.WeanList.as_view(), name="todo-weaning"),
	url(r'^no_cage/$', views.NoCageList.as_view(), name="todo-no-cage"),
	url(r'^no_rack/$', views.NoRackList.as_view(), name="todo-no-rack"),
)
