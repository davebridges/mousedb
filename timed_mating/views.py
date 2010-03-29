from django.shortcuts import render_to_response
from django.contrib.auth.decorators import permission_required
from django.template import RequestContext
from django.http import HttpResponseRedirect

from animal.models import Breeding, Animal
from timed_mating.forms import BreedingPlugForm

@permission_required('timed_mating.add_plugevents')
def breeding_plugevent(request, breeding_id):
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

