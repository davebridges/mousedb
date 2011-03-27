"""This package defines custom views for the timed_mating application.

Currently all views are generic CRUD views except for the view in which a plug event is defined from a breeding cage."""

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import permission_required
from django.db.models import Q

from mousedb.views import ProtectedListView, ProtectedDetailView
from mousedb.animal.models import Breeding, Animal, Strain
from mousedb.timed_mating.forms import BreedingPlugForm
from mousedb.timed_mating.models import PlugEvents


class PlugEventsListView(ProtectedListView):
    """This class generates an object list for PlugEvent objects.
    
    This login protected view takes all PlugEvents objects and sends them to plugevents_list.html as a plug_list dictionary.
    The url for this view is **/plugs/**"""
    model = PlugEvents
    context_object_name = 'plug_list'
    template_name = "plugevents_list.html"
    
class StrainPlugEventsListView(ProtectedListView):
    """This class generates an object list for PlugEvent objects.
    
    This login protected view takes PlugEvents belonging to a particular strain_slug and sends them to plugevents_list.html as a plug_list dictionary.  The url for this view is **/plugs/strain/strain-slug**.  This view is not yet working."""
    model = PlugEvents
    context_object_name = 'plug_list'
    template_name = "plugevents_list.html" 

    def get_queryset(self):
        """This function defines the queryset for the StrainPlugEventsListView.
        
        The function takes an argument, which is typically a Strain_slug and filters the PlugEvents by that strain."""
        strain = get_object_or_404(Strain, Strain_slug__iexact=self.args[0])
        return PlugEvents.objects.filter(PlugFemale__strain=strain)
        
class PlugEventsDetailView(ProtectedDetailView): 
    """This class generates the plugevents-detail view.
    
    This login protected takes a url in the form **/plugs/1** for plug event id=1 and passes a plug object to plugevents_detail.html"""
    model = PlugEvents
    template_name = 'plugevents_detail.html'
    context_object_name = 'plug'
       
    
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

