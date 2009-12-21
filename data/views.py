from mousedb.animal.models import Animal
from mousedb.data.models import Experiment, Measurement, Study, Treatment
from mousedb.data.forms import MeasurementForm, StudyExperimentForm
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.forms.models import modelformset_factory
from django.forms.formsets import formset_factory
from django import forms



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

@login_required
def add_measurement(request, experiment_id):
	experiment = Experiment.objects.get(id=experiment_id)
	MeasurementFormSet = modelformset_factory(Measurement, form=MeasurementForm, extra=10, can_delete=True)
	if request.method == 'POST':
		formset = MeasurementFormSet()
		if formset.is_valid():
			formset.save()
	else:
		formset = MeasurementFormSet()
	return render_to_response("data_entry_form.html", {"formset": formset, "experiment": experiment }, context_instance=RequestContext(request))

@login_required
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
		form.fields["animals"].queryset = Animal.objects.filter(treatment=treatments)
	return render_to_response("study_experiment_form.html", {'form':form, 'study':study, 'treatments': treatments},context_instance=RequestContext(request))
	


