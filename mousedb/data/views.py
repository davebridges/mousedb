import csv

from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy

from braces.views import LoginRequiredMixin, PermissionRequiredMixin

from mousedb.animal.models import Animal
from mousedb.data.models import Experiment, Measurement, Study, Treatment, Pharmaceutical, Cohort
from mousedb.data.forms import MeasurementForm, MeasurementFormSet, StudyExperimentForm

class CohortDetail(LoginRequiredMixin,DetailView):
    '''This view generates details about a :class:`~mousedb.data.models.Cohort` object.
    
    This view is restricted to logged in users.
    It passes an object **cohort** when the url **/cohort/<slug>** is requested.'''
    
    model = Cohort
    template_name = 'cohort_detail.html'
    context_object_name = 'cohort'
    
class CohortList(LoginRequiredMixin,ListView):
    '''This view generates list of :class:`~mousedb.data.models.Cohort` objects.
    
    This view is restricted to logged in users.
    It passes an object **cohort_list** when the url **/cohort** is requested.'''
    
    model = Cohort
    template_name = 'cohort_list.html'
    context_object_name = 'cohort_list'
    
class CohortCreate(PermissionRequiredMixin,CreateView):
    '''This view generates a form for creating a :class:`~mousedb.data.models.Cohort` object.
    
    This view is restricted to logged in users with the create-cohort permission.
    It is generated when the url **/cohort/new** is requested.'''
    
    model = Cohort
    permission_required = "data.add_cohort"    
    template_name = 'cohort_form.html'
    context_object_name = 'cohort'
    
class CohortUpdate(PermissionRequiredMixin,UpdateView):
    '''This view generates a form for updating :class:`~mousedb.data.models.Cohort` objects.
    
    This view is restricted to logged in users with the update-cohort permision. 
    It passes an object **object** when the url **/cohort/<slug>/edit** is requested.'''
    
    model = Cohort
    permission_required = "data.update_cohort"    
    template_name = 'cohort_form.html'
    context_object_name = 'cohort'        

class CohortDelete(PermissionRequiredMixin,DeleteView):
    '''This view generates a view for deleting :class:`~mousedb.data.models.Cohort` objects.
    
    This view is restricted to logged in users with the delete-cohort permision. 
    It passes an object **cohort** when the url **/cohort/<slug>/delete** is requested.'''
    
    model = Cohort
    permission_required = "data.delete_cohort"
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('cohort-list')    

class PharmaceuticalDetail(LoginRequiredMixin,DetailView):
    '''This view generates details about a :class:`~mousedb.data.models.Pharmaceutical` object.
    
    This view is restricted to logged in users.
    It passes an object **pharmaceutical** when the url **/parameter/pharmaceutical/<id>** is requested.'''
    
    model = Pharmaceutical
    template_name = 'pharmaceutical_detail.html'
    context_object_name = 'pharmaceutical'

class PharmaceuticalList(LoginRequiredMixin,ListView):
    '''This view generates list of :class:`~mousedb.data.models.Pharmaceutical` objects.
    
    This view is restricted to logged in users.
    It passes an object **pharmaceutical** when the url **/parameter/pharmaceutical** is requested.'''
    
    model = Pharmaceutical
    template_name = 'pharmaceutical_list.html'
    context_object_name = 'pharmaceutical_list'
    
class PharmaceuticalCreate(PermissionRequiredMixin,CreateView):
    '''This view generates a form for creating a :class:`~mousedb.data.models.Pharmaceutical` object.
    
    This view is restricted to logged in users with the create-pharmaceutical permission.
    It is generated when the url **/parameter/pharmaceutical/new** is requested.'''
    
    model = Pharmaceutical
    permission_required = "data.add_pharmaceutical"    
    template_name = 'pharmaceutical_form.html'
    context_object_name = 'pharmaceutical'
    
class PharmaceuticalUpdate(PermissionRequiredMixin,UpdateView):
    '''This view generates a form for updating :class:`~mousedb.data.models.Pharmaceutical` objects.
    
    This view is restricted to logged in users with the update-pharmaceutical permision. 
    It passes an object **pharmaceutical** when the url **/parameter/pharmaceutical/<id>/edit** is requested.'''
    
    model = Pharmaceutical
    permission_required = "data.update_pharmaceutical"    
    template_name = 'pharmaceutical_form.html'
    context_object_name = 'pharmaceutical'        

class PharmaceuticalDelete(PermissionRequiredMixin,DeleteView):
    '''This view generates a view for deleting :class:`~mousedb.data.models.Pharmaceutical` objects.
    
    This view is restricted to logged in users with the delete-pharmaceutical permision. 
    It passes an object **pharmaceutical** when the url **/parameter/pharmaceutical/<id>/delete** is requested.'''
    
    model = Pharmaceutical
    permission_required = "data.delete_pharmaceutical"
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('pharmaceutical-list')

class TreatmentDetail(LoginRequiredMixin, DetailView):
    '''This view generates details about a :class:`~mousedb.data.models.Treatment` object.
    
    This view is restricted to logged in users.
    It passes an object **treatment** when the url **/treatment/<pk#>** is requested.'''
    
    model = Treatment
    template_name = 'treatment_detail.html'
    context_object_name = 'treatment'  

class TreatmentList(LoginRequiredMixin, ListView):
    '''This view generatea list of a :class:`~mousedb.data.models.Treatment` objects.
    
    This view is restricted to logged in users.
    It passes an object **treatment_list** when the url **/treatment** is requested.'''
    
    model = Treatment
    template_name = 'treatment_list.html'
    context_object_name = 'treatment_list'      

@login_required
def experiment_list(request):
	experiment_list = Experiment.objects.all()
	return render_to_response('experiment_list.html', {'experiment_list' : experiment_list},context_instance=RequestContext(request))

@login_required
def experiment_detail(request, experiment):
	experiment = Experiment.objects.get(pk=experiment)
	measurement_plasmaglucose = Measurement.objects.filter(assay__pk=1).filter(experiment=experiment).select_related()
	measurement_seruminsulin = Measurement.objects.filter(assay__pk=2).filter(experiment=experiment).select_related()
	measurement_bodyweight = Measurement.objects.filter(assay__pk=3).filter(experiment=experiment).select_related()
	return render_to_response('experiment_detail.html', {'experiment' : experiment, 'measurement_plasmaglucose' : measurement_plasmaglucose, 'measurement_seruminsulin': measurement_seruminsulin, 'measurement_bodyweight' : measurement_bodyweight},context_instance=RequestContext(request))

@login_required
def experiment_detail_all(request):
	measurement_plasmaglucose = Measurement.objects.filter(assay__pk=1).select_related()
	measurement_seruminsulin = Measurement.objects.filter(assay__pk=2).select_related()
	measurement_bodyweight = Measurement.objects.filter(assay__pk=3).select_related()
	return render_to_response('experiment_detail_all.html', {'measurement_plasmaglucose' : measurement_plasmaglucose, 'measurement_seruminsulin': measurement_seruminsulin, 'measurement_bodyweight' : measurement_bodyweight},context_instance=RequestContext(request))

@permission_required('data.add_measurement')
def add_measurement(request, experiment_id):
	"""This is a view to display a form to add single measurements to an experiment.
	
	It calls the object MeasurementForm, which has an autocomplete field for animal."""
	experiment = get_object_or_404(Experiment, pk=experiment_id)
	if request.method == 'POST':
		form = MeasurementForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect( experiment.get_absolute_url() ) 
	else:
		form = MeasurementForm() 
	return render_to_response("data_entry_form.html", {"form": form, "experiment": experiment }, context_instance=RequestContext(request))
	
@permission_required('data.add_experiment')
def study_experiment(request, study_id):
	study = Study.objects.get(pk=study_id)
	treatments = Treatment.objects.filter(study=study)
	if request.method == 'POST':
		form = StudyExperimentForm(request.POST, request.FILES)
		if form.is_valid():
			experiment = form.save(commit=False)
			experiment.study_id = study.id
			experiment.save()
			form.save()
			return HttpResponseRedirect('/mousedb/study/')
	else:
		form = StudyExperimentForm()
		form.fields["animals"].queryset = Animal.objects.filter(treatment__in=treatments)
	return render_to_response("study_experiment_form.html", {'form':form, 'study':study, 'treatments': treatments},context_instance=RequestContext(request))
	
def experiment_details_csv(request, experiment_id):
    """This view generates a csv output file of an experiment.
	
	The view writes to a csv table the animal, genotype, age (in days), assay and values."""
    experiment = get_object_or_404(Experiment, pk=experiment_id)
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=experiment.csv'
    writer = csv.writer(response)
    writer.writerow(["Animal","Cage", "Strain", "Genotype", "Age", "Assay", "Values", "Feeding", "Treatment"])
    for measurement in experiment.measurement_set.iterator():
        writer.writerow([
			measurement.animal,
            measurement.animal.Cage,
            measurement.animal.Strain,
			measurement.animal.Genotype, 
			measurement.age(), 
			measurement.assay, 
			measurement.values, 
            measurement.experiment.feeding_state,
			measurement.animal.treatment_set.all()
			])
    return response
    
    
def aging_csv(request):
    """This view generates a csv output file of all animal data for use in aging analysis.
	
	The view writes to a csv table the animal, strain, genotype, age (in days), and cause of death."""
    animal_list = Animal.objects.all()
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=aging.csv'
    writer = csv.writer(response)
    writer.writerow(["Animal", "Strain", "Genotype", "Age", "Death", "Alive"])
    for animal in animal_list.iterator():
        writer.writerow([
            animal.MouseID, 
            animal.Strain, 
            animal.Genotype, 
            animal.age(),
            animal.Cause_of_Death,
            animal.Alive            
            ])
    return response    
 
def litters_csv(request):
    """This view generates a csv output file of all animal data for use in litter analysis.
	
	The view writes to a csv table the birthdate, breeding cage and strain."""
    animal_list = Animal.objects.all()
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=litters.csv'
    writer = csv.writer(response)
    writer.writerow(["Born", "Breeding", "Strain"])
    for animal in animal_list:
        writer.writerow([
            animal.Born,
            animal.Breeding,
            animal.Strain
            ])
    return response   

def all_data_csv(request):
    """This view generates a csv output of all data for a strain."""

    measurement_list = Measurement.objects.filter(assay__assay = "Body Weight")
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=data.csv'
    writer = csv.writer(response)
    writer.writerow(["Animal", "Genotype", "Assay", "Value","Strain", "Age", "Cage", "Feeding", "Treatment"])
    for measurement in measurement_list:
        writer.writerow([
            measurement.animal,
            measurement.animal.Genotype,
            measurement.assay,
            int(measurement.values.split(',')[0]),
            measurement.animal.Strain,
            measurement.age(),
            measurement.animal.Cage,
            measurement.experiment.feeding_state,
            measurement.animal.treatment_set.all(),
            ])
    return response