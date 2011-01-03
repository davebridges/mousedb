from django.conf.urls.defaults import *

from django.views.generic.list_detail import object_list
from django.contrib.auth.decorators import login_required

from mousedb.animal.models import Animal

@login_required
def limited_object_list(*args, **kwargs):
	return object_list(*args, **kwargs)
	
@login_required
def limited_object_detail(*args, **kwargs):
	return object_detail(*args, **kwargs)

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
	url(r'^/?$', limited_object_list, {
		'queryset': Animal.objects.values('Cage', 'Strain__Strain', 'Strain__Strain_slug', 'Rack', 'Rack_Position', 'Alive').filter(Alive=True).order_by('Cage').distinct().filter(Alive='True'),
		'template_name': 'cage_list.html',
		'template_object_name': 'cage',
		}, name="cage-list"),
	url(r'^all/?$', limited_object_list, {
		'queryset': Animal.objects.values("Cage", "Strain__Strain","Strain__Strain_slug", "Rack", "Rack_Position", "Alive").order_by('Cage').distinct(),
		'template_name': 'cage_list.html',
		'template_object_name': 'cage',
		'extra_context': {'all_cages':True}
		}, name="cage-list-all"),
	url(r'^(?P<object_id>\d*)/$', limited_object_detail, {
		'queryset': Animal.objects.filter(), #need to fix this to filter for a cage number
		'template_name': 'animal_list.html',
		'template_object_name': 'animal',
		}, name="cage-detail"),		
		)