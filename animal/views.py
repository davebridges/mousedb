from mousedb.animal.models import Animal, Strain, Breeding, Cage
from mousedb.data.models import Measurement
from mousedb.animal.forms import AnimalChangeForm, AnimalForm
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.forms.models import inlineformset_factory
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.db.models import Count


@login_required
def animal_detail(request, id):
	animal = Animal.objects.get(pk=id)
	animal_measurements=Measurement.objects.filter(animal__id=id).order_by('assay','experiment')
	return render_to_response('animal_detail.html', {'animal' : animal, 'animal_measurements':animal_measurements},context_instance=RequestContext(request))

@login_required
def strain_list(request):
	strain_list = Strain.objects.all()
	strain_list_alive = Strain.objects.filter(animal__Alive=True).annotate(alive=Count('animal'))
	return render_to_response('strain_list.html', {'strain_list': strain_list, 'strain_list_alive':strain_list_alive },context_instance=RequestContext(request))

@login_required
def strain_detail(request, strain):
	strain = Strain.objects.get(Strain_slug=strain)
	animal_list = Animal.objects.filter(Strain=strain, Alive=True).order_by('Background','Genotype')	
	return render_to_response('strain_detail.html', {'strain' : strain, 'animal_list' : animal_list},context_instance=RequestContext(request))

@login_required
def strain_detail_all(request, strain):
	strain = Strain.objects.get(Strain_slug=strain)
	animal_list = Animal.objects.filter(Strain=strain).order_by('Background','Genotype')	
	return render_to_response('strain_detail.html', {'strain' : strain, 'animal_list' : animal_list},context_instance=RequestContext(request))

@login_required
def breeding(request):
	breeding_list = Breeding.objects.filter(Active=True).order_by('Strain','-Start')
	return render_to_response('breeding.html', {'breeding_list': breeding_list},context_instance=RequestContext(request))

@login_required
def breeding_all(request):
	breeding_list = Breeding.objects.order_by('Strain','-Start')
	return render_to_response('breeding.html', {'breeding_list': breeding_list},context_instance=RequestContext(request))

@login_required
def breeding_detail(request, breeding_id):
	breeding = Breeding.objects.select_related().get(id=breeding_id)
	pups = Animal.objects.filter(Breeding=breeding)
	return render_to_response('breeding_detail.html', {'breeding': breeding, 'pups' : pups},context_instance=RequestContext(request))

@login_required
def breeding_pups(request, breeding_id):
	breeding = Breeding.objects.select_related().get(id=breeding_id)
	strain = breeding.Strain
	PupsFormSet = inlineformset_factory(Breeding, Animal, extra=10, fields=['Born','Background','Gender','Strain','Cage','Backcross','Generation', 'Weaned', 'Rack', 'Rack_Position', 'MouseID', 'Genotype'])
	if request.method =="POST":
		formset = PupsFormSet(request.POST, instance=breeding)
		if formset.is_valid():
			formset.save()
			return HttpResponseRedirect("/mousedb/breeding/")
	else:
		formset = PupsFormSet(instance=breeding,)
	return render_to_response("breeding_pups.html", {"formset":formset, 'breeding':breeding},context_instance=RequestContext(request))

@login_required
def breeding_change(request, breeding_id):
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

@login_required
def animal_change(request, animal_id):
	animal = Animal.objects.get(id=animal_id)
	if request.method == "POST":
		form = AnimalChangeForm(request.POST, instance=animal)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect("/mousedb/mouse")
	else:
		form = AnimalChangeForm(instance=animal)
	return render_to_response("animal_change.html", {"form":form, 'animal':animal},context_instance=RequestContext(request))

@login_required
def animal_new(request):
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
	return render_to_response("animal_new.html",{"form":form,},context_instance=RequestContext(request))
