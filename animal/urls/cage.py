from django.conf.urls.defaults import *

from django.views.generic.list_detail import object_list
from django.contrib.auth.decorators import login_required

from mousedb.animal.models import Animal

@login_required
def limited_object_list(*args, **kwargs):
	return object_list(*args, **kwargs)

def animals_by_cage(request, cage_number):
	"""Wrapper function to filter animals by cage number."""
	return limited_object_list(
		request,
		queryset = Animal.objects.filter(Cage=cage_number),
		template_name = 'animal_list.html', 
		template_object_name = 'animal'
	)
		
urlpatterns = patterns('',
	url(r'^(?P<cage_number>\d*)/$', animals_by_cage, name="animals-list-by-cage"),
		)