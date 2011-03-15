from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required
from django.views.generic.date_based import archive_year, archive_month

from mousedb.animal.models import Animal

@login_required
def limited_archive_year(*args, **kwargs):
	return archive_year(*args, **kwargs)

@login_required
def limited_archive_month(*args, **kwargs):
	return archive_month(*args, **kwargs)

urlpatterns = patterns('',
	url(r'^$','mousedb.animal.views.date_archive_year', name="archive-home"), 
	url(r'^(?P<year>\d{4})/$', limited_archive_year, {
		'queryset': Animal.objects.all(),
		'date_field': 'Born',
		'template_name': 'animal_list.html', 
		'template_object_name': 'animal',
		'make_object_list': True,
		}, name="archive-year"),
	url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$', limited_archive_month, {
		'queryset': Animal.objects.all(),
		'date_field': 'Born',
		'month_format': '%m',
		'template_name': 'animal_list.html', 
		'template_object_name': 'animal',
		}, name="archive-month"),
)
