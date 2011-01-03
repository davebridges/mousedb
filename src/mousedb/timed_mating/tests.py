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


class GroupsModelTests(TestCase):
    """Test the models contained in the 'groups' app."""

    def setUp(self):
        """Instantiate the test client."""
        self.client = Client()

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

class PlugEventViewTests(TestCase):
    """Test for views related to plug events.

    This testcase tests for plug list, plug detail, plug edit, plug new and plug delete pages.
    The testcase loads a test fixture, test_plugevents.json to populate a single instance (for edit, detail and delete pages)."""
    fixtures = ['test_plugevents', 'test_groups']

    def setUp(self):
        """Instantiate the test client."""
        self.client = Client()
        self.test_user = User.objects.create_user('blah', 'blah@blah.com', 'blah')
        self.test_user.is_superuser = True
        self.test_user.save()
        self.client.login(username='blah', password='blah')

    def tearDown(self):
        """Depopulate created model instances from test database."""
        self.client.logout()
        self.test_user.delete()

    def test_plug_list(self):
        """This tests for templates and staus code of the plug list pages."""
        response = self.client.get('/plug/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'jquery_script.html')
        self.assertTemplateUsed(response, 'jquery_ui_script_css.html')
        self.assertTemplateUsed(response, 'plug_list.html')
        self.assertTemplateUsed(response, 'plug_table.html')

    def test_plug_detail(self):
        """This tests for templates and staus code of the plug detail pages."""
        response = self.client.get('/plug/1/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'jquery_script.html')
        self.assertTemplateUsed(response, 'jquery_ui_script_css.html')
        self.assertTemplateUsed(response, 'plug_detail.html')

    def test_plug_new(self):
        """This tests for templates and staus code of the new plug pages."""
        response = self.client.get('/plug/new/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'jquery_script.html')
        self.assertTemplateUsed(response, 'jquery_ui_script_css.html')
        self.assertTemplateUsed(response, 'plug_form.html')

    def test_plug_edit(self):
        """This tests for templates and staus code of the plug edit pages."""
        response = self.client.get('/plug/1/edit/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'jquery_script.html')
        self.assertTemplateUsed(response, 'jquery_ui_script_css.html')
        self.assertTemplateUsed(response, 'plug_form.html')

    def test_plug_edit(self):
        """This tests for templates and staus code of the plug delete pages."""
        response = self.client.get('/plug/1/delete/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'jquery_script.html')
        self.assertTemplateUsed(response, 'jquery_ui_script_css.html')
        self.assertTemplateUsed(response, 'confirm_delete.html')
