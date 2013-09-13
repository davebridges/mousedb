import csv

from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import TemplateView, View
from django.core.urlresolvers import reverse_lazy

from braces.views import LoginRequiredMixin, PermissionRequiredMixin

from mousedb.animal.models import Animal, Strain
from mousedb.animal.views import AnimalList
from mousedb.data.models import Experiment, Measurement, Study, Treatment, Pharmaceutical, Cohort, Diet
from mousedb.data.forms import MeasurementForm, MeasurementFormSet, StudyExperimentForm, TreatmentForm, CohortForm

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
    form_class = CohortForm
    permission_required = "data.add_cohort"    
    template_name = 'cohort_form.html'
    context_object_name = 'cohort'
    
class CohortUpdate(PermissionRequiredMixin,UpdateView):
    '''This view generates a form for updating :class:`~mousedb.data.models.Cohort` objects.
    
    This view is restricted to logged in users with the update-cohort permision. 
    It passes an object **object** when the url **/cohort/<slug>/edit** is requested.'''
    
    model = Cohort
    form_class = CohortForm
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
    
class CohortData(LoginRequiredMixin, ListView):
    '''This view is for displaying all data specific to a particular :class:`~mousedb.data.Cohort`.
    
    It filters the data based on the slug field in the strain and returns a data_list when /some-cohort/data is requested.'''
    
    context_object_name = 'data_list'
    template_name ='data.html' 
    
    def get_queryset(self):
        '''The queryset is filtered by measurements of animals which are part of that strain.'''
        cohort = get_object_or_404(Cohort, slug=self.kwargs['slug'])
        animals = cohort.animals.all()
        return Measurement.objects.filter(animal=animals)     
    
class CohortDataCSV(TemplateView):
    '''This view is for downloading all data specific to a particular :class:`~mousedb.data.Cohort`.
    
    It filters the data based on the slug field in the strain and returns a csv file when /some-cohort/data.csv is requested.'''
    
    def get(self, request, *args, **kwargs):
        '''The queryset is filtered by measurements of animals which are part of that strain.'''
        cohort = get_object_or_404(Cohort, slug=self.kwargs['slug'])
        animals = cohort.animals.all()
        measurements = Measurement.objects.filter(animal=animals)    
        return data_csv(self.request, measurements)          

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
	
def experiment_details_csv(request, pk):
    """This view generates a csv output file of an experiment.
	
	The view writes to a csv table the animal, genotype, age (in days), assay and values."""
    experiment = get_object_or_404(Experiment, pk=pk)
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
    writer.writerow(["Animal", "Strain", "Genotype", "Gender", "Age", "Death", "Alive"])
    for animal in animal_list.iterator():
        writer.writerow([
            animal.MouseID, 
            animal.Strain, 
            animal.Genotype, 
            animal.Gender,
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

def data_csv(request, measurement_list):
    """This view generates a csv output of all data for a strain.
    
    For this function to work, you have to provide the filtered set of measurements."""

    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=data.csv'
    writer = csv.writer(response)
    writer.writerow(["Animal", "Genotype", "Gender","Assay", "Value","Strain", "Age", "Cage", "Feeding", "Treatment"])
    for measurement in measurement_list:
        writer.writerow([
            measurement.animal,
            measurement.animal.Genotype,
            measurement.animal.Gender,
            measurement.assay,
            measurement.values.split(',')[0],
            measurement.animal.Strain,
            measurement.age(),
            measurement.animal.Cage,
            measurement.experiment.feeding_state,
            measurement.animal.treatment_set.all(),
            ])
    return response
    
    
class ExperimentDetail(LoginRequiredMixin, DetailView):
    '''This view is for details of a particular :class:`~mousedb.data.Experiment`.
    
    It passes an object **experiment** when the url **/experiment/<pk#>** is requested.'''

    model = Experiment
    context_object_name = 'experiment'
    template_name = 'experiment_detail.html'
    
class ExperimentCreate(PermissionRequiredMixin, CreateView):
    '''This view is for creating a new :class:`~mousedb.data.Experiment`.
    
    It requires the permissions to create a new experiment and is found at the url **/experiment/new**.'''
    
    permission_required = 'data.create_experiment'
    model = Experiment
    template_name = 'experiment_form.html'
    
class ExperimentUpdate(PermissionRequiredMixin, UpdateView):
    '''This view is for updating a :class:`~mousedb.data.Experiment`.
    
    It requires the permissions to update an experiment and is found at the url **/experiment/<pk#>/edit**.'''
    
    permission_required = 'data.update_experiment'
    model = Experiment
    context_object_name = 'experiment'
    template_name = 'experiment_form.html'   
    
class ExperimentDelete(PermissionRequiredMixin, DeleteView):
    '''This view is for deleting a :class:`~mousedb.data.Experiment`.
    
    It requires the permissions to delete an experiment and is found at the url **/experiment/<pk$>/delete**.'''
    
    permission_required = 'data.delete_experiment'
    model = Experiment
    template_name = 'confirm_delete.html' 
    success_url = reverse_lazy('experiment-list')        
    
class ExperimentList(LoginRequiredMixin, ListView):
    '''This view is for details of a particular :class:`~mousedb.data.Experiment`.
    
    It passes an object **experiment_list** when the url **/experiment** is requested.''' 
    
    model = Experiment
    template_object_name = 'experiment_list'
    template_name = 'experiment_list.html'   

class MeasurementCreate(LoginRequiredMixin, CreateView):
    '''This view is for adding a new measurement.
    
    It creates a form when the url **/experiment/data/new** is requested.'''
    
    permission_required = 'data.add_measurement'
    form_class = MeasurementForm
    model = Measurement
    template_object_name = 'data'
    template_name = 'measurement_form.html' 
    
class MeasurementList(LoginRequiredMixin, ListView):
    '''This view shows all :class:`~mousedb.data.Measurement` objects recorded .
    
    It passes an object **data* when the url **/experiment/data/all** is requested.'''
    
    model = Measurement
    context_object_name = 'data_list'
    template_name = 'data.html'  
    
     
class MeasurementListCSV(View):
    '''This view shows all :class:`~mousedb.data.Measurement` objects recorded as a CSV file.
    
    It passes an object **data* when the url **/experiment/data/all.csv** is requested.'''
    
    def get(self, request, *args, **kwargs):
        '''The queryset returns all measurement objects'''
        measurements = Measurement.objects.all()    
        return data_csv(self.request, measurements)  
    
class MeasurementUpdate(PermissionRequiredMixin, UpdateView):
    '''This view is for updating a :class:`~mousedb.data.Measurement`.
    
    It requires the permissions to update a measurement and is found at the url **/experiment/data/<pk#>/edit**.'''
    
    permission_required = 'data.update_measurement'
    form_class = MeasurementForm
    model = Measurement
    template_object_name = 'data'
    template_name = 'measurement_form.html'   
    
class MeasurementDelete(PermissionRequiredMixin, DeleteView):
    '''This view is for deleting a :class:`~mousedb.data.Measurement`.
    
    It requires the permissions to delete a measurement and is found at the url **/experiment/data/<pk$>/delete**.'''
    
    permission_required = 'data.delete_measurement'
    model = Measurement
    template_name = 'confirm_delete.html' 
    success_url = reverse_lazy('experiment-list')  
    
class StudyDetail(LoginRequiredMixin, DetailView):
    '''This view is for details of a particular :class:`~mousedb.data.Study`.
    
    It passes an object **study** when the url **/study/<pk#>** is requested.'''

    model = Study
    context_object_name = 'study'
    template_name = 'study_detail.html'
    
class StudyCreate(PermissionRequiredMixin, CreateView):
    '''This view is for creating a new :class:`~mousedb.data.Study`.
    
    It requires the permissions to create a new study and is found at the url **/study/new**.'''
    
    permission_required = 'data.create_study'
    model = Study
    template_name = 'study_form.html'
    
class StudyUpdate(PermissionRequiredMixin, UpdateView):
    '''This view is for updating a :class:`~mousedb.data.Study`.
    
    It requires the permissions to update a study and is found at the url **/study/<pk#>/edit**.'''
    
    permission_required = 'data.update_study'
    model = Study
    context_object_name = 'study'
    template_name = 'study_form.html'   
    
class StudyDelete(PermissionRequiredMixin, DeleteView):
    '''This view is for deleting a :class:`~mousedb.data.Study`.
    
    It requires the permissions to delete a study and is found at the url **/study/<pk$>/delete**.'''
    
    permission_required = 'data.delete_study'
    model = Study
    template_name = 'confirm_delete.html' 
    success_url = reverse_lazy('data-home')        
    
class StudyList(LoginRequiredMixin, ListView):
    '''This view is for details of a particular :class:`~mousedb.data.Study`.
    
    It passes an object **study_list** when the url **/study** is requested.''' 
    
    model = Study
    template_object_name = 'study_list'
    template_name = 'study_list.html' 
    
class StudyAgeing(AnimalList):
    '''This view shows animals in an ageing study.
    
    It displays all animals that died of unknown (natural) causes.
    This is a subclass of :class:`~mousedb.animal.views.AnimalList`.'''
    
    queryset = Animal.objects.filter(Alive=False, Cause_of_Death="Unknown")   
    
class TreatmentDetail(LoginRequiredMixin, DetailView):
    '''This view is for details of a particular :class:`~mousedb.data.Treatment`.
    
    It passes an object **treatment** when the url **/treatment/<pk#>** is requested.'''

    model = Treatment
    context_object_name = 'treatment'
    template_name = 'treatment_detail.html'
    
class TreatmentCreate(PermissionRequiredMixin, CreateView):
    '''This view is for creating a new :class:`~mousedb.data.Treatment`.
    
    It requires the permissions to create a new treatment and is found at the url **/treatment/new**.'''
    
    permission_required = 'data.create_treatment'
    form_class = TreatmentForm    
    model = Treatment
    template_name = 'treatment_form.html'
    
class TreatmentUpdate(PermissionRequiredMixin, UpdateView):
    '''This view is for updating a :class:`~mousedb.data.Treatment`.
    
    It requires the permissions to update a treatment and is found at the url **/treatment/<pk#>/edit**.'''
    
    permission_required = 'data.update_treatment'
    model = Treatment
    form_class = TreatmentForm
    context_object_name = 'treatment'
    template_name = 'treatment_form.html'   
    
class TreatmentDelete(PermissionRequiredMixin, DeleteView):
    '''This view is for deleting a :class:`~mousedb.data.Treatment`.
    
    It requires the permissions to delete a treatment and is found at the url **/treatment/<pk$>/delete**.'''
    
    permission_required = 'data.delete_treatment'
    model = Treatment
    template_name = 'confirm_delete.html' 
    success_url = reverse_lazy('data-home')        
    
class TreatmentList(LoginRequiredMixin, ListView):
    '''This view is for details of a particular :class:`~mousedb.data.Treatment`.
    
    It passes an object **treatment_list** when the url **/treatment** is requested.''' 
    
    model = Treatment
    template_object_name = 'treatment_list'
    template_name = 'treatment_list.html'      
    
class DietDetail(LoginRequiredMixin, DetailView):
    '''This view is for details of a particular :class:`~mousedb.data.Diet`.
    
    It passes an object **diet** when the url **/diet/<pk#>** is requested.'''

    model = Diet
    context_object_name = 'diet'
    template_name = 'diet_detail.html'
    
class DietCreate(PermissionRequiredMixin, CreateView):
    '''This view is for creating a new :class:`~mousedb.data.Diet`.
    
    It requires the permissions to create a new diet and is found at the url **/diet/new**.'''
    
    permission_required = 'data.create_diet' 
    model = Diet
    template_name = 'diet_form.html'
    
class DietUpdate(PermissionRequiredMixin, UpdateView):
    '''This view is for updating a :class:`~mousedb.data.Diet`.
    
    It requires the permissions to update a diet and is found at the url **/diet/<pk#>/edit**.'''
    
    permission_required = 'data.update_diet'
    model = Diet
    context_object_name = 'diet'
    template_name = 'diet_form.html'   
    
class DietDelete(PermissionRequiredMixin, DeleteView):
    '''This view is for deleting a :class:`~mousedb.data.Diet`.
    
    It requires the permissions to delete a diet and is found at the url **/diet/<pk$>/delete**.'''
    
    permission_required = 'data.delete_diet'
    model = Diet
    template_name = 'confirm_delete.html' 
    success_url = reverse_lazy('data-home')        
    
class DietList(LoginRequiredMixin, ListView):
    '''This view is for details of a particular :class:`~mousedb.data.Diet`.
    
    It passes an object **diet_list** when the url **/diet** is requested.''' 
    
    model = Diet
    template_object_name = 'diet_list'
    template_name = 'diet_list.html' 
    
class StrainData(LoginRequiredMixin, ListView):
    '''This view is for displaying all data specific to a particular :class:`~mousedb.animals.Strain`.
    
    It filters the data based on the slug field in the strain and returns a data_list when /some-strain/data is requested.'''
    
    context_object_name = 'data_list'
    template_name ='data.html' 
    
    def get_queryset(self):
        '''The queryset is filtered by measurements of animals which are part of that strain.'''
        strain = get_object_or_404(Strain, Strain_slug=self.kwargs['strain_slug'])
        animals = Animal.objects.filter(Strain=strain)
        return Measurement.objects.filter(animal=animals)  
        
class StrainDataCSV(TemplateView):
    '''This view is for downloading all data specific to a particular :class:`~mousedb.animals.Strain`.
    
    It filters the data based on the slug field in the strain and returns a csv file when /some-strain/data.csv is requested.'''
    
    def get(self, request, *args, **kwargs):
        '''The queryset is filtered by measurements of animals which are part of that strain.'''
        strain = get_object_or_404(Strain, Strain_slug=self.kwargs['strain_slug'])
        animals = Animal.objects.filter(Strain=strain)
        measurements = Measurement.objects.filter(animal=animals)    
        return data_csv(self.request, measurements)     
        
                 
