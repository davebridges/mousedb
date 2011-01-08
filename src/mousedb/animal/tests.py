"""This file contains tests for the animal application.

These tests will verify generation and function of a new breeding, strain and animal object.
"""

import datetime

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User

from mousedb.animal.models import Animal, Strain, Breeding

MODELS = [Breeding, Animal, Strain]

class AnimalModelTests(TestCase):
    """Tests the model attributes of Animal objects contained in the animal app."""

    fixtures = ['test_animals']
    
    def setUp(self):
        """Instantiate the test client."""
        self.client = Client()
    
    def tearDown(self):
        """Depopulate created model instances from test database."""
        for model in MODELS:
            for obj in model.objects.all():
                obj.delete()
    
    def test_create_animal_minimal(self):
        """This is a test for creating a new animal object, with only the minimum fields being entered"""
        animal = Animal(Strain = Strain.objects.get(pk=1), Genotype="-/-", Background="Mixed")
        animal.save()
        animal_id = animal.id
        self.assertEquals(animal.__unicode__(), "test_strain (2)")

    def test_animal_unicode(self):
        """This is a test for creating a new animal object, with only the minimum fields being entered.  It then tests that the correct unicode representation is being generated."""
        animal = Animal(Strain = Strain.objects.get(pk=1), Genotype="-/-", Background="Mixed")
        animal.save()
        animal_id = animal.id
        self.assertEquals(animal.__unicode__(), "test_strain (2)")
        animal.MouseID = 1234
        animal.save()
        self.assertEquals(animal.__unicode__(), "test_strain-EarTag #1234")

class BreedingModelTests(TestCase):
    """Tests the model attributes of Breeding objects contained in the animal app."""

    fixtures = ['test_group', 'test_animals', 'test_breeding']
    
    def setUp(self):
        """Instantiate the test client."""
        self.client = Client()
    
    def tearDown(self):
        """Depopulate created model instances from test database."""
        for model in MODELS:
            for obj in model.objects.all():
                obj.delete()

    def test_create_breeding_minimal(self):
        """This is a test for creating a new breeding object, with only the minimum being entered."""
        new_breeding = Breeding(Strain = Strain.objects.get(pk=1))
        new_breeding.save()
	test_breeding = Breeding.objects.get(pk=2)
        self.assertEquals(test_breeding, new_breeding)
        self.assertEquals(test_breeding.__unicode__(), "test_strain Breeding Cage: None starting on None")

    def test_study_absolute_url(self):
        """This test verifies that the absolute url of a breeding object is set correctly."""
        test_breeding = Breeding.objects.get(pk=1)
        self.assertEquals(test_breeding.get_absolute_url(), '/breeding_cage/1/')

    def test_autoset_active_state(self):
        """This is a test for creating a new breeding object, with only the minimum being entered.  That object is then tested for the active state being automatically set when a End date is specified."""
        test_breeding = Breeding.objects.get(pk=1)
        self.assertEquals(test_breeding.Active, True)
        test_breeding.End = datetime.date.today()
        test_breeding.save()
        self.assertEquals(test_breeding.Active, False)

    def test_unweaned(self):
        """This is a test for the unweaned animal list.  It creates several animals for a breeding object and tests that they are tagged as unweaned.  They are then weaned and retested to be tagged as not unweaned.  This test is incomplete."""
        pass


class BreedingViewTests(TestCase):
    """These are tests for views based on Breeding objects.  Included are tests for breeding list (active and all), details, create, update and delete pages as well as for the timed mating lists."""
    fixtures = ['test_breeding', 'test_animals']

    def setUp(self):
        self.client = Client()
        self.test_user = User.objects.create_user('blah', 'blah@blah.com', 'blah')
        self.test_user.is_superuser = True
        self.test_user.is_active = True
        self.test_user.save()
        self.client.login(username='blah', password='blah')

    def tearDown(self):
        self.client.logout()
        self.test_user.delete()

    def test_breeding_list(self):
        """This test checks the view which displays a breeding list page.  It checks for the correct templates and status code."""        

        response = self.client.get('/breeding/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'jquery_script.html')
        self.assertTemplateUsed(response, 'jquery_ui_script_css.html')
        self.assertTemplateUsed(response, 'breeding_list.html')
        self.assertTemplateUsed(response, 'breeding_table.html')
        self.assertTemplateUsed(response, 'sortable_table_script.html')

    def test_breeding_list_all(self):
        """This test checks the view which displays a breeding list page, for all the cages.  It checks for the correct templates and status code."""
        response = self.client.get('/breeding/all/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'jquery_script.html')
        self.assertTemplateUsed(response, 'jquery_ui_script_css.html')
        self.assertTemplateUsed(response, 'breeding_list.html')
        self.assertTemplateUsed(response, 'breeding_table.html')
        self.assertTemplateUsed(response, 'sortable_table_script.html')

    def test_timed_mating_list(self):
        """This test checks the view which displays a breeding list page, for all the cages.  It checks for the correct templates and status code."""
        response = self.client.get('/breeding/timed_mating/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'jquery_script.html')
        self.assertTemplateUsed(response, 'jquery_ui_script_css.html')
        self.assertTemplateUsed(response, 'breeding_list.html')
        self.assertTemplateUsed(response, 'breeding_table.html')
        self.assertTemplateUsed(response, 'sortable_table_script.html')


    def test_breeding_new(self):
        """This test checks the view which displays a new breeding page.  It checks for the correct templates and status code."""
        response = self.client.get('/breeding/new/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'jquery_script.html')
        self.assertTemplateUsed(response, 'jquery_ui_script_css.html')
        self.assertTemplateUsed(response, 'breeding_form.html')


    def test_breeding_detail(self):
        """This test checks the view which displays a breeding detail page.  It checks for the correct templates and status code."""
        response = self.client.get('/breeding/1/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'jquery_script.html')
        self.assertTemplateUsed(response, 'jquery_ui_script_css.html')
        self.assertTemplateUsed(response, 'breeding_detail.html')

    def test_breeding_change(self):
        """This test checks the view which displays a breeding edit page.  It checks for the correct templates and status code."""
        response = self.client.get('/breeding/1/update/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'jquery_script.html')
        self.assertTemplateUsed(response, 'jquery_ui_script_css.html')
        self.assertTemplateUsed(response, 'breeding_form.html')


    def test_breeding_delete(self):
        """This test checks the view which displays a breeding detail page.  It checks for the correct templates and status code."""
        response = self.client.get('/breeding/1/delete/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'jquery_script.html')
        self.assertTemplateUsed(response, 'jquery_ui_script_css.html')
        self.assertTemplateUsed(response, 'confirm_delete.html')


