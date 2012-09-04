"""This package is the url dispatcher for date views.

This urlconf takes a url in the form **/date/...** and can generate a general archive, yearly archive or monthly archive."""

from django.conf.urls.defaults import *

from mousedb.animal.views import AnimalYearArchive, AnimalMonthArchive

urlpatterns = patterns('',
	url(r'^$','mousedb.animal.views.date_archive_year', name="archive-home"), 
    url(r'^(?P<year>\d{4})/?$', AnimalYearArchive.as_view(), name="archive-year"),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/?$', AnimalMonthArchive.as_view(), name="archive-month")
)
