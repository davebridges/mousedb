import datetime

from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.template import RequestContext
from django.db import connection
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db.models import Q

from mousedb.animal.models import Animal, Strain
from mousedb import settings

def logout_view(request):
    """This view logs out the current user.
	
    It redirects the user to the '/index/' page which in turn should redirect to the login page."""
    logout(request)
    return HttpResponseRedirect(reverse('home'))

@login_required
def todo(request):
	eartag_list = Animal.objects.filter(Born__lt=(datetime.date.today() - datetime.timedelta(days=settings.WEAN_AGE))).filter(MouseID__isnull=True, Alive=True)
	genotype_list = Animal.objects.filter(Q(Genotype='N.D.')|Q(Genotype__icontains='?')).filter(Alive=True, Born__lt=(datetime.date.today() - datetime.timedelta(days=settings.GENOTYPE_AGE)))
	wean = datetime.date.today() - datetime.timedelta(days=settings.WEAN_AGE)
	wean_list = Animal.objects.filter(Born__lt=wean).filter(Weaned=None,Alive=True).exclude(Strain=2).order_by('Strain','Background','Rack','Cage')
	return render_to_response('todo.html', {'eartag_list':eartag_list, 'wean_list':wean_list, 'genotype_list':genotype_list},context_instance=RequestContext(request))

@login_required
def home(request):
	cursor = connection.cursor()
	cage_list = Animal.objects.values("Cage")
	cage_list_current = Animal.objects.filter(Alive=True).values("Cage")
	animal_list = Animal.objects.all()
	animal_list_current = Animal.objects.filter(Alive=True)
	strain_list = Strain.objects.all()
	strain_list_current = Strain.objects.filter(animal__Alive=True)
	return render_to_response('home.html', {'animal_list':animal_list, 'animal_list_current':animal_list_current, 'strain_list':strain_list, 'strain_list_current':strain_list_current, 'cage_list':cage_list, 'cage_list_current':cage_list_current},context_instance=RequestContext(request))

