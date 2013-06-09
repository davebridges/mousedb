"""Url redirections for :class:`~mousedb.data.models.Cohort` objects.

This includes generic create, update, delete, list and detail views.
The views for these urls are defined in the :mod:`~mousedb.data.views.` module.
"""

from django.conf.urls import *

from mousedb.data.views import CohortDetail, CohortList, CohortUpdate, CohortDelete, CohortCreate

urlpatterns = patterns('',
	url(r'^/?$', CohortList.as_view(), name="cohort-list"),	
	url(r'^new/?$', CohortCreate.as_view(), name="cohort-new"),	
	url(r'^(?P<slug>[-\w\d]+)/edit/?$', CohortUpdate.as_view(), name="cohort-edit"),
	url(r'^(?P<slug>[-\w\d]+)/delete/?$', CohortDelete.as_view(), name="cohort-delete"),
	url(r'^(?P<slug>[-\w\d]+)/?$', CohortDetail.as_view(), name="cohort-detail"),		
)
