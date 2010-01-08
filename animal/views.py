"""These views define template redirects for the animal app.

This module contains only non-generic views.  Several generic views are also used and are defined in animal/urls/."""

from mousedb.animal.models import Animal, Strain, Breeding, Cage
from mousedb.data.models import Measurement
from mousedb.animal.forms import AnimalChangeForm, AnimalForm
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.forms.models import inlineformset_factory
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.db.models import Count


@login_required
def animal_detail(request, id):
    """This view displays specific details about an animal.
	
    It takes a request in the form animal/(id)/, mice/(id) or mouse/(id)/ and renders the detail page for that mouse.  The request is defined for id not MouseID (or barcode) because this allows for details to be displayed for mice without barcode identification.
    Therefore care must be taken that animal/4932 is id=4932 and not barcode=4932.  The animal name is defined at the top of the page.
    This page is restricted to logged-in users.
    """
    animal = Animal.objects.get(pk=id)
    animal_measurements=Measurement.objects.filter(animal__id=id).order_by('assay','experiment')
    return render_to_response('animal_detail.html', {'animal' : animal, 'animal_measurements':animal_measurements},context_instance=RequestContext(request))

@login_required
def strain_list(request):
    """This view presents a list of strains currently present in the database and annotates this list with a count of alive and total animals.
	
    This view redirects from a /strain/ request.
    This view is restricted to logged-in users.
    """
    strain_list = Strain.objects.all()
    strain_list_alive = Strain.objects.filter(animal__Alive=True).annotate(alive=Count('animal'))
    return render_to_response('strain_list.html', {'strain_list': strain_list, 'strain_list_alive':strain_list_alive },context_instance=RequestContext(request))

@login_required
def strain_detail(request, strain):
    """This view displays specific details about a strain.
	
    It takes a request in the form strain/(strain_slug)/ and renders the detail page for that strain.
    This view also passes along a dictionary of alive animals belonging to that strain.
    This page is restricted to logged-in users.
    """
    strain = Strain.objects.get(Strain_slug=strain)
    animal_list = Animal.objects.filter(Strain=strain, Alive=True).order_by('Background','Genotype')	
    return render_to_response('strain_detail.html', {'strain' : strain, 'animal_list' : animal_list},context_instance=RequestContext(request))

@login_required
def strain_detail_all(request, strain):
    """This view displays specific details about a strain.
	
    It takes a request in the form /strain/(strain_slug)/all and renders the detail page for that strain.
    This view also passes along a dictionary of all animals belonging to that strain.
    This page is restricted to logged-in users.
    """
    strain = Strain.objects.get(Strain_slug=strain)
    animal_list = Animal.objects.filter(Strain=strain).order_by('Background','Genotype')	
    return render_to_response('strain_detail.html', {'strain' : strain, 'animal_list' : animal_list},context_instance=RequestContext(request))

@login_required
def breeding(request):
    """This view displays a list of breeding sets.
	
    It takes a request in the form /breeding/ and lists all currently active breeding sets.
    This page is restricted to logged-in users.
    """
    breeding_list = Breeding.objects.filter(Active=True).order_by('Strain','-Start')
    return render_to_response('breeding.html', {'breeding_list': breeding_list},context_instance=RequestContext(request))

@login_required
def breeding_all(request):
    """This view displays a list of breeding sets.
	
    It takes a request in the form /breeding/all and lists all breeding sets (both active and inactive).
    This page is restricted to logged-in users.
    """
    breeding_list = Breeding.objects.order_by('Strain','-Start')
    return render_to_response('breeding.html', {'breeding_list': breeding_list},context_instance=RequestContext(request))

@login_required
def breeding_detail(request, breeding_id):
    """This view displays specific details about a breeding set.

    It takes a request in the form /breeding/(breeding_id)/all and renders the detail page for that breeding set.
    The breeding_id refers to the background id of the breeding set, and not the breeding cage barcode.
    This view also passes along a dictionary of all pups belonging to that breeding set.
    This page is restricted to logged-in users.
    """
    breeding = Breeding.objects.select_related().get(id=breeding_id)
    pups = Animal.objects.filter(Breeding=breeding)
    return render_to_response('breeding_detail.html', {'breeding': breeding, 'pups' : pups},context_instance=RequestContext(request))

@permission_required('animal.add_animal')
def breeding_pups(request, breeding_id):
    """This view is used to generate a form by which to add pups which belong to a particular breeding set.
	
    It takes a request in the form /breeding/(breeding_id)/pups/ and returns a form specific to the breeding set defined in breeding_id.  breeding_id is the background identification number of the breeding set and does not refer to the barcode of any breeding cage.
    This view is restricted to those with the permission animal.add_animal.
    """
    breeding = get_object_or_404(Breeding, pk=breeding_id)
    PupsFormSet = inlineformset_factory(Breeding, Animal)
    if request.method == "POST":
        formset = PupsFormSet(request.POST, instance=breeding)
        if formset.is_valid():
            formset.save
            return HttpResponseRedirect( breeding.get_absolute_url() )            
    else:
        formset = PupsFormSet(instance=breeding)
    return render_to_response("breeding_pups.html", {"formset":formset, 'breeding':breeding},context_instance=RequestContext(request))




@permission_required('animal.change_animal')
def breeding_change(request, breeding_id):
    """This view is used to generate a form by which to change pups which belong to a particular breeding set.
	
    It takes a request in the form /breeding/(breeding_id)/change/ and returns a form specific to the breeding set defined in breeding_id.  breeding_id is the background identification number of the breeding set and does not refer to the barcode of any breeding cage.
    This view returns a formset in which one row represents one animal.  To add extra animals to a breeding set use /breeding/(breeding_id)/pups/.
    This view is restricted to those with the permission animal.change_animal.
    """
    breeding = Breeding.objects.select_related().get(id=breeding_id)
    strain = breeding.Strain
    PupsFormSet = inlineformset_factory(Breeding, Animal, extra=0, fields=['MouseID', 'Gender','Cage', 'Genotype', 'Death','Cause_of_Death','Born','Rack', 'Rack_Position','Markings'])
    if request.method =="POST":
        formset = PupsFormSet(request.POST, instance=breeding)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect("/mousedb/breeding/")
    else:
        formset = PupsFormSet(instance=breeding,)
    return render_to_response("breeding_change.html", {"formset":formset, 'breeding':breeding},context_instance=RequestContext(request))

@permission_required('animal.change_animal')
def animal_change(request, animal_id):
    """This view is used to render a form to modify one animal.
	
    The request takes the form /mouse/(id)/change/ or insetad of mouse mice, animal or animals.  This returns a form specific to the animal defined in id.  id represents the background identification number of a mouse and not the eartag or other identification number for an animal.
    This view is restricted to users with the permission animal.change_animal."""
    animal = Animal.objects.get(id=animal_id)
    if request.method == "POST":
        form = AnimalChangeForm(request.POST, instance=animal)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/mousedb/mouse")
    else:
        form = AnimalChangeForm(instance=animal)
    return render_to_response("animal_form.html", {"form":form, 'animal':animal},context_instance=RequestContext(request))

@permission_required('animal.add_animal')
def animal_new(request):
    """This view is used to generate a form to add one animal.

    It takes a request of /mouse/new/ or insetad of mouse mice, animal or animals and returns a blank form.
    If you are adding an animal as part of a breeding set it is best to use /breeding/(breeding_id)/pups."""
    if request.method =="POST":
        form=AnimalForm(request.POST)
        if form.is_valid():
            animal = form.save(commit=False)
            cage = Cage(Barcode=animal.CageID, Rack=animal.Rack, Rack_Position=animal.Rack_Position)
            cage.save()
            animal.save()
            form.save()
        return HttpResponseRedirect("/mousedb/mouse")
    else:
        form = AnimalForm()
    return render_to_response("animal_form.html",{"form":form,},context_instance=RequestContext(request))
