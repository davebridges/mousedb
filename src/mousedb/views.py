"""This package defines simple root views.

Currently this package includes views for both the logout and home pages."""

import datetime

from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from mousedb.animal.models import Animal, Strain
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from mousedb import settings

def logout_view(request):
    """This view logs out the current user.
	
    It redirects the user to the '/index/' page which in turn should redirect to the login page."""
    logout(request)
    return HttpResponseRedirect(reverse('home'))

@login_required
def home(request):
    """This view generates the data for the home page.
    
    This login restricted view passes dictionaries containing the current cages, animals and strains as well as the totals for each.  This data is passed to the template home.html"""
    cage_list = Animal.objects.values("Cage")
    cage_list_current = Animal.objects.filter(Alive=True).values("Cage")
    animal_list = Animal.objects.all()
    animal_list_current = Animal.objects.filter(Alive=True)
    strain_list = Strain.objects.all()
    strain_list_current = Strain.objects.filter(animal__Alive=True)
    return render_to_response('home.html', {'animal_list':animal_list, 'animal_list_current':animal_list_current, 'strain_list':strain_list, 'strain_list_current':strain_list_current, 'cage_list':cage_list, 'cage_list_current':cage_list_current},context_instance=RequestContext(request))
    
class ProtectedListView(ListView):
    """This subclass of LisView generates a login_required protected version of the ListView.
    
    This ProtectedListView is then subclassed instead of using ListView for login_required views."""
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProtectedListView, self).dispatch(*args, **kwargs)    

