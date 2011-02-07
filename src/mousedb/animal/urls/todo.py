"""URL configuration file for todo subpages.

This controls any page /mousedb/todo/ and sends it to the appropriate views."""

import datetime

from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required
from django.views.generic.list_detail import object_list, object_detail
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from mousedb.animal.models import Animal
from mousedb import settings

@login_required
def limited_object_list(*args, **kwargs):
	return object_list(*args, **kwargs)

@login_required
def limited_object_detail(*args, **kwargs):
	return object_detail(*args, **kwargs)

urlpatterns = patterns('',
	url(r'^$', 'mousedb.views.todo', name="todo-list"),
	url(r'^eartag/$', limited_object_list, {
		'queryset': Animal.objects.filter(Born__lt=(datetime.date.today() - datetime.timedelta(days=settings.WEAN_AGE))).filter(MouseID__isnull=True, Alive=True),
		'template_name': 'animal_list.html',
		'template_object_name': 'animal',
		}, name="todo-eartags"),
	url(r'^genotype/$', limited_object_list, {
		'queryset': Animal.objects.filter(Q(Genotype='N.D.')|Q(Genotype__icontains='?')).filter(Alive=True, Born__lt=(datetime.date.today() - datetime.timedelta(days=settings.GENOTYPE_AGE))),
		'template_name': 'animal_list.html',
		'template_object_name': 'animal',
		}, name="todo-genotype"),
	url(r'^wean/$',limited_object_list, {
		'queryset': Animal.objects.filter(Born__lt=(datetime.date.today() - datetime.timedelta(days=settings.WEAN_AGE)),Weaned=None,Alive=True).exclude(Strain__Strain="C57BL/6"),
		'template_name': 'animal_list.html',
		'template_object_name': 'animal',
		}, name="todo-weaning"),
	url(r'^no_cage/$', limited_object_list, {
		'queryset': Animal.objects.filter(Cage__exact=None).filter(Alive=True),
		'template_name': 'animal_list.html',
		'template_object_name': 'animal',
		}, name="todo-no-cage"),
	url(r'^no_rack/$', limited_object_list, {
		'queryset': Animal.objects.filter(Rack__iexact='').filter(Alive=True),
		'template_name': 'animal_list.html',
		'template_object_name': 'animal',
		}, name="todo-no-rack"),
)
