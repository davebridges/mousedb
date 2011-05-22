"""This package defines custom views for the timed_mating application.

Currently all views are generic CRUD views except for the view in which a plug event is defined from a breeding cage."""

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import permission_required
from django.db.models import Q
from django.core.urlresolvers import reverse

from mousedb.views import ProtectedListView, ProtectedDetailView, RestrictedCreateView, RestrictedUpdateView, RestrictedDeleteView
from mousedb.animal.models import Breeding, Animal, Strain
from mousedb.timed_mating.forms import BreedingPlugForm
from mousedb.timed_mating.models import PlugEvents


class PlugEventsList(ProtectedListView):
    """This class generates an object list for PlugEvent objects.
    
    This login protected view takes all PlugEvents objects and sends them to plugevents_list.html as a plug_list dictionary.
    The url for this view is **/plugs/**"""
    model = PlugEvents
    context_object_name = 'plugevents_list'
    template_name = "plugevents_list.html"
    
class PlugEventsListStrain(PlugEventsList):
    """This class generates a strain filtered list for Plug Event objects.
    
    This is a subclass of PlugEventsList and returns as context_object_name plug_events_list to plugevents_list.html.
    It takes a named argument (strain) which is a Strain_slug and filters based on that strain."""

    def get_queryset(self):
        """The queryset is over-ridden to show only plug events in which the strain matches the breeding strain."""
        self.strain = get_object_or_404(Strain, Strain_slug__iexact=self.kwargs['slug'])
        return PlugEvents.objects.filter(Breeding__Strain=self.strain)

    
class PlugEventsDetail(ProtectedDetailView): 
    """This class generates the plugevents-detail view.
    
    This login protected takes a url in the form **/plugs/1** for plug event id=1 and passes a **plug** object to plugevents_detail.html"""
    model = PlugEvents
    template_name = 'plugevents_detail.html'
    context_object_name = 'plugevent'
    
class PlugEventsCreate(RestrictedCreateView):
    """This class generates the plugevents-new view.

    This permission restricted view takes a url in the form **/plugs/new** and generates an empty plugevents_form.html."""
    model = PlugEvents
    template_name = 'plugevents_form.html'
    
class PlugEventsUpdate(RestrictedUpdateView):
    """This class generates the plugevents-edit view.

    This permission restricted view takes a url in the form **/plugs/#/edit** and generates a plugevents_form.html with that object."""
    model = PlugEvents
    template_name = 'plugevents_form.html'
    context_object_name = 'plugevent'    

class PlugEventsDelete(RestrictedDeleteView):
    """This class generates the plugevents-delete view.

    This permission restricted view takes a url in the form **/plugs/#/delete** and passes that object to the confirm_delete.html page."""
    model = PlugEvents
    template_name = 'confirm_delete.html'
    context_object_name = 'plugevent'    
    success_url = "/mousedb/plugs/"
    
  
    
@permission_required('timed_mating.add_plugevents')
def breeding_plugevent(request, breeding_id):
    """This view defines a form for adding new plug events from a breeding cage.

    This form requires a breeding_id from a breeding set and restricts the PlugFemale and PlugMale to animals that are defined in that breeding cage."""
    breeding = get_object_or_404(Breeding, pk=breeding_id)
    if request.method == "POST":
        form = BreedingPlugForm(request.POST, request.FILES)
        if form.is_valid():
            plug = form.save(commit=False)
            plug.Breeding_id = breeding.id
            plug.save()
            form.save()
            return HttpResponseRedirect(reverse("plugevents-list"))
    else:
        form = BreedingPlugForm()
        form.fields["PlugFemale"].queryset = breeding.Females.all()
        form.fields["PlugMale"].queryset = breeding.Male.all()
    return render_to_response('breeding_plugevent_form.html', {'form':form, 'breeding':breeding},context_instance=RequestContext(request))

