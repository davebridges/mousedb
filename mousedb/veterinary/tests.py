"""
This package contains the unit tests for the :mod:`~mousedb.veterinary` app.


There are tests for each of the three models in this app.
"""
import datetime

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User

from mousedb.veterinary.models import MedicalIssue, MedicalCondition, MedicalTreatment
from mousedb.animal.models import Animal

MODELS = [MedicalIssue, MedicalCondition, MedicalTreatment]

class MedicalIssueTests(TestCase):
    '''This class tests various aspects of the :class:`~mousedb.veterinary.models.MedicalIssue` model.'''

    fixtures = ['test_medical_condition', 'test_medical_treatment', 'test_animals', 'test_strain']

    def setUp(self):
        '''Instantiate the test client.  Creates a test user.'''
        self.client = Client()
        self.test_user = User.objects.create_user('testuser', 'blah@blah.com', 'testpassword')
        self.test_user.is_superuser = True
        self.test_user.is_active = True
        self.test_user.save()
        self.assertEqual(self.test_user.is_superuser, True)
        login = self.client.login(username='testuser', password='testpassword')
        self.failUnless(login, 'Could not log in')
    
    def tearDown(self):
        '''Depopulate created model instances from test database.'''
        for model in MODELS:
            for obj in model.objects.all():
                obj.delete()
                
    def test_create_new_medicalissue_minimum(self):
        '''This test creates a :class:`~mousedb.veterinary.models.MedicalIssue` with the required information only.'''

        test_medical_issue = MedicalIssue(animal= Animal.objects.get(pk=1),
        	condition = MedicalCondition.objects.get(pk=1)) 
        test_medical_issue.save()
        self.assertEqual(test_medical_issue.pk, 1) #presumes one model loaded in fixture data
        
    def test_create_new_medicalissue_all(self):
        '''This test creates a :class:`~mousedb.veterinary.models.MedicalIssue` with all information entered.'''

        test_medical_issue = MedicalIssue(animal= Animal.objects.get(pk=1),
        	condition = MedicalCondition.objects.get(pk=1),
        	treatment = MedicalTreatment.objects.get(pk=1),
        	diagnosis = datetime.date.today(),
        	treatment_start = datetime.date.today(),
        	treatment_end = datetime.date.today(),) 
        test_medical_issue.save() 
        self.assertEqual(test_medical_issue.pk, 1) #presumes one model loaded in fixture data       
        
    def test_medicalissue_unicode(self):
        '''This tests the unicode representation of a :class:`~mousedb.veterinary.models.MedicalIssue`.'''

        test_medical_issue = MedicalIssue(animal= Animal.objects.get(pk=1),
        	condition = MedicalCondition.objects.get(pk=1)) 
        test_medical_issue.save()
        self.assertEqual(test_medical_issue.__unicode__(), "Fixture Strain (1) - Test Condition") 
        
    def test_medicalissue_absolute_url(self):
        '''This tests the absolute_url generation of a :class:`~mousedb.veterinary.models.MedicalIssue`.'''

        test_medical_issue = MedicalIssue(animal= Animal.objects.get(pk=1),
        	condition = MedicalCondition.objects.get(pk=1)) 
        test_medical_issue.save()
        self.assertEqual(test_medical_issue.get_absolute_url(), "/veterinary/medical-issue/2/") #where the url should be 

class MedicalConditionTests(TestCase):
    '''This class tests various aspects of the :class:`~mousedb.veterinary.models.MedicalCondition` model.'''

    def setUp(self):
        '''Instantiate the test client.  Creates a test user.'''
        self.client = Client()
        self.test_user = User.objects.create_user('testuser', 'blah@blah.com', 'testpassword')
        self.test_user.is_superuser = True
        self.test_user.is_active = True
        self.test_user.save()
        self.assertEqual(self.test_user.is_superuser, True)
        login = self.client.login(username='testuser', password='testpassword')
        self.failUnless(login, 'Could not log in')
    
    def tearDown(self):
        '''Depopulate created model instances from test database.'''
        for model in MODELS:
            for obj in model.objects.all():
                obj.delete()
                
    def test_create_new_medical_condition_minimum(self):
        '''This test creates a :class:`~mousedb.veterinary.models.MedicalCondition` with the required information only.'''

        test_medical_condition = MedicalCondition(name = "Test Condition") 
        test_medical_condition.save()
        self.assertEqual(test_medical_condition.pk, 1) #presumes one model loaded in fixture data
        
    def test_create_new_medical_condition_all(self):
        '''This test creates a :class:`~mousedb.veterinary.models.MedicalCondition` with all information entered.'''

        test_medical_condition = MedicalCondition(name = "Test Condition",
        	notes = "Some notes about the test condition.") 
        test_medical_condition.save() 
        self.assertEqual(test_medical_condition.pk, 1) #presumes one model loaded in fixture data       
        
    def test_medical_condition_unicode(self):
        '''This tests the unicode representation of a :class:`~mousedb.veterinary.models.MedicalCondition`.'''

        test_medical_condition = MedicalCondition(name = "Test Condition") 
        test_medical_condition.save()
        self.assertEqual(test_medical_condition.__unicode__(), "Test Condition")
        
    def test_medical_condition_name_slug(self):
        '''This tests the slug field generation of a :class:`~mousedb.veterinary.models.MedicalCondition`.'''

        test_medical_condition = MedicalCondition(name = "Test Condition") 
        test_medical_condition.save()
        self.assertEqual(test_medical_condition.slug, "test-condition")  
        
    def test_medical_condition_absolute_url(self):
        '''This tests the absolute_url generation of a :class:`~mousedb.veterinary.models.MedicalCondition`.'''

        test_medical_condition = MedicalCondition(name = "Test Condition")  
        test_medical_condition.save()
        self.assertEqual(test_medical_condition.get_absolute_url(), "/veterinary/medical-condition/test-condition/") #where the url should be 
        
class MedicalTreatmentTests(TestCase):
    '''This class tests various aspects of the :class:`~mousedb.veterinary.models.MedicalTreatment` model.'''

    def setUp(self):
        '''Instantiate the test client.  Creates a test user.'''
        self.client = Client()
        self.test_user = User.objects.create_user('testuser', 'blah@blah.com', 'testpassword')
        self.test_user.is_superuser = True
        self.test_user.is_active = True
        self.test_user.save()
        self.assertEqual(self.test_user.is_superuser, True)
        login = self.client.login(username='testuser', password='testpassword')
        self.failUnless(login, 'Could not log in')
    
    def tearDown(self):
        '''Depopulate created model instances from test database.'''
        for model in MODELS:
            for obj in model.objects.all():
                obj.delete()
                
    def test_create_new_medical_treatment_minimum(self):
        '''This test creates a :class:`~mousedb.veterinary.models.MedicalTreatment` with the required information only.'''

        test_medical_treatment = MedicalTreatment(name = "Test Treatment") 
        test_medical_treatment.save()
        self.assertEqual(test_medical_treatment.pk, 1) #presumes one model loaded in fixture data
        
    def test_create_new_test_medical_treatment_all(self):
        '''This test creates a :class:`~mousedb.veterinary.models.MedicalTreatment` with all information entered.'''

        test_medical_treatment = MedicalTreatment(name = "Test Treatment") 
        test_medical_treatment.save() 
        self.assertEqual(test_medical_treatment.pk, 1) #presumes one model loaded in fixture data       
        
    def test_test_medical_treatment_unicode(self):
        '''This tests the unicode representation of a :class:`~mousedb.veterinary.models.MedicalTreatment`.'''

        test_medical_treatment = MedicalTreatment(name = "Test Treatment") 
        test_medical_treatment.save()
        self.assertEqual(test_medical_treatment.__unicode__(), "Test Treatment")
        
    def test_test_medical_treatment_name_slug(self):
        '''This tests the slug field generation of a :class:`~mousedb.veterinary.models.MedicalTreatment`.'''

        test_medical_treatment = MedicalTreatment(name = "Test Treatment") 
        test_medical_treatment.save()
        self.assertEqual(test_medical_treatment.slug, "test-treatment")  
        
    def test_test_medical_treatment_absolute_url(self):
        '''This tests the absolute_url generation of a :class:`~mousedb.veterinary.models.MedicalTreatment`.'''

        test_medical_treatment = MedicalTreatment(name = "Test Treatment")  
        test_medical_treatment.save()
        self.assertEqual(test_medical_treatment.get_absolute_url(), "/veterinary/medical-treatment/test-treatment/") #where the url should be         