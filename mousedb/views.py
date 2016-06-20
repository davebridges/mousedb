"""This package defines simple root views.

Currently this package includes views for both the logout and home pages."""

import datetime

from tastypie.models import ApiKey

from braces.views import LoginRequiredMixin

from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import logout
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from mousedb.animal.models import Animal, Strain
from django.utils.decorators import method_decorator
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateView
from django.conf import settings

def logout_view(request):
    """This view logs out the current user.
	
    It redirects the user to the '/index/' page which in turn should redirect to the login page."""
    logout(request)
    return HttpResponseRedirect(reverse('home'))

@login_required
def home(request):
    """This view generates the data for the home page.
    
    This login restricted view passes dictionaries containing the current cages, animals and strains as well as the totals for each.  This data is passed to the template home.html"""
    cage_list = Animal.objects.values("Cage").distinct()
    cage_list_current = cage_list.filter(Alive=True)
    animal_list = Animal.objects.all()
    animal_list_current = animal_list.filter(Alive=True)
    strain_list = animal_list.values("Strain").distinct()
    strain_list_current = animal_list_current.values("Strain").distinct()
    return render(request, 'home.html', {'animal_list':animal_list, 'animal_list_current':animal_list_current, 'strain_list':strain_list, 'strain_list_current':strain_list_current, 'cage_list':cage_list, 'cage_list_current':cage_list_current})
    
class ProtectedListView(ListView):
    """This subclass of ListView generates a login_required protected version of the ListView.
    
    This ProtectedListView is then subclassed instead of using ListView for login_required views."""
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProtectedListView, self).dispatch(*args, **kwargs)    
        
class ProtectedDetailView(DetailView):
    """This subclass of DetailView generates a login_required protected version of the DetailView.
    
    This ProtectedDetailView is then subclassed instead of using ListView for login_required views."""
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProtectedDetailView, self).dispatch(*args, **kwargs)

class RestrictedUpdateView(UpdateView):
    """Generic update view that checks permissions.
    
    This is from http://djangosnippets.org/snippets/2317/ and subclasses the UpdateView into one that requires permissions to update a particular model."""
    def dispatch(self, request, *args, **kwargs):
        @permission_required('%s.change_%s' % (self.model._meta.app_label, self.model._meta.module_name))
        def wrapper(request, *args, **kwargs):
            return super(RestrictedUpdateView, self).dispatch(request, *args, **kwargs)
        return wrapper(request, *args, **kwargs)

class RestrictedCreateView(CreateView):
    """Generic create view that checks permissions.
    
    This is from http://djangosnippets.org/snippets/2317/ and subclasses the UpdateView into one that requires permissions to create a particular model."""
    def dispatch(self, request, *args, **kwargs):
        @permission_required('%s.create_%s' % (self.model._meta.app_label, self.model._meta.module_name))
        def wrapper(request, *args, **kwargs):
            return super(RestrictedCreateView, self).dispatch(request, *args, **kwargs)
        return wrapper(request, *args, **kwargs)

class RestrictedDeleteView(DeleteView):
    """Generic delete view that checks permissions.
    
    This is from http://djangosnippets.org/snippets/2317/ and subclasses the UpdateView into one that requires permissions to delete a particular model."""
    def dispatch(self, request, *args, **kwargs):
        @permission_required('%s.delete_%s' % (self.model._meta.app_label, self.model._meta.module_name))
        def wrapper(request, *args, **kwargs):
            return super(RestrictedDeleteView, self).dispatch(request, *args, **kwargs)
        return wrapper(request, *args, **kwargs) 
        
class APIKeyView(LoginRequiredMixin, TemplateView):
    """This view shows the API key for the currently logged in user."""
    
    template_name = "api_key.html"     

