"""These views define template redirects for the animal app.

This module contains all views for this app as class based views."""

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
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, DeleteView, YearArchiveView, MonthArchiveView

from mousedb.settings import WEAN_AGE, GENOTYPE_AGE

from mousedb.views import ProtectedListView, ProtectedDetailView


from mousedb.animal.models import Animal, Strain, Breeding
from mousedb.data.models import Measurement
from mousedb.animal.forms import MultipleAnimalForm, MultipleBreedingAnimalForm, BreedingForm, AnimalForm

class AnimalList(ProtectedListView):
    """This view generates a list of animals as animal-list
    
    This view responds to a url in the form */animal*
    It sends a variable animal containing all animals to animal_list.html.
    This view is login protected."""
    
    model = Animal
    template_name = 'animal_list.html'
    context_object_name = 'animal_list'

class AnimalListAlive(AnimalList):
    """This view generates a list of alive animals or animal-list-alive.
    
    The main use for this view is to take a url in the form */animal/all* and to return a list of all alive animals to animal_list.html in the context animal.  It also adds an extra context variable, "list type" as Alive.  
    This view is login protected."""
    
    queryset = Animal.objects.filter(Alive=True)
        
    def get_context_data(self, **kwargs):
        """This add in the context of list_type and returns this as Alive."""
        
        context = super(AnimalListAlive, self).get_context_data(**kwargs)
        context['list_type'] = 'Alive'
        return context         

class AnimalDetail(ProtectedDetailView):
    """This view displays specific details about an animal as the animal-detail.
	
    It takes a request in the form *animal/(id)*, *mice/(id)* or *mouse/(id)* and renders the detail page for that mouse.  The request is defined for id not MouseID (or barcode) because this allows for details to be displayed for mice without barcode identification.
    Therefore care must be taken that animal/4932 is id=4932 and not barcode=4932.  The animal name is defined at the top of the page.
    This page is restricted to logged-in users.
    """
    
    model = Animal
    template_name = 'animal_detail.html'
    context_object_name = 'animal'
    
class AnimalCreate(CreateView):
    """This class generates the animal-new view.

    This permission restricted view takes a url in the form */animal/new* and generates an empty animal_form.html.
    This view is restricted to those with the animal.create_animal permission.    """
    
    model = Animal
    form_class = AnimalForm
    template_name = 'animal_form.html'
    
    @method_decorator(permission_required('animal.add_animal'))
    def dispatch(self, *args, **kwargs):
        """This decorator sets this view to have restricted permissions."""
        return super(AnimalCreate, self).dispatch(*args, **kwargs)   
    
class AnimalUpdate(UpdateView):
    """This class generates the animal-edit view.

    This permission restricted view takes a url in the form */animal/#/edit* and generates a animal_form.html with that object.
    This view is restricted to those with the animal.update_animal permission."""
    
    model = Animal
    form_class = AnimalForm    
    template_name = 'animal_form.html'
    context_object_name = 'animal'    
    
    @method_decorator(permission_required('animal.change_animal'))
    def dispatch(self, *args, **kwargs):
        """This decorator sets this view to have restricted permissions."""
        return super(AnimalUpdate, self).dispatch(*args, **kwargs)  

class AnimalDelete(DeleteView):
    """This class generates the animal-delete view.

    This permission restricted view takes a url in the form */animal/#/delete* and passes that object to the confirm_delete.html page.
    This view is restricted to those with the animal.delete_animal permission."""
    
    model = Animal
    template_name = 'confirm_delete.html'
    context_object_name = 'animal'    
    success_url = '/animal/'     

    @method_decorator(permission_required('animal.delete_animal'))
    def dispatch(self, *args, **kwargs):
        """This decorator sets this view to have restricted permissions."""
        return super(AnimalDelete, self).dispatch(*args, **kwargs)    
    
    
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

class StrainDetail(ProtectedDetailView):
    """This view displays specific details about a strain showing *only current* related objects.
	
    It takes a request in the form *strain/(strain_slug)/* and renders the detail page for that strain.
    This view also passes along a dictionary of alive animals belonging to that strain.
    This page is restricted to logged-in users.
    """
    
    queryset = Strain.objects.all()
    slug_field = 'Strain_slug'
    context_object_name = 'strain' 
    template_name = "strain_detail.html"    
    
    def get_context_data(self, **kwargs):
        """This add in the context of strain_list_alive (which filters for only alive animals and active) and cages which filters for the number of current cages."""
        
        strain = super(StrainDetail, self).get_object()
        context = super(StrainDetail, self).get_context_data(**kwargs)
        context['breeding_cages'] = Breeding.objects.filter(Strain=strain).filter(Active=True)
        context['animal_list'] = Animal.objects.filter(Strain=strain, Alive=True).order_by('Background','Genotype')
        context['cages'] = Animal.objects.filter(Strain=strain, Alive=True).values("Cage", "Alive").filter(Alive=True).distinct()
        context['active'] = True        
        return context  
    
class StrainDetailAll(StrainDetail):
    """This view displays specific details about a strain showing *all* related objects.
	
    This view subclasses StrainDetail and modifies the get_context_data to show associated active objects.
    It takes a request in the form *strain/(strain_slug)/all* and renders the detail page for that strain.
    This view also passes along a dictionary of alive animals belonging to that strain.
    This page is restricted to logged-in users.
    """

    def get_context_data(self, **kwargs):
        """This adds into the context of strain_list_all (which filters for all alive animals and active cages) and cages which filters for the number of current cages."""
        
        strain = super(StrainDetail, self).get_object()
        context = super(StrainDetail, self).get_context_data(**kwargs)
        context['breeding_cages'] = Breeding.objects.filter(Strain=strain)
        context['animal_list'] = Animal.objects.filter(Strain=strain).order_by('Background','Genotype')
        context['cages'] = Animal.objects.filter(Strain=strain).values("Cage").distinct()
        context['active'] = False        
        return context      
 
class StrainCreate(CreateView):
    """This class generates the strain-new view.

    This permission restricted view takes a url in the form */strain/new* and generates an empty strain_form.html.
    This view is restricted to those with the animal.create_strain permission.    """
    
    model = Strain
    template_name = 'strain_form.html'
    
    @method_decorator(permission_required('animal.create_strain'))
    def dispatch(self, *args, **kwargs):
        """This decorator sets this view to have restricted permissions."""
        return super(StrainCreate, self).dispatch(*args, **kwargs)   
    
class StrainUpdate(UpdateView):
    """This class generates the strain-edit view.

    This permission restricted view takes a url in the form */strain/#/edit* and generates a strain_form.html with that object.
    This view is restricted to those with the animal.update_strain permission."""
    
    model = Strain
    template_name = 'strain_form.html'
    context_object_name = 'strain'    
    
    @method_decorator(permission_required('animal.update_strain'))
    def dispatch(self, *args, **kwargs):
        """This decorator sets this view to have restricted permissions."""
        return super(StrainUpdate, self).dispatch(*args, **kwargs)  

class StrainDelete(DeleteView):
    """This class generates the strain-delete view.

    This permission restricted view takes a url in the form */strain/#/delete* and passes that object to the confirm_delete.html page.
    This view is restricted to those with the animal.delete_strain permission."""
    
    model = Strain
    template_name = 'confirm_delete.html'
    context_object_name = 'strain'    
    success_url = '/strain/'     

    @method_decorator(permission_required('animal.delete_strain'))
    def dispatch(self, *args, **kwargs):
        """This decorator sets this view to have restricted permissions."""
        return super(StrainDelete, self).dispatch(*args, **kwargs)  

class BreedingDetail(ProtectedDetailView):
    """This view displays specific details about a breeding set.

    It takes a request in the form */breeding/(breeding_id)* and renders the detail page for that breeding set.
    The breeding_id refers to the background id of the breeding set, and not the breeding cage barcode.
    This page is restricted to logged-in users.
    """
    
    model = Breeding
    context_object_name = 'breeding' 
    template_name = "breeding_detail.html"  
    
class BreedingList(ProtectedListView):
    """This class generates an object list for active Breeding objects.
    
    This login protected view takes all Breeding objects and sends them to strain_list.html as a strain_list dictionary.  It also passes a strain_list_alive and cages dictionary to show the numbers for total cages and total strains.
    The url for this view is */strain/*"""
    
    queryset = Breeding.objects.filter(Active=True)
    context_object_name = 'breeding_list'
    template_name = "breeding_list.html"

    def get_context_data(self, **kwargs):
        """This adds into the context of breeding_type and sets it to Active."""
        
        context = super(BreedingList, self).get_context_data(**kwargs)
        context['breeding_type'] = "Active" 
        return context    

class BreedingListAll(BreedingList):
    """This class generates a view for all breeding objects.
    
    This class is a subclass of BreedingList, changing the queryset and the  breeding_type context."""

    queryset = Breeding.objects.all()

    def get_context_data(self, **kwargs):
        """This add in the context of breeding_type and sets it to All."""
        
        context = super(BreedingList, self).get_context_data(**kwargs)
        context['breeding_type'] = "All" 
        return context
        
class BreedingListTimedMating(BreedingList):
    """This class generates a view for breeding objects, showing only timed mating cages.
    
    This class is a subclass of BreedingList, changing the queryset and the  breeding_type context."""

    queryset = Breeding.objects.filter(Timed_Mating=True)

    def get_context_data(self, **kwargs):
        """This add in the context of breeding_type and sets it to Timed_Matings."""
        
        context = super(BreedingList, self).get_context_data(**kwargs)
        context['breeding_type'] = "Timed Matings" 
        return context     

class BreedingCreate(CreateView):
    """This class generates the breeding-new view.

    This permission restricted view takes a url in the form */breeding/new* and generates an empty plugevents_form.html."""
    
    model = Breeding
    form_class = BreedingForm
    template_name = 'breeding_form.html'
    
    @method_decorator(permission_required('animal.add_breeding'))
    def dispatch(self, *args, **kwargs):
        """This decorator sets this view to have restricted permissions."""
        return super(BreedingCreate, self).dispatch(*args, **kwargs)      
    
class BreedingUpdate(UpdateView):
    """This class generates the breeding-edit view.

    This permission restricted view takes a url in the form */breeding/#/edit* and generates a breeding_form.html with that object."""
    
    model = Breeding
    form_class = BreedingForm    
    template_name = 'breeding_form.html'
    context_object_name = 'breeding'    
    
    @method_decorator(permission_required('animal.change_breeding'))
    def dispatch(self, *args, **kwargs):
        """This decorator sets this view to have restricted permissions."""
        return super(BreedingUpdate, self).dispatch(*args, **kwargs)      

class BreedingDelete(DeleteView):
    """This class generates the breeding-delete view.

    This permission restricted view takes a url in the form */breeding/#/delete* and passes that object to the confirm_delete.html page."""
    
    model = Breeding
    template_name = 'confirm_delete.html'
    context_object_name = 'breeding'    
    success_url = '/breeding/'     
    
    @method_decorator(permission_required('animal.delete_breeding'))
    def dispatch(self, *args, **kwargs):
        """This decorator sets this view to have restricted permissions."""
        return super(BreedingDelete, self).dispatch(*args, **kwargs)      
        
        
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
    return render_to_response("breeding_wean.html", {"formset":formset, 'breeding':breeding},context_instance=RequestContext(request))	

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
    
class AnimalYearArchive(YearArchiveView):
    """This view generates a list of animals born within the specified year.
    
    It takes a url in the form of **/date/####** where #### is the four digit code of the year.
    This view is restricted to logged in users."""
    
    model = Animal
    template_name = 'animal_list.html'
    context_object_name = 'animal_list'  
    date_field = 'Born'
    make_object_list = True

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        """This decorator sets this view to have restricted permissions."""
        return super(AnimalYearArchive, self).dispatch(*args, **kwargs)    

class AnimalMonthArchive(MonthArchiveView):
    """This view generates a list of animals born within the specified year.
    
    It takes a url in the form of **/date/####** where #### is the four digit code of the year.
    This view is restricted to logged in users."""
    
    model = Animal
    template_name = 'animal_list.html'
    context_object_name = 'animal_list'  
    date_field = 'Born'
    make_object_list = True
    month_format = '%m'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        """This decorator sets this view to have restricted permissions."""
        return super(AnimalMonthArchive, self).dispatch(*args, **kwargs)          
    
    

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



