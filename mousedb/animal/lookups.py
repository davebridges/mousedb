"""This is a configuration file for the ajax lookups for the animal app.

See http://code.google.com/p/django-ajax-selects/ for information about configuring the ajax lookups.
"""

from mousedb.animal.models import Animal

from django.db.models import Q
from django.utils.html import escape

from ajax_select import register, LookupChannel

@register('animals')
class AnimalLookup(LookupChannel):
    """This is the generic lookup for animals.
	
	It is to be used for all animal requests and directs to the 'animal' channel.
	"""
    model = Animal
    
    def get_query(self,q,request):
        """ This sets up the query for the lookup.
		
		The lookup searches the MouseID or the id (database identifier) for the mouse."""
        return Animal.objects.filter(Q(MouseID__icontains=q)|Q(id__icontains=q)|Q(Cage__icontains=q))

    def format_result(self,animal):
        """ This controls the display of the dropdown menu.
		
		This is set to show the unicode name of the animal, as well as its Cage and its Markings."""
        #return unicode(animal)
        return u"%s <strong>Cage:</strong> %s <strong>Markings:</strong> %s" % (animal, animal.Cage, animal.Markings)


    def format_item(self,animal):
        """ the display of a currently selected object in the area below the search box. html is OK """
        return u"%s <strong>Cage:</strong> %s <strong>Markings:</strong> %s" % (animal, animal.Cage, animal.Markings)

    def get_objects(self,ids):
        """ given a list of ids, return the objects ordered as you would like them on the admin page.
            this is for displaying the currently selected items (in the case of a ManyToMany field)
        """
        return Animal.objects.filter(pk__in=ids)
		
@register('animals-males')
class AnimalLookupMale(object):
    """This is the generic lookup for animals.
	
	It is to be used for all animal requests and directs to the 'animal-male' channel.
	"""
    model = Animal
    
    def get_query(self,q,request):
        """ This sets up the query for the lookup.
		
		The lookup searches the MouseID or the id (database identifier) for the mouse.  It then filters this set for only males."""
        return Animal.objects.filter(Q(MouseID__icontains=q)|Q(id__icontains=q)|Q(Cage__icontains=q)).filter(Gender='M')

    def format_result(self,animal):
        """ This controls the display of the dropdown menu.
		
		This is set to show the unicode name of the animal, as well as its Cage and its Markings."""
        #return unicode(animal)
        return u"%s <strong>Cage:</strong> %s <strong>Markings:</strong> %s" % (animal, animal.Cage, animal.Markings)


    def format_item(self,animal):
        """ the display of a currently selected object in the area below the search box. html is OK """
        return u"%s <strong>Cage:</strong> %s <strong>Markings:</strong> %s" % (animal, animal.Cage, animal.Markings)

    def get_objects(self,ids):
        """ given a list of ids, return the objects ordered as you would like them on the admin page.
            this is for displaying the currently selected items (in the case of a ManyToMany field)
        """
        return Animal.objects.filter(pk__in=ids)

@register('animals-females')		
class AnimalLookupFemales(LookupChannel):
    """This is the generic lookup for animals.
	
	It is to be used for all animal requests and directs to the 'animal-female' channel.
	"""

    model = Animal

    def get_query(self,q,request):
        """ This sets up the query for the lookup.
		
		The lookup searches the MouseID or the id (database identifier) for the mouse.  It then filters this set for only females."""
        return Animal.objects.filter(Q(MouseID__icontains=q)|Q(id__icontains=q)|Q(Cage__icontains=q)).filter(Gender='F')

    def get_result(self,animal):
        """ This controls the display of the dropdown menu.
		
		This is set to show the unicode name of the animal, as well as its Cage and its Markings."""
        #return unicode(animal)
        return u"%s <strong>Cage:</strong> %s <strong>Markings:</strong> %s" % (animal, animal.Cage, animal.Markings)

    def format_match(self,animal):
        """ the display of a currently selected object in the area below the search box. html is OK """
        return u"%s <strong>Cage:</strong> %s <strong>Markings:</strong> %s" % (animal, animal.Cage, animal.Markings)

    def format_item_display(self,animalj):
        """ (HTML) formatted item for displaying item in the selected deck area """
        return u"%s<div><i>%s</i></div>" % (escape(obj.MouseID),escape(obj.Cage))
