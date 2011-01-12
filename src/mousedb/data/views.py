import csv

from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext

from mousedb.animal.models import Animal
from mousedb.data.models import Experiment, Measurement, Study, Treatment
from mousedb.data.forms import MeasurementForm, MeasurementFormSet, StudyExperimentForm



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
	
@login_required
def experiment_details_csv(request, experiment_id):
    """This view generates a csv output file of an experiment.
	
	The view writes to a csv table the animal, genotype, age (in days), assay and values."""
    experiment = get_object_or_404(Experiment, pk=experiment_id)
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=experiment.csv'
    writer = csv.writer(response)
    writer.writerow(["Animal", "Genotype", "Age (in Days)", "Assay", "Value(s)", "Treatment"])
    for measurement in experiment.measurement_set.iterator():
        writer.writerow([
			measurement.animal, 
			measurement.animal.Genotype, 
			measurement.age(), 
			measurement.assay, 
			measurement.values, 
			#measurement.animal.treatment_set.all()[0] this only works if an animal is in a treatment group
			])
    return response

