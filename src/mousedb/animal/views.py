"""These views define template redirects for the animal app.

This module contains only non-generic views.  Several generic views are also used and are defined in animal/urls/."""

import datetime

from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.forms.models import inlineformset_factory
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.db.models import Count
from django.core import serializers
from django.core.urlresolvers import reverse
from django.db.models import Q

from mousedb.settings import WEAN_AGE, GENOTYPE_AGE

from mousedb.views import ProtectedListView, ProtectedDetailView, RestrictedCreateView, RestrictedUpdateView, RestrictedDeleteView

from mousedb.animal.models import Animal, Strain, Breeding
from mousedb.data.models import Measurement
from mousedb.animal.forms import MultipleAnimalForm, MultipleBreedingAnimalForm

class AnimalDetailView(ProtectedDetailView):
    """This view displays specific details about an animal.
	
    It takes a request in the form animal/(id)/, mice/(id) or mouse/(id)/ and renders the detail page for that mouse.  The request is defined for id not MouseID (or barcode) because this allows for details to be displayed for mice without barcode identification.
    Therefore care must be taken that animal/4932 is id=4932 and not barcode=4932.  The animal name is defined at the top of the page.
    This page is restricted to logged-in users.
    """
    model = Animal
    template_name = 'animal_detail.html'
    context_object_name = 'animal'
    
    
class StrainList(ProtectedListView):
    """This class generates an object list for Strain objects.
    
    This login protected view takes all Strain objects and sends them to strain_list.html as a strain_list dictionary.  It also passes a strain_list_alive and cages dictionary to show the numbers for total cages and total strains.
    The url for this view is **/strain/**"""
    model = Strain
    context_object_name = 'strain_list'
    template_name = "strain_list.html"

    def get_context_data(self, **kwargs):
        """This add in the context of strain_list_alive (which filters for all alive animals) and cages which filters for the number of current cages."""
        context = super(StrainList, self).get_context_data(**kwargs)
        context['strain_list_alive'] = Strain.objects.filter(animal__Alive=True).annotate(alive=Count('animal'))
        context['cages'] = Animal.objects.filter(Alive=True).values("Cage")        
        return context    

@login_required
def strain_detail(request, strain):
    """This view displays specific details about a strain.
	
    It takes a request in the form strain/(strain_slug)/ and renders the detail page for that strain.
    This view also passes along a dictionary of alive animals belonging to that strain.
    This page is restricted to logged-in users.
    """
    strain = get_object_or_404(Strain, Strain_slug=strain)
    breeding_cages = Breeding.objects.filter(Strain=strain).filter(Active=True)
    animal_list = Animal.objects.filter(Strain=strain, Alive=True).order_by('Background','Genotype')
    cages = animal_list.values("Cage", "Alive").filter(Alive=True).distinct()
    active = True
    return render_to_response('strain_detail.html', {
        'strain' : strain, 
        'animal_list' : animal_list, 
        'cages':cages, 
        'breeding_cages':breeding_cages,
        'active':active
        }
        ,context_instance=RequestContext(request))

@login_required
def strain_detail_all(request, strain):
    """This view displays specific details about a strain.
	
    It takes a request in the form /strain/(strain_slug)/all and renders the detail page for that strain.
    This view also passes along a dictionary of all animals belonging to that strain.
    This page is restricted to logged-in users.
    """
    strain = get_object_or_404(Strain, Strain_slug=strain)
    animal_list = Animal.objects.filter(Strain=strain).order_by('Background','Genotype')	
    cages = animal_list.values("Cage").distinct()
    breeding_cages = Breeding.objects.filter(Strain=strain)
    active = False
    return render_to_response('strain_detail.html', {
        'strain' : strain, 
        'animal_list' : animal_list, 
        'cages':cages, 
        'breeding_cages':breeding_cages,
        'active':active
        }
        ,context_instance=RequestContext(request))
	
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
	
    This view is intended to be used to add initial information about pups, including eartag, genotype, gender and birth or weaning information.
    It takes a request in the form /breeding/(breeding_id)/pups/ and returns a form specific to the breeding set defined in breeding_id.  breeding_id is the background identification number of the breeding set and does not refer to the barcode of any breeding cage.
    This view is restricted to those with the permission animal.add_animal.
    """
    breeding = get_object_or_404(Breeding, pk=breeding_id)
    PupsFormSet = inlineformset_factory(Breeding, Animal, extra=10, exclude=('Notes','Alive', 'Death', 'Cause_of_Death', 'Father', 'Mother', 'Breeding'))
    if request.method == "POST":
        formset = PupsFormSet(request.POST, instance=breeding)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect( breeding.get_absolute_url() )            
    else:
        formset = PupsFormSet(instance=breeding)
    return render_to_response("breeding_pups.html", {"formset":formset, 'breeding':breeding},context_instance=RequestContext(request))

@permission_required('animal.change_animal')
def breeding_change(request, breeding_id):
    """This view is used to generate a form by which to change pups which belong to a particular breeding set.
	
    This view typically is used to modify existing pups.  This might include marking animals as sacrificed, entering genotype or marking information or entering movement of mice to another cage.  It is used to show and modify several animals at once.
    It takes a request in the form /breeding/(breeding_id)/change/ and returns a form specific to the breeding set defined in breeding_id.  breeding_id is the background identification number of the breeding set and does not refer to the barcode of any breeding cage.
    This view returns a formset in which one row represents one animal.  To add extra animals to a breeding set use /breeding/(breeding_id)/pups/.
    This view is restricted to those with the permission animal.change_animal.
    """
    breeding = Breeding.objects.select_related().get(id=breeding_id)
    strain = breeding.Strain
    PupsFormSet = inlineformset_factory(Breeding, Animal, extra=0, exclude=('Alive','Father', 'Mother', 'Breeding', 'Notes'))
    if request.method =="POST":
        formset = PupsFormSet(request.POST, instance=breeding)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect( breeding.get_absolute_url() )
    else:
        formset = PupsFormSet(instance=breeding,)
    return render_to_response("breeding_change.html", {"formset":formset, 'breeding':breeding},context_instance=RequestContext(request))
	
@permission_required('animal.change_animal')
def breeding_wean(request, breeding_id):
    """This view is used to generate a form by which to wean pups which belong to a particular breeding set.
	
    This view typically is used to wean existing pups.  This includes the MouseID, Cage, Markings, Gender and Wean Date fields.  For other fields use the breeding-change page.
    It takes a request in the form /breeding/(breeding_id)/wean/ and returns a form specific to the breeding set defined in breeding_id.  breeding_id is the background identification number of the breeding set and does not refer to the barcode of any breeding cage.
    This view returns a formset in which one row represents one animal.  To add extra animals to a breeding set use /breeding/(breeding_id)/pups/.
    This view is restricted to those with the permission animal.change_animal.
    """
    breeding = Breeding.objects.get(id=breeding_id)
    strain = breeding.Strain
    PupsFormSet = inlineformset_factory(Breeding, Animal, extra=0, exclude=('Alive','Father', 'Mother', 'Breeding', 'Notes','Rack','Rack_Position','Strain','Background','Genotype','Death','Cause_of_Death','Backcross','Generation'))
    if request.method =="POST":
        formset = PupsFormSet(request.POST, instance=breeding)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect( breeding.get_absolute_url() )
    else:
        formset = PupsFormSet(instance=breeding,)
    return render_to_response("breeding_change.html", {"formset":formset, 'breeding':breeding},context_instance=RequestContext(request))	

def multiple_pups(request):
    """This view is used to enter multiple animals at the same time.
	
    It will generate a form containing animal information and a number of mice.  It is intended to create several identical animals with the same attributes.
    """
    if request.method == "POST":
        form = MultipleAnimalForm(request.POST)
        if form.is_valid():
            count = form.cleaned_data['count']
            for i in range(count):
                animal = Animal(
				    Strain = form.cleaned_data['Strain'], 
					Background = form.cleaned_data['Background'],
					Breeding = form.cleaned_data['Breeding'],
					Cage = form.cleaned_data['Cage'],
                    Rack = form.cleaned_data['Rack'],
                    Rack_Position = form.cleaned_data['Rack_Position'],
                    Genotype = form.cleaned_data['Genotype'],
                    Gender = form.cleaned_data['Gender'],
                    Born = form.cleaned_data['Born'],
                    Weaned = form.cleaned_data['Weaned'],
                    Backcross = form.cleaned_data['Backcross'],
                    Generation = form.cleaned_data['Generation'],
                    Father = form.cleaned_data['Father'],
                    Mother = form.cleaned_data['Mother'],
                    Markings = form.cleaned_data['Markings'],					
                    Notes = form.cleaned_data['Notes'])
                animal.save()
        return HttpResponseRedirect( reverse('strain-list') )	
    else:
        form = MultipleAnimalForm()
    return render_to_response("animal_multiple_form.html", {"form":form,}, context_instance=RequestContext(request))		
	
def multiple_breeding_pups(request, breeding_id):
    """This view is used to enter multiple animals at the same time from a breeding cage.
	
    It will generate a form containing animal information and a number of mice.  It is intended to create several identical animals with the same attributes.
	This view requres an input of a breeding_id to generate the correct form.
    """
    breeding = Breeding.objects.get(id=breeding_id)
    if request.method == "POST":
        form = MultipleBreedingAnimalForm(request.POST)
        if form.is_valid():
            count = form.cleaned_data['count']
            for i in range(count):
                animal = Animal(
				    Strain = breeding.Strain, 
					Background = breeding.background,
					Breeding = breeding,
					Cage = breeding.Cage,
                    Rack = breeding.Rack,
                    Rack_Position = breeding.Rack_Position,
                    Genotype = breeding.genotype,
                    Gender = form.cleaned_data['Gender'],
                    Born = form.cleaned_data['Born'],
                    Weaned = form.cleaned_data['Weaned'],
                    Backcross = breeding.backcross,
                    Generation = breeding.generation)
                animal.save()	
        return HttpResponseRedirect( breeding.get_absolute_url() )	
    else:
        form = MultipleBreedingAnimalForm()
    return render_to_response("animal_multiple_form.html", {"form":form, "breeding":breeding}, context_instance=RequestContext(request))	

def date_archive_year(request):
    """This view will generate a table of the number of mice born on an annual basis.
    
    This view is associated with the url name archive-home, and returns an dictionary of a date and a animal count."""
    oldest_animal = Animal.objects.filter(Born__isnull=False).order_by('Born')[0]
    archive_dict = {}
    tested_year = oldest_animal.Born.year
    while tested_year <= datetime.date.today().year:
        archive_dict[tested_year] = Animal.objects.filter(Born__year=tested_year).count()
        tested_year = tested_year + 1
    return render_to_response("animal_archive.html", {"archive_dict": archive_dict}, context_instance=RequestContext(request))

@login_required
def todo(request):
    """This view generates a summary of the todo lists.
    
    The login restricted view passes lists for ear tagging, genotyping and weaning and passes them to the template todo.html"""
    eartag_list = Animal.objects.filter(Born__lt=(datetime.date.today() - datetime.timedelta(days=WEAN_AGE))).filter(MouseID__isnull=True, Alive=True)
    genotype_list = Animal.objects.filter(Q(Genotype='N.D.')|Q(Genotype__icontains='?')).filter(Alive=True, Born__lt=(datetime.date.today() - datetime.timedelta(days=GENOTYPE_AGE)))
    wean = datetime.date.today() - datetime.timedelta(days=WEAN_AGE)
    wean_list = Animal.objects.filter(Born__lt=wean).filter(Weaned=None,Alive=True).exclude(Strain=2).order_by('Strain','Background','Rack','Cage')
    return render_to_response('todo.html', {'eartag_list':eartag_list, 'wean_list':wean_list, 'genotype_list':genotype_list},context_instance=RequestContext(request))    



