"""This file contains tests for the animal application.

These tests will verify generation and function of a new breeding, strain and animal object.
"""

import datetime

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User

from mousedb.animal.models import Animal, Strain, Breeding

MODELS = [Breeding, Animal, Strain]

class StrainModelTests(TestCase):
    """Tests the model attributes of Strain objects contained in the animal app."""

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
    
    def test_create_strain_minimal(self):
        """This is a test for creating a new strain object, with only the minimum fields being entered"""
        test_strain = Strain(Strain = "Test Strain", Strain_slug = "test-strain")
        test_strain.save()
        self.assertEquals(test_strain.id, 1)
        
    def test_create_strain_all(self):
        """This is a test for creating a new strain object, with only all fields being entered"""
        test_strain = Strain(
            Strain = "Test Strain", 
            Strain_slug = "test-strain",
            Source = "The test strain came from some place",
            Comments = "Here are some comments about the Test Strain")
        test_strain.save()
        self.assertEquals(test_strain.id, 1)
   
    def test_strain_unicode(self):
        """This is a test for creating a new strain object, then testing the unicode representation of the strain."""
        test_strain = Strain(Strain = "Test Strain", Strain_slug = "test-strain")
        test_strain.save()
        self.assertEquals(test_strain.__unicode__(), "Test Strain")
        
    def test_strain_absolute_url(self):
        """This is a test for creating a new strain object, then testing absolute url."""
        test_strain = Strain(Strain = "Test Strain", Strain_slug = "test-strain")
        test_strain.save()
        self.assertEquals(test_strain.get_absolute_url(), "/strain/test-strain")        

class StrainViewTests(TestCase):
    """Test the views contained in the animal app relating to Strain objects."""

    fixtures = ['test_strain',]

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

    def test_strain_list(self):
        """This tests the strain-list view, ensuring that templates are loaded correctly.  

        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        test_response = self.client.get('/strain/')
        self.assertEqual(test_response.status_code, 200)
        self.assertTrue('strain_list' in test_response.context)
        self.assertTrue('strain_list_alive' in test_response.context)          
        self.assertTrue('cages' in test_response.context)          
        self.assertTemplateUsed(test_response, 'base.html')
        self.assertTemplateUsed(test_response, 'jquery_script.html')
        self.assertTemplateUsed(test_response, 'jquery_ui_script_css.html')
        self.assertTemplateUsed(test_response, 'strain_list.html')
        self.assertTemplateUsed(test_response, 'sortable_table_script.html')
        self.assertEqual([strain.pk for strain in test_response.context['strain_list']], [1])        
        self.assertEqual([strain.Strain for strain in test_response.context['strain_list']], [u'Fixture Strain'])   
        self.assertEqual([strain.Strain_slug for strain in test_response.context['strain_list']], [u'fixture-strain'])


    def test_strain_detail(self):
        """This tests the strain-detail view, ensuring that templates are loaded correctly.  

        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        test_response = self.client.get('/strain/fixture-strain/')
        self.assertEqual(test_response.status_code, 200)
        self.assertTrue('strain' in test_response.context)        
        self.assertTrue('strain' in test_response.context)          
        self.assertTemplateUsed(test_response, 'base.html')
        self.assertTemplateUsed(test_response, 'jquery_script.html')
        self.assertTemplateUsed(test_response, 'jquery_ui_script_css.html')
        self.assertTemplateUsed(test_response, 'strain_detail.html')
        self.assertTemplateUsed(test_response, 'sortable_table_script.html')        
        self.assertTemplateUsed(test_response, 'animal_list_table.html')         
        self.assertEqual(test_response.context['strain'].pk, 1)
        self.assertEqual(test_response.context['strain'].Strain, u'Fixture Strain')
        self.assertEqual(test_response.context['strain'].Strain_slug, 'fixture-strain') 

        null_response = self.client.get('/strain/not-fixture-strain/')
        self.assertEqual(null_response.status_code, 404)  

    def test_strain_detail_all(self):
        """This tests the strain-detail-all view, ensuring that templates are loaded correctly.  

        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        test_response = self.client.get('/strain/fixture-strain/all/')
        self.assertEqual(test_response.status_code, 200)
        self.assertTrue('strain' in test_response.context)        
        self.assertTrue('strain' in test_response.context)          
        self.assertTemplateUsed(test_response, 'base.html')
        self.assertTemplateUsed(test_response, 'jquery_script.html')
        self.assertTemplateUsed(test_response, 'jquery_ui_script_css.html')
        self.assertTemplateUsed(test_response, 'strain_detail.html')
        self.assertTemplateUsed(test_response, 'sortable_table_script.html')        
        self.assertTemplateUsed(test_response, 'animal_list_table.html')         
        self.assertEqual(test_response.context['strain'].pk, 1)
        self.assertEqual(test_response.context['strain'].Strain, u'Fixture Strain')
        self.assertEqual(test_response.context['strain'].Strain_slug, 'fixture-strain') 

        null_response = self.client.get('/strain/not-fixture-strain/all/')
        self.assertEqual(null_response.status_code, 404)         


    def test_strain_new(self):
        """This tests the strain-new view, ensuring that templates are loaded correctly.  

        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        test_response = self.client.get('/strain/new/')
        self.assertEqual(test_response.status_code, 200)
        self.assertTemplateUsed(test_response, 'base.html')
        self.assertTemplateUsed(test_response, 'jquery_script.html')
        self.assertTemplateUsed(test_response, 'jquery_ui_script_css.html')
        self.assertTemplateUsed(test_response, 'strain_form.html')

    def test_strain_edit(self):
        """This tests the strain-edit view, ensuring that templates are loaded correctly.  

        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        test_response = self.client.get('/strain/1/edit/')
        self.assertEqual(test_response.status_code, 200)
        self.assertTrue('strain' in test_response.context)          
        self.assertTemplateUsed(test_response, 'base.html')
        self.assertTemplateUsed(test_response, 'jquery_script.html')
        self.assertTemplateUsed(test_response, 'jquery_ui_script_css.html')
        self.assertTemplateUsed(test_response, 'strain_form.html')
        self.assertEqual(test_response.context['strain'].pk, 1)
        self.assertEqual(test_response.context['strain'].Strain, u'Fixture Strain')
        self.assertEqual(test_response.context['strain'].Strain_slug, 'fixture-strain')  

        null_response = self.client.get('/strain/2/')
        self.assertEqual(null_response.status_code, 404)         

    def test_strain_delete(self):
        """This tests the strain-delete view, ensuring that templates are loaded correctly.  

        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        
        test_response = self.client.get('/strain/1/delete/')
        self.assertEqual(test_response.status_code, 200)
        self.assertTrue('object' in test_response.context)           
        self.assertTemplateUsed(test_response, 'base.html')
        self.assertTemplateUsed(test_response, 'jquery_script.html')
        self.assertTemplateUsed(test_response, 'jquery_ui_script_css.html')
        self.assertTemplateUsed(test_response, 'confirm_delete.html')
        self.assertEqual(test_response.context['object'].pk, 1)
        self.assertEqual(test_response.context['object'].Strain, u'Fixture Strain')
        self.assertEqual(test_response.context['object'].Strain_slug, 'fixture-strain')           
        
        null_response = self.client.get('/strain/2/delete/')
        self.assertEqual(null_response.status_code, 404) 

class AnimalModelTests(TestCase):
    """Tests the model attributes of Animal objects contained in the animal app."""

    fixtures = ['test_animals', 'test_strain']
    
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
        self.assertEquals(animal.__unicode__(), "Fixture Strain (2)")

    def test_animal_unicode(self):
        """This is a test for creating a new animal object, with only the minimum fields being entered.  It then tests that the correct unicode representation is being generated."""
        animal = Animal(Strain = Strain.objects.get(pk=1), Genotype="-/-", Background="Mixed")
        animal.save()
        animal_id = animal.id
        self.assertEquals(animal.__unicode__(), "Fixture Strain (2)")
        animal.MouseID = 1234
        animal.save()
        self.assertEquals(animal.__unicode__(), "Fixture Strain-EarTag #1234")
        
class AnimalViewTests(TestCase):
    """Tests the views associated with animal objects."""
    
    fixtures = ['test_animals','test_strain']

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
    
    def test_animal_list(self):
        """This test checks the view which displays a breeding list page showing active animals.  It checks for the correct templates and status code."""        

        response = self.client.get('/animal/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('animal_list' in response.context)    
        self.assertEqual(response.context['animal_list'].count(), 1)        
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'jquery_script.html')
        self.assertTemplateUsed(response, 'jquery_ui_script_css.html')
        self.assertTemplateUsed(response, 'animal_list.html')
        self.assertTemplateUsed(response, 'animal_list_table.html')
        self.assertTemplateUsed(response, 'sortable_table_script.html')
        self.assertEqual([animal.pk for animal in response.context['animal_list']][0], 1)        
        self.assertEqual([animal.Strain.Strain for animal in response.context['animal_list']][0], u'Fixture Strain')     
        self.assertEqual([animal.Cage for animal in response.context['animal_list']][0], 123456)
        self.assertEqual([animal.Born for animal in response.context['animal_list']][0], datetime.date(2011,01,01))
        self.assertEqual([animal.Background for animal in response.context['animal_list']][0], "Mixed")
        self.assertEqual([animal.Genotype for animal in response.context['animal_list']][0], "-/-")        

    def test_animal_list_all(self):
        """This test checks the view which displays a breeding list page showing all animals.  It checks for the correct templates and status code."""        

        response = self.client.get('/animal/all/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('animal_list' in response.context)    
        self.assertEqual(response.context['animal_list'].count(), 1)        
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'jquery_script.html')
        self.assertTemplateUsed(response, 'jquery_ui_script_css.html')
        self.assertTemplateUsed(response, 'animal_list.html')
        self.assertTemplateUsed(response, 'animal_list_table.html')
        self.assertTemplateUsed(response, 'sortable_table_script.html')
        self.assertEqual([animal.pk for animal in response.context['animal_list']][0], 1)        
        self.assertEqual([animal.Strain.Strain for animal in response.context['animal_list']][0], u'Fixture Strain')     
        self.assertEqual([animal.Cage for animal in response.context['animal_list']][0], 123456)
        self.assertEqual([animal.Born for animal in response.context['animal_list']][0], datetime.date(2011,01,01))
        self.assertEqual([animal.Background for animal in response.context['animal_list']][0], "Mixed")
        self.assertEqual([animal.Genotype for animal in response.context['animal_list']][0], "-/-")  

    def test_animal_detail(self):
        """This tests the animal-detail view, ensuring that templates are loaded correctly.  

        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        test_response = self.client.get('/animal/1')
        self.assertEqual(test_response.status_code, 200)
        self.assertTrue('animal' in test_response.context)        
        self.assertTemplateUsed(test_response, 'base.html')
        self.assertTemplateUsed(test_response, 'jquery_script.html')
        self.assertTemplateUsed(test_response, 'jquery_ui_script_css.html')
        self.assertTemplateUsed(test_response, 'animal_detail.html')
        self.assertTemplateUsed(test_response, 'sortable_table_script.html')        
        self.assertEqual(test_response.context['animal'].pk, 1)
        self.assertEqual(test_response.context['animal'].Born, datetime.date(2011,01,01))
        self.assertEqual(test_response.context['animal'].Cage, 123456) 
        self.assertEqual(test_response.context['animal'].Background, "Mixed") 
        self.assertEqual(test_response.context['animal'].Genotype, "-/-") 
        self.assertEqual(test_response.context['animal'].Strain.Strain, "Fixture Strain")         

        null_response = self.client.get('/animal/999')
        self.assertEqual(null_response.status_code, 404)  
        
    def test_animal_new(self):
        """This test checks the view which displays a new animal.  
        
        It checks for the correct templates and status code."""
        
        test_response = self.client.get('/animal/new')
        self.assertEqual(test_response.status_code, 200)
        self.assertTemplateUsed(test_response, 'base.html')
        self.assertTemplateUsed(test_response, 'jquery_script.html')
        self.assertTemplateUsed(test_response, 'jquery_ui_script_css.html')
        self.assertTemplateUsed(test_response, 'animal_form.html')  

    def test_animal_edit(self):
        """This test checks the view which displays a animal edit page.  
        
        It checks for the correct templates and status code and that the animal is passed correctly to the context."""
        
        test_response = self.client.get('/animal/1/edit')
        self.assertEqual(test_response.status_code, 200)
        self.assertTrue('animal' in test_response.context)           
        self.assertTemplateUsed(test_response, 'base.html')
        self.assertTemplateUsed(test_response, 'jquery_script.html')
        self.assertTemplateUsed(test_response, 'jquery_ui_script_css.html')
        self.assertTemplateUsed(test_response, 'animal_form.html')
        self.assertEqual(test_response.context['animal'].pk, 1)
        self.assertEqual(test_response.context['animal'].Born, datetime.date(2011,01,01))
        self.assertEqual(test_response.context['animal'].Cage, 123456) 
        self.assertEqual(test_response.context['animal'].Background, "Mixed") 
        self.assertEqual(test_response.context['animal'].Genotype, "-/-") 
        self.assertEqual(test_response.context['animal'].Strain.Strain, "Fixture Strain")           

        #Checks that an incorrect animal number givs a 404 error.
        null_response = self.client.get('/animal/999/edit')
        self.assertEqual(null_response.status_code, 404)          

    def test_animal_delete(self):
        """This test checks the view which displays an animal deletion page.  
        
        It checks for the correct templates and status code and that the animal is passed correctly to the context."""
        
        test_response = self.client.get('/animal/1/delete')
        self.assertEqual(test_response.status_code, 200)
        self.assertTrue('animal' in test_response.context)           
        self.assertTemplateUsed(test_response, 'base.html')
        self.assertTemplateUsed(test_response, 'jquery_script.html')
        self.assertTemplateUsed(test_response, 'jquery_ui_script_css.html')
        self.assertTemplateUsed(test_response, 'confirm_delete.html')
        self.assertEqual(test_response.context['animal'].pk, 1)
        self.assertEqual(test_response.context['animal'].Born, datetime.date(2011,01,01))
        self.assertEqual(test_response.context['animal'].Cage, 123456) 
        self.assertEqual(test_response.context['animal'].Background, "Mixed") 
        self.assertEqual(test_response.context['animal'].Genotype, "-/-") 
        self.assertEqual(test_response.context['animal'].Strain.Strain, "Fixture Strain")           
        
        #Checks that an incorrect animal number gives a 404 error.
        null_response = self.client.get('/animal/999/delete')
        self.assertEqual(null_response.status_code, 404)         
        
class BreedingModelTests(TestCase):
    """Tests the model attributes of Breeding objects contained in the animal app."""

    fixtures = ['test_group', 'test_animals', 'test_breeding', 'test_strain']
    
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
        test_breeding = Breeding(Strain = Strain.objects.get(pk=1))
        test_breeding.save()
        self.assertEquals(test_breeding.pk,  4)

    def test_study_absolute_url(self):
        """This test verifies that the absolute url of a breeding object is set correctly."""
        test_breeding = Breeding.objects.get(pk=1)
        self.assertEquals(test_breeding.get_absolute_url(), '/breeding_cage/1')
        
    def test_duration(self):
        """This test verifies that the duration is set correctly."""
        test_breeding = Breeding.objects.get(pk=1)
        calculated_duration = datetime.date.today() - test_breeding.Start
        self.assertEquals(test_breeding.duration(), calculated_duration.days )        

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
    fixtures = ['test_breeding', 'test_animals', 'test_strain']

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
        """This test checks the view which displays a breeding list page showing active breeding cages.  It checks for the correct templates and status code."""        

        response = self.client.get('/breeding/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('breeding_list' in response.context)    
        self.assertEqual(response.context['breeding_list'].count(), 2)        
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'jquery_script.html')
        self.assertTemplateUsed(response, 'jquery_ui_script_css.html')
        self.assertTemplateUsed(response, 'breeding_list.html')
        self.assertTemplateUsed(response, 'breeding_table.html')
        self.assertTemplateUsed(response, 'sortable_table_script.html')
        self.assertEqual([breeding.pk for breeding in response.context['breeding_list']][0], 1)        
        self.assertEqual([breeding.Strain.Strain for breeding in response.context['breeding_list']][0], u'Fixture Strain')     
        self.assertEqual([breeding.Cage for breeding in response.context['breeding_list']][0], u'12345')
     

    def test_breeding_list_all(self):
        """This test checks the view which displays a breeding list page, for all the cages.  It checks for the correct templates and status code."""
        
        response = self.client.get('/breeding/all')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('breeding_list' in response.context)  
        self.assertEqual(response.context['breeding_list'].count(), 3)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'jquery_script.html')
        self.assertTemplateUsed(response, 'jquery_ui_script_css.html')
        self.assertTemplateUsed(response, 'breeding_list.html')
        self.assertTemplateUsed(response, 'breeding_table.html')
        self.assertTemplateUsed(response, 'sortable_table_script.html')
        self.assertEqual([breeding.pk for breeding in response.context['breeding_list']][0], 3)        
        self.assertEqual([breeding.Strain.Strain for breeding in response.context['breeding_list']][0], u'Fixture Strain')     
        self.assertEqual([breeding.Cage for breeding in response.context['breeding_list']][0], u'111111')        

    def test_timed_mating_list(self):
        """This test checks the view which displays a breeding list page, for all the cages.  It checks for the correct templates and status code."""
        
        response = self.client.get('/breeding/timed_mating')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('breeding_list' in response.context) 
        self.assertEqual(response.context['breeding_list'].count(), 1)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'jquery_script.html')
        self.assertTemplateUsed(response, 'jquery_ui_script_css.html')
        self.assertTemplateUsed(response, 'breeding_list.html')
        self.assertTemplateUsed(response, 'breeding_table.html')
        self.assertTemplateUsed(response, 'sortable_table_script.html')
        self.assertEqual([breeding.pk for breeding in response.context['breeding_list']][0], 3)        
        self.assertEqual([breeding.Strain.Strain for breeding in response.context['breeding_list']][0], u'Fixture Strain')     
        self.assertEqual([breeding.Cage for breeding in response.context['breeding_list']][0], u'111111')
        self.assertEqual([breeding.Start for breeding in response.context['breeding_list']][0], datetime.date(1978, 12, 24))  


    def test_breeding_new(self):
        """This test checks the view which displays a new breeding page.  It checks for the correct templates and status code."""
        response = self.client.get('/breeding/new')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'jquery_script.html')
        self.assertTemplateUsed(response, 'jquery_ui_script_css.html')
        self.assertTemplateUsed(response, 'breeding_form.html')


    def test_breeding_detail(self):
        """This test checks the view which displays a breeding detail page.  It checks for the correct templates and status code."""
        response = self.client.get('/breeding/1')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('breeding' in response.context)        
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'jquery_script.html')
        self.assertTemplateUsed(response, 'jquery_ui_script_css.html')
        self.assertTemplateUsed(response, 'breeding_detail.html')
        self.assertTemplateUsed(response, 'sortable_table_script.html')    
        self.assertEqual(response.context['breeding'].pk, 1)
        self.assertEqual(response.context['breeding'].Strain.Strain, u'Fixture Strain')
        self.assertEqual(response.context['breeding'].Cage, '12345') 

        null_response = self.client.get('/breeding/999')
        self.assertEqual(null_response.status_code, 404)          

    def test_breeding_edit(self):
        """This test checks the view which displays a breeding edit page.  It checks for the correct templates and status code."""
        
        response = self.client.get('/breeding/1/edit')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('breeding' in response.context)           
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'jquery_script.html')
        self.assertTemplateUsed(response, 'jquery_ui_script_css.html')
        self.assertTemplateUsed(response, 'breeding_form.html')
        self.assertEqual(response.context['breeding'].pk, 1)
        self.assertEqual(response.context['breeding'].Strain.Strain, u'Fixture Strain')
        self.assertEqual(response.context['breeding'].Cage, '12345')         
        
        null_response = self.client.get('/breeding/999/edit')
        self.assertEqual(null_response.status_code, 404)          


    def test_breeding_delete(self):
        """This test checks the view which displays a breeding detail page.  It checks for the correct templates and status code."""
        
        response = self.client.get('/breeding/1/delete')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('breeding' in response.context)           
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'jquery_script.html')
        self.assertTemplateUsed(response, 'jquery_ui_script_css.html')
        self.assertTemplateUsed(response, 'confirm_delete.html')
        self.assertEqual(response.context['breeding'].pk, 1)
        self.assertEqual(response.context['breeding'].Strain.Strain, u'Fixture Strain')
        self.assertEqual(response.context['breeding'].Cage, '12345')         
        
        null_response = self.client.get('/breeding/999/delete')
        self.assertEqual(null_response.status_code, 404)           
		
class CageViewTests(TestCase):
    """These are tests for views based on animal objects as directed by cage urls.  Included are tests for cage-list, cage-list-all and cage-detail"""
    fixtures = ['test_animals', 'test_strain']

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

    def test_cage_list(self):
        """This test checks the view which displays a cage list page for active animals.  It checks for the correct templates and status code."""        

        response = self.client.get('/cage/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'jquery_script.html')
        self.assertTemplateUsed(response, 'jquery_ui_script_css.html')
        self.assertTemplateUsed(response, 'sortable_table_script.html')		
        self.assertTemplateUsed(response, 'cage_list.html')
		
    def test_cage_list(self):
        """This test checks the view which displays a cage list page showing all animals.  It checks for the correct templates and status code."""        

        response = self.client.get('/cage/all')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'jquery_script.html')
        self.assertTemplateUsed(response, 'jquery_ui_script_css.html')
        self.assertTemplateUsed(response, 'sortable_table_script.html')
        self.assertTemplateUsed(response, 'cage_list.html')		

    def test_cage_detail(self):
        """This test checks the view which displays a animal list page showing all animals with a specified cage number.  It checks for the correct templates and status code."""        

        response = self.client.get('/cage/123456/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'jquery_script.html')
        self.assertTemplateUsed(response, 'jquery_ui_script_css.html')
        self.assertTemplateUsed(response, 'sortable_table_script.html')
        self.assertTemplateUsed(response, 'animal_list.html')				
        self.assertTemplateUsed(response, 'animal_list_table.html')	
		
class DateViewTests(TestCase):
    """These are tests for views based on animal objects as directed by date based urls.  Included are tests for archive-home, archive-month and archive-year"""
    fixtures = ['test_animals', 'test_strain']

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

    def test_archive_home(self):
        """This test checks the view which displays a summary of the birthdates of animals.  It checks for the correct templates and status code."""        

        response = self.client.get('/date/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'jquery_script.html')
        self.assertTemplateUsed(response, 'jquery_ui_script_css.html')
        self.assertTemplateUsed(response, 'sortable_table_script.html')
        self.assertTemplateUsed(response, 'animal_archive.html')		
		
    def test_archive_year(self):
        """This test checks the view which displays a list of the animals, filtered by year.  It checks for the correct templates and status code."""        

        response = self.client.get('/date/2011/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('animal_list' in response.context)  
        self.assertEqual(response.context['animal_list'].count(), 1)        
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'jquery_script.html')
        self.assertTemplateUsed(response, 'jquery_ui_script_css.html')
        self.assertTemplateUsed(response, 'animal_list.html')
        self.assertTemplateUsed(response, 'animal_list_table.html')
        self.assertTemplateUsed(response, 'sortable_table_script.html')
        self.assertEqual([animal.pk for animal in response.context['animal_list']][0], 1)        
        self.assertEqual([animal.Strain.Strain for animal in response.context['animal_list']][0], u'Fixture Strain')     
        self.assertEqual([animal.Cage for animal in response.context['animal_list']][0], 123456)
        self.assertEqual([animal.Born for animal in response.context['animal_list']][0], datetime.date(2011,01,01))
        self.assertEqual([animal.Background for animal in response.context['animal_list']][0], "Mixed")
        self.assertEqual([animal.Genotype for animal in response.context['animal_list']][0], "-/-")    
		
    def test_archive_month(self):
        """This test checks the view which displays a list of the animals, filtered by month.  It checks for the correct templates and status code."""        

        response = self.client.get('/date/2011/01/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('animal_list' in response.context)  
        self.assertEqual(response.context['animal_list'].count(), 1)        
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'jquery_script.html')
        self.assertTemplateUsed(response, 'jquery_ui_script_css.html')
        self.assertTemplateUsed(response, 'animal_list.html')
        self.assertTemplateUsed(response, 'animal_list_table.html')
        self.assertTemplateUsed(response, 'sortable_table_script.html')
        self.assertEqual([animal.pk for animal in response.context['animal_list']][0], 1)        
        self.assertEqual([animal.Strain.Strain for animal in response.context['animal_list']][0], u'Fixture Strain')     
        self.assertEqual([animal.Cage for animal in response.context['animal_list']][0], 123456)
        self.assertEqual([animal.Born for animal in response.context['animal_list']][0], datetime.date(2011,01,01))
        self.assertEqual([animal.Background for animal in response.context['animal_list']][0], "Mixed")
        self.assertEqual([animal.Genotype for animal in response.context['animal_list']][0], "-/-")  	

