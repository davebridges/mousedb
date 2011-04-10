"""This file contains tests for the timed_mating application.

These tests will verify generation of a new PlugEvent object.
"""

import datetime

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User

from mousedb.timed_mating.models import PlugEvents
from mousedb.animal.models import Breeding, Strain, Animal
 
MODELS = [PlugEvents,]


class Timed_MatingModelTests(TestCase):
    """Test the models contained in the 'timed_mating' app."""

  
    def setUp(self):
        """Instantiate the test client.  Creates a test user."""
        self.client = Client()
        self.test_user = User.objects.create_user('blah', 'blah@blah.com', 'blah')
        self.test_user.is_superuser = True
        self.test_user.save()
        self.client.login(username='blah', password='blah')

    def tearDown(self):
        """Depopulate created model instances from test database."""
        for model in MODELS:
            for obj in model.objects.all():
                obj.delete()

    def test_create_plugevent_minimal(self):
        """This is a test for creating a new PlugEvent object, with only the minimum being entered."""
        new_plugevent = PlugEvents(PlugDate = datetime.date.today() )
        new_plugevent.save()
	test_plugevent = PlugEvents.objects.get(PlugDate = datetime.date.today() )
        self.assertEquals(new_plugevent, test_plugevent)
        self.assertEquals(test_plugevent.__unicode__(), "Plug Event - 1")

    def test_create_plugevent_most_fields(self):
        """This is a test for creating a new PlugEvent object.
        
        This test uses a Breeding, PlugDate, PlugMale and PlugFemale field."""
        new_plugevent = PlugEvents(
            Breeding = Breeding(Strain = Strain(Strain="Test Strain", Strain_slug="Test_Strain")),
            PlugDate = datetime.date.today(),
            PlugMale = Animal(
                Strain = Strain(Strain="Test Strain", Strain_slug="Test_Strain"), 
                Background = "Mixed", 
                Genotype="-/-", 
                Gender="M"
                ),
            PlugFemale = Animal(
                Strain = Strain(Strain="Test Strain", Strain_slug="Test_Strain"), 
                Background = "Mixed", 
                Genotype="-/-", 
                Gender="M"
                )
            )
        new_plugevent.save()
	test_plugevent = PlugEvents.objects.get(PlugDate = datetime.date.today() )
        self.assertEquals(test_plugevent, new_plugevent)
        self.assertEquals(test_plugevent.__unicode__(), "Plug Event - %i" % test_plugevent.id)

    def test_set_plugevent_inactive(self):
        """This is a test for the automatic inactivation of a cage when the SacrificeDate is entered."""
        plugevent = PlugEvents(PlugDate = datetime.date.today() )
        plugevent.save()
        self.assertEquals(plugevent.__unicode__(), "Plug Event - 1")
        self.assertEquals(plugevent.Active, True)
        plugevent = PlugEvents(id = 1, PlugDate = datetime.date.today(), SacrificeDate = datetime.date.today() )
        plugevent.save()
        self.assertEquals(plugevent.Active, False)

class Timed_MatingViewTests(TestCase):
    """Test the views contained in the 'timed_mating' app."""

    fixtures = ['test_breeding','test_plugevents', 'test_animals']

    def setUp(self):
        """Instantiate the test client.  Creates a test user."""
        self.client = Client()
        self.test_user = User.objects.create_user('testuser', 'blah@blah.com', 'testpassword')
        self.test_user.is_superuser = True
        self.test_user.is_active = True
        self.test_user.save()
        self.assertEqual(self.test_user.is_superuser, True)
        login = self.client.login(username='testuser', password='testpassword')
        self.failUnless(login, 'Could not log in')

    def tearDown(self):
        """Depopulate created model instances from test database."""
        for model in MODELS:
            for obj in model.objects.all():
                obj.delete()

    def test_plugevent_list(self):
        """This tests the plugevent-list view, ensuring that templates are loaded correctly.  

        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        test_response = self.client.get('/plugs/')
        self.assertEqual(test_response.status_code, 200)
        self.assertTrue('plugevents_list' in test_response.context)
        self.assertTemplateUsed(test_response, 'base.html')
        self.assertTemplateUsed(test_response, 'jquery_script.html')
        self.assertTemplateUsed(test_response, 'jquery_ui_script_css.html')
        self.assertTemplateUsed(test_response, 'plugevents_list.html')
        self.assertTemplateUsed(test_response, 'plug_table.html')
        self.assertEqual([plugevent.pk for plugevent in test_response.context['plugevents_list']], [1])        
        self.assertEqual([plugevent.PlugDate for plugevent in test_response.context['plugevents_list']], [datetime.date(2010,10,01)])     
        self.assertEqual([plugevent.PlugFemale.id for plugevent in test_response.context['plugevents_list']], [1])


    def test_plugevent_detail(self):
        """This tests the plugevent-detail view, ensuring that templates are loaded correctly.  

        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        test_response = self.client.get('/plugs/1/')
        self.assertEqual(test_response.status_code, 200)
        self.assertTrue('plugevent' in test_response.context)        
        self.assertTemplateUsed(test_response, 'base.html')
        self.assertTemplateUsed(test_response, 'jquery_script.html')
        self.assertTemplateUsed(test_response, 'jquery_ui_script_css.html')
        self.assertTemplateUsed(test_response, 'plugevents_detail.html')
        self.assertEqual(test_response.context['plugevent'].pk, 1)
        self.assertEqual(test_response.context['plugevent'].PlugDate, datetime.date(2010,10,01))
        self.assertEqual(test_response.context['plugevent'].PlugFemale.id, 1) 

        null_response = self.client.get('/plugs/2/')
        self.assertEqual(null_response.status_code, 404)        


    def test_plugevent_new(self):
        """This tests the plugevent-new view, ensuring that templates are loaded correctly.  

        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        test_response = self.client.get('/plugs/new/')
        self.assertEqual(test_response.status_code, 200)
        self.assertTemplateUsed(test_response, 'base.html')
        self.assertTemplateUsed(test_response, 'jquery_script.html')
        self.assertTemplateUsed(test_response, 'jquery_ui_script_css.html')
        self.assertTemplateUsed(test_response, 'plugevents_form.html')

    def test_plugevent_edit(self):
        """This tests the plugevent-edit view, ensuring that templates are loaded correctly.  

        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        test_response = self.client.get('/plugs/1/edit/')
        self.assertEqual(test_response.status_code, 200)
        self.assertTrue('plugevent' in test_response.context)          
        self.assertTemplateUsed(test_response, 'base.html')
        self.assertTemplateUsed(test_response, 'jquery_script.html')
        self.assertTemplateUsed(test_response, 'jquery_ui_script_css.html')
        self.assertTemplateUsed(test_response, 'plugevents_form.html')
        self.assertEqual(test_response.context['plugevent'].pk, 1)
        self.assertEqual(test_response.context['plugevent'].PlugDate, datetime.date(2010,10,01))
        self.assertEqual(test_response.context['plugevent'].PlugFemale.id, 1)    

        null_response = self.client.get('/plugs/2/')
        self.assertEqual(null_response.status_code, 404)         

    def test_plugevent_delete(self):
        """This tests the plugevent-delete view, ensuring that templates are loaded correctly.  

        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        test_response = self.client.get('/plugs/1/delete/')
        self.assertEqual(test_response.status_code, 200)
        self.assertTrue('plugevent' in test_response.context)           
        self.assertTemplateUsed(test_response, 'base.html')
        self.assertTemplateUsed(test_response, 'jquery_script.html')
        self.assertTemplateUsed(test_response, 'jquery_ui_script_css.html')
        self.assertTemplateUsed(test_response, 'confirm_delete.html')
        self.assertEqual(test_response.context['plugevent'].pk, 1)
        self.assertEqual(test_response.context['plugevent'].PlugDate, datetime.date(2010,10,01))
        self.assertEqual(test_response.context['plugevent'].PlugFemale.id, 1)            
        
        null_response = self.client.get('/plugs/2/')
        self.assertEqual(null_response.status_code, 404) 
        
    def test_plugevent_new(self):
        """This tests the breeding-plugevent-new view, ensuring that templates are loaded correctly.  

        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        test_response = self.client.get('/plugs/breeding/1/new/')
        self.assertEqual(test_response.status_code, 200)
        self.assertTrue('breeding' in test_response.context)
        self.assertEqual(test_response.context['breeding'].pk, 1)
        self.assertEqual(test_response.context['breeding'].Start, datetime.date(2010,01,01))
        self.assertEqual(test_response.context['breeding'].Cage, '12345')          
        self.assertEqual(test_response.context['breeding'].Strain.__unicode__(), 'test_strain')          
        self.assertTemplateUsed(test_response, 'base.html')
        self.assertTemplateUsed(test_response, 'jquery_script.html')
        self.assertTemplateUsed(test_response, 'jquery_ui_script_css.html')
        self.assertTemplateUsed(test_response, 'breeding_plugevent_form.html') 

        null_response = self.client.get('/plugs/breeding/2/new/')
        self.assertEqual(null_response.status_code, 404)         
