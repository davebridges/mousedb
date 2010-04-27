"""This package defines custom views for the timed_mating application.

Currently all views are generic CRUD views except for the view in which a plug event is defined from a breeding cage."""

from django.shortcuts import render_to_response
from django.contrib.auth.decorators import permission_required
from django.template import RequestContext
from django.http import HttpResponseRedirect

from mousedb.animal.models import Breeding, Animal
from mousedb.timed_mating.forms import BreedingPlugForm

@permission_required('timed_mating.add_plugevents')
def breeding_plugevent(request, breeding_id):
	"""This view defines a form for adding new plug events from a breeding cage.

        This form requires a breeding_id from a breeding set and restricts the PlugFemale and PlugMale to animals that are defined in that breeding cage."""
	breeding = Breeding.objects.select_related().get(id=breeding_id)
        if request.method == "POST":
		form = BreedingPlugForm(request.POST, request.FILES)
                if form.is_valid():
                        plug = form.save(commit=False)
                        plug.Breeding_id = breeding.id
                        plug.save()
                        form.save()
                        return HttpResponseRedirect("/mousedb/plug/")
        else:
                form = BreedingPlugForm()
		form.fields["PlugFemale"].queryset = breeding.Females.all()
		form.fields["PlugMale"].queryset = breeding.Male.all()
        return render_to_response('breedingplug_form.html', {'form':form, 'breeding':breeding},context_instance=RequestContext(request))

