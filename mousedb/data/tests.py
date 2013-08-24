"""This file contains tests for the data application.

These tests will verify generation of new experiment, measurement, assay, researcher, study, treatment, vendor, diet, environment, implantation, transplantation and pharnaceutical objects.
"""
import datetime

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User

from mousedb.data.models import Study, Diet, Environment, Researcher, Treatment, Transplantation, Pharmaceutical, Implantation, Vendor, Cohort
from mousedb.animal.models import Strain, Animal

MODELS = [Study]

class BasicTestCase(TestCase):
    '''This class factors out the TestcCase setup and Teardown code.'''

    def setUp(self):
        """Instantiate the test client."""
        self.client = Client()
        self.test_user = User.objects.create_user('blah', 'blah@blah.com', 'blah')
        self.test_user.is_superuser = True
        self.test_user.is_active = True
        self.test_user.save()
        self.client.login(username='blah', password='blah')

    def tearDown(self):
        """Depopulate created model instances from test database."""
        for model in MODELS:
            for obj in model.objects.all():
                obj.delete()

class StudyModelTests(BasicTestCase):
    """Test the creation and modification of Study objects."""

    def test_create_study_minimal(self):
        """This is a test for creating a new study object, with only the minimum being entered.  It also verifies that unicode is set correctly."""
        new_study = Study(description = "Effects of x on y")
        new_study.save()
        self.assertEquals(new_study.__unicode__(), u'Effects of x on y')

    def test_create_studey_detailed(self):
        """This is a test for creating a new study object, with all fields being entered.  It also verifies that unicode is set correctly.  This test is dependent on the ability to create a new Strain object (see animal.tests.StrainModelTests.test_create_minimal_strain)."""
        new_study = Study(
            description = "Effects of x on y",
            start_date = datetime.date.today(),
            stop_date = datetime.date.today(),
            notes = "some notes on this strain"
            )
        new_study.save()
        new_study.strain.create(Strain='test_strain')
        self.assertEquals(new_study.__unicode__(), u'Effects of x on y')

    def test_study_absolute_url(self):
        """This test verifies that the absolute url of a study object is set correctly.  This study is dependend on a positive result on test_create_study_minimal."""
        test_study = Study(description = "Effects of x on y")
        test_study.save()
        self.assertEquals(test_study.get_absolute_url(), '/studies/1/')

class StudyViewTests(BasicTestCase):
    """These tests test the views associated with Study objects."""

    fixtures = ['test_study',]

    def test_study_list(self):
        """This test checks the status code, and templates for study lists."""
        response = self.client.get('/study/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'jquery_script.html')
        self.assertTemplateUsed(response, 'jquery_ui_script_css.html')
        self.assertTemplateUsed(response, 'study_list.html')

    def test_study_detail(self):
        """This test checks the view which displays a study detail page.  It checks for the correct templates and status code."""
        response = self.client.get('/study/1/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'jquery_script.html')
        self.assertTemplateUsed(response, 'jquery_ui_script_css.html')
        self.assertTemplateUsed(response, 'study_detail.html')
        self.assertTemplateUsed(response, 'experiment_list_table.html')

    def test_study_new(self):
        """This test checks the view which displays a study creation page.  It checks for the correct templates and status code."""
        response = self.client.get('/study/new/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'jquery_script.html')
        self.assertTemplateUsed(response, 'jquery_ui_script_css.html')
        self.assertTemplateUsed(response, 'study_form.html')

    def test_study_edit(self):
        """This test checks the view which displays a study edit page.  It checks for the correct templates and status code."""
        response = self.client.get('/study/1/edit/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'jquery_script.html')
        self.assertTemplateUsed(response, 'jquery_ui_script_css.html')
        self.assertTemplateUsed(response, 'study_form.html')


    def test_study_delete(self):
        """This test checks the view which displays a study detail page.  It checks for the correct templates and status code."""
        response = self.client.get('/study/1/delete/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'jquery_script.html')
        self.assertTemplateUsed(response, 'jquery_ui_script_css.html')
        self.assertTemplateUsed(response, 'confirm_delete.html')
				
class TreatmentModelTests(BasicTestCase):
    '''These tests test the functionality of :class:`~mousedb.data.models.Treatment` objects.'''
    
    fixtures = ['test_diet', 'test_environment', 'test_researcher', 
    'test_animals', 'test_strain', 'test_vendor', 'test_study', 'test_transplantation',
    'test_pharmaceutical','test_implantation']
    
    def test_create_treatment_minimum(self):
        '''This test creates a :class:`~mousedb.data.models.Treatment` with the required information only.'''

        test_treatment = Treatment(treatment = 'Test Treatment', 
            diet = Diet.objects.get(pk=1),
            environment = Environment.objects.get(pk=1))
        test_treatment.save()
        test_treatment.animals.add(Animal.objects.get(pk=1))
        test_treatment.researchers.add(Researcher.objects.get(pk=1))
        self.assertEqual(test_treatment.pk, 1) #presumes no models loaded in fixture data
        
    def test_create_treatment_all(self):
        '''This test creates a :class:`~mousedb.data.models.Treatment` with all information entered.'''

        test_treatment = Treatment(treatment = 'Test Treatment', 
            diet = Diet.objects.get(pk=1),
            environment = Environment.objects.get(pk=1),
            study = Study.objects.get(pk=1),
            transplantation = Transplantation.objects.get(pk=1),
            notes = "Some notes about this test treatment."
            )
        test_treatment.save()
        test_treatment.animals.add(Animal.objects.get(pk=1))
        test_treatment.researchers.add(Researcher.objects.get(pk=1))
        test_treatment.pharmaceutical.add(Pharmaceutical.objects.get(pk=1))  
        test_treatment.implantation.add(Implantation.objects.get(pk=1))                
        self.assertEqual(test_treatment.pk, 1) #presumes no models loaded in fixture data       
        
    def test_treatment_unicode(self):
        '''This tests the unicode representation of a :class:`~mousedb.data.models.Treatment`.'''

        test_treatment = Treatment(treatment = 'Test Treatment', 
            diet = Diet.objects.get(pk=1),
            environment = Environment.objects.get(pk=1))
        test_treatment.save()
        test_treatment.animals.add(Animal.objects.get(pk=1))
        test_treatment.researchers.add(Researcher.objects.get(pk=1))
        self.assertEqual(test_treatment.__unicode__(), "Test Treatment")  
        
    def test_treatment_absolute_url(self):
        '''This tests the absolute_url generation of a :class:`~mousedb.data.models.Treatment`.'''

        test_treatment = Treatment(treatment = 'Test Treatment', 
            diet = Diet.objects.get(pk=1),
            environment = Environment.objects.get(pk=1))
        test_treatment.save()
        test_treatment.animals.add(Animal.objects.get(pk=1))
        test_treatment.researchers.add(Researcher.objects.get(pk=1))
        self.assertEqual(test_treatment.get_absolute_url(), "/treatment/1")

class TreatmentViewTests(BasicTestCase):
    """These tests test the views associated with Treatment objects."""

    fixtures = ['test_treatment','test_study', 'test_diet', 'test_environment', 'test_vendor']

    def test_treatment_detail(self):
        """This test checks the view which displays a treatment-detail page.  
        
        It checks for the correct templates and status code."""        

        test_response = self.client.get('/treatment/1/')
        self.assertEqual(test_response.status_code, 200)
        self.assertTrue('treatment' in test_response.context)            
        
        #test templates
        self.assertTemplateUsed(test_response, 'base.html')
        self.assertTemplateUsed(test_response, 'jquery_script.html')
        self.assertTemplateUsed(test_response, 'jquery_ui_script_css.html')
        self.assertTemplateUsed(test_response, 'treatment_detail.html')
        self.assertTemplateUsed(test_response, 'sortable_table_script.html')
        self.assertTemplateUsed(test_response, 'menu_script.html')              
        
        #test object attributes
        self.assertEqual(test_response.context['treatment'].pk, 1)
        self.assertEqual(test_response.context['treatment'].treatment, u'Test Treatment')
        self.assertEqual(test_response.context['treatment'].notes, u'Some Notes')
        self.assertEqual(test_response.context['treatment'].diet.__unicode__(), u'Test Diet')
        
        #test that an incorrect id gives a 404
        wrong_test_response = self.client.get('/treatment/101/')
        self.assertEqual(wrong_test_response.status_code, 404)
        
    def test_treatment_list(self):
        """This tests the treatment-list view, ensuring that templates are loaded correctly.  

        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        
        test_response = self.client.get('/treatment/')
        self.assertEqual(test_response.status_code, 200)
        self.assertTrue('treatment_list' in test_response.context) 

        #test templates
        self.assertTemplateUsed(test_response, 'base.html')
        self.assertTemplateUsed(test_response, 'jquery_script.html')
        self.assertTemplateUsed(test_response, 'jquery_ui_script_css.html')
        self.assertTemplateUsed(test_response, 'treatment_list.html')
        self.assertTemplateUsed(test_response, 'menu_script.html')        

        #test object attributes
        self.assertEqual(test_response.context['treatment_list'][0].pk, 1)
        self.assertEqual(test_response.context['treatment_list'][0].treatment, u'Test Treatment')
        self.assertEqual(test_response.context['treatment_list'][0].notes, u'Some Notes')
        self.assertEqual(test_response.context['treatment_list'][0].diet.__unicode__(), u'Test Diet')
        
class PharmaceuticalModelTests(BasicTestCase):
    '''These tests test the functionality of :class:`~mousedb.data.models.Pharmaceutical` objects.'''
    
    fixtures = ['test_vendor',]
    
    def test_create_pharmaceutical_minimum(self):
        '''This test creates a :class:`~mousedb.data.models.Pharmaceutical` with the required information only.'''

        test_pharmaceutical = Pharmaceutical(drug = 'Test Drug', 
            dose = '1 mg/kg',
            mode = 'Oral',
            recurrance = 'Daily',
            vendor = Vendor.objects.get(pk=1))
        test_pharmaceutical.save()
        self.assertEqual(test_pharmaceutical.pk, 1) #presumes no models loaded in fixture data
        
    def test_create_pharmaceutical_all(self):
        '''This test creates a :class:`~mousedb.data.models.Pharmaceutical` with all information entered.'''

        test_pharmaceutical = Pharmaceutical(drug = 'Test Drug', 
            dose = '1 mg/kg',
            mode = 'Oral',
            recurrance = 'Daily',
            vendor = Vendor.objects.get(pk=1))
        test_pharmaceutical.save()
        self.assertEqual(test_pharmaceutical.pk, 1) #presumes no models loaded in fixture data      
        
    def test_pharmaceutical_unicode(self):
        '''This tests the unicode representation of a :class:`~mousedb.data.models.Pharmaceutical`.'''

        test_pharmaceutical = Pharmaceutical(drug = 'Test Drug', 
            dose = '1 mg/kg',
            mode = 'Oral',
            recurrance = 'Daily',
            vendor = Vendor.objects.get(pk=1))
        test_pharmaceutical.save()
        self.assertEqual(test_pharmaceutical.__unicode__(), "Test Drug at 1 mg/kg, Daily")  
        
    def test_pharmaceutical_absolute_url(self):
        '''This tests the absolute_url generation of a :class:`~mousedb.data.models.Pharmaceutical`.'''

        test_pharmaceutical = Pharmaceutical(drug = 'Test Drug', 
            dose = '1 mg/kg',
            mode = 'Oral',
            recurrance = 'Daily',
            vendor = Vendor.objects.get(pk=1))
        test_pharmaceutical.save()
        self.assertEqual(test_pharmaceutical.get_absolute_url(), "/parameter/pharmaceutical/1")
                
class PharmaceuticalViewTests(BasicTestCase):
    '''This class tests the views for :class:`~mousedb.data.models.Pharmaceutical` objects.'''

    fixtures = ['test_pharmaceutical', 'test_vendor']

    def test_pharmaceutical_list(self):
        """This tests the pharmaceutical-list view, ensuring that templates are loaded correctly.  

        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        
        test_response = self.client.get('/parameter/pharmaceutical')
        self.assertEqual(test_response.status_code, 200)
        self.assertTrue('pharmaceutical_list' in test_response.context)      
        self.assertTemplateUsed(test_response, 'pharmaceutical_list.html')
        self.assertEqual(test_response.context['pharmaceutical_list'][0].pk, 1)
        self.assertEqual(test_response.context['pharmaceutical_list'][0].__unicode__(), u'Test Drug at 1 mg/kg, daily')


    def test_pharmaceutical_view(self):
        """This tests the pharmaceutical-view view, ensuring that templates are loaded correctly.  

        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        
        test_response = self.client.get('/parameter/pharmaceutical/1/')
        self.assertEqual(test_response.status_code, 200)
        self.assertTrue('pharmaceutical' in test_response.context)        
        self.assertTemplateUsed(test_response, 'pharmaceutical_detail.html')
        self.assertEqual(test_response.context['pharmaceutical'].pk, 1)
        self.assertEqual(test_response.context['pharmaceutical'].__unicode__(), u'Test Drug at 1 mg/kg, daily')


    def test_pharmaceutical_view_create(self):
        """This tests the pharmaceutical-new view, ensuring that templates are loaded correctly.  

        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        
        test_response = self.client.get('/parameter/pharmaceutical/new/')
        self.assertEqual(test_response.status_code, 200)
        self.assertTemplateUsed(test_response, 'base.html')
        self.assertTemplateUsed(test_response, 'pharmaceutical_form.html') 

    def test_pharmaceutical_view_edit(self):
        """This tests the pharmaceutical-edit view, ensuring that templates are loaded correctly.  

        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        
        test_response = self.client.get('/parameter/pharmaceutical/1/edit/')
        self.assertEqual(test_response.status_code, 200)
        self.assertTrue('pharmaceutical' in test_response.context)        
        self.assertTemplateUsed(test_response, 'pharmaceutical_form.html')
        self.assertEqual(test_response.context['pharmaceutical'].pk, 1)
        self.assertEqual(test_response.context['pharmaceutical'].__unicode__(), u'Test Drug at 1 mg/kg, daily')

        #verifies that a non-existent object returns a 404 error presuming there is no object with pk=2.
        null_response = self.client.get('/parameter/pharmaceutical/2/edit/')
        self.assertEqual(null_response.status_code, 404)   

    def test_pharmaceutical_view_delete(self):
        """This tests the pharmaceutical-delete view, ensuring that templates are loaded correctly.  

        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        
        test_response = self.client.get('/parameter/pharmaceutical/1/delete/')
        self.assertEqual(test_response.status_code, 200)
        self.assertTrue('pharmaceutical' in test_response.context)        
        self.assertTemplateUsed(test_response, 'confirm_delete.html')
        self.assertEqual(test_response.context['object'].pk, 1)
        self.assertEqual(test_response.context['object'].__unicode__(), u'Test Drug at 1 mg/kg, daily')

        #verifies that a non-existent object returns a 404 error.
        null_response = self.client.get('/parameter/pharmaceutical/2/delete/')
        self.assertEqual(null_response.status_code, 404) 
        
class CohortModelTests(BasicTestCase):
    '''These tests test the functionality of :class:`~mousedb.data.models.Cohort` objects.'''
    
    fixtures = ['test_animals','test_strain', 'test_treatment', 'test_study','test_measurement', 'test_assay','test_experiment']
    
    def test_create_cohort_minimum(self):
        '''This test creates a :class:`~mousedb.data.models.Cohort` with the required information only.'''

        test_cohort = Cohort(name = 'Test Cohort')
        test_cohort.save() 
        test_cohort.animals.add = Animal.objects.all()
        self.assertEqual(test_cohort.pk, 1) #presumes no models loaded in fixture data
        
    def test_create_cohort_all(self):
        '''This test creates a :class:`~mousedb.data.models.Cohort` with all information entered.'''

        test_cohort = Cohort(name = 'Test Cohort',
                             start_date = '2012-01-01',
                             end_date = '2012-08-01',
                             notes = "Some notes about this cohort")
        test_cohort.save() 
        test_cohort.animals.add = Animal.objects.all()
        test_cohort.treatment_groups.all = Treatment.objects.get(pk=1)
        test_cohort.studies.all = Study.objects.get(pk=1)
        self.assertEqual(test_cohort.pk, 1) #presumes no models loaded in fixture data      
        
    def test_cohort_unicode(self):
        '''This tests the unicode representation of a :class:`~mousedb.data.models.Cohort`.'''

        test_cohort = Cohort(name = 'Test Cohort')
        test_cohort.save() 
        test_cohort.animals.add = Animal.objects.all()
        self.assertEqual(test_cohort.__unicode__(), "Test Cohort") 
        
    def test_cohort_absolute_url(self):
        '''This tests the absolute_url generation of a :class:`~mousedb.data.models.Cohort`.'''

        test_cohort = Cohort(name = 'Test Cohort')
        test_cohort.save() 
        test_cohort.animals.add = Animal.objects.all()
        self.assertEqual(test_cohort.get_absolute_url(), "/cohort/test-cohort")        
        
class CohortViewTests(BasicTestCase):
    '''This class tests the views for :class:`~mousedb.data.models.Cohort` objects.'''

    fixtures = ['test_cohort', 'test_animals', 'test_strain']

    def test_cohort_list(self):
        """This tests the cohort-list view, ensuring that templates are loaded correctly.  

        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        
        test_response = self.client.get('/cohort/')
        self.assertEqual(test_response.status_code, 200)
        self.assertTrue('cohort_list' in test_response.context)      
        self.assertTemplateUsed(test_response, 'cohort_list.html')
        self.assertEqual(test_response.context['cohort_list'][0].pk, 1)
        self.assertEqual(test_response.context['cohort_list'][0].__unicode__(), u'Fixture Cohort')


    def test_cohort_view(self):
        """This tests the cohort-view view, ensuring that templates are loaded correctly.  

        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        
        test_response = self.client.get('/cohort/fixture-cohort')
        self.assertEqual(test_response.status_code, 200)
        self.assertTrue('cohort' in test_response.context)        
        self.assertTemplateUsed(test_response, 'cohort_detail.html')
        self.assertEqual(test_response.context['cohort'].pk, 1)
        self.assertEqual(test_response.context['cohort'].__unicode__(), u'Fixture Cohort')
        
        #verifies that a non-existent object returns a 404 error presuming there is no object with slug=wrong-cohort-name.
        null_response = self.client.get('/cohort/wrong-cohort-name')
        self.assertEqual(null_response.status_code, 404) 


    def test_cohort_view_create(self):
        """This tests the cohort-new view, ensuring that templates are loaded correctly.  

        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        
        test_response = self.client.get('/cohort/new/')
        self.assertEqual(test_response.status_code, 200)
        self.assertTemplateUsed(test_response, 'base.html')
        self.assertTemplateUsed(test_response, 'cohort_form.html') 

    def test_cohort_view_edit(self):
        """This tests the cohort-edit view, ensuring that templates are loaded correctly.  

        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        
        test_response = self.client.get('/cohort/fixture-cohort/edit')
        self.assertEqual(test_response.status_code, 200)
        self.assertTrue('cohort' in test_response.context)        
        self.assertTemplateUsed(test_response, 'cohort_form.html')
        self.assertEqual(test_response.context['cohort'].pk, 1)
        self.assertEqual(test_response.context['cohort'].__unicode__(), u'Fixture Cohort')

        #verifies that a non-existent object returns a 404 error presuming there is no object with slug=wrong-cohort-name.
        null_response = self.client.get('/cohort/wrong-cohort-name')
        self.assertEqual(null_response.status_code, 404)   

    def test_cohort_view_delete(self):
        """This tests the cohort-delete view, ensuring that templates are loaded correctly.  

        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        
        test_response = self.client.get('/cohort/fixture-cohort/delete')
        self.assertEqual(test_response.status_code, 200)
        self.assertTrue('object' in test_response.context)        
        self.assertTemplateUsed(test_response, 'confirm_delete.html')
        self.assertEqual(test_response.context['object'].pk, 1)
        self.assertEqual(test_response.context['object'].__unicode__(), u'Fixture Cohort')

        #verifies that a non-existent object returns a 404 error.
        null_response = self.client.get('/cohort/wrong-cohort-name/delete/')
        self.assertEqual(null_response.status_code, 404)
        
    def test_cohort_measurement_list(self):
        """This tests the cohort-data view, ensuring that templates are loaded correctly.  

        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        
        test_response = self.client.get('/cohort/fixture-cohort/data')
        self.assertEqual(test_response.status_code, 200)
        self.assertTrue('data_list' in test_response.context)      
        self.assertTemplateUsed(test_response, 'data_table.html')
        self.assertTemplateUsed(test_response, 'data.html')        
        self.assertTemplateUsed(test_response, 'base.html')
        self.assertTemplateUsed(test_response, 'jquery_script.html')  
        self.assertTemplateUsed(test_response, 'menu_script.html')
        self.assertTemplateUsed(test_response, 'jquery_ui_script_css.html')
        self.assertTemplateUsed(test_response, 'sortable_table_script.html')               
        print test_response.context['data_list']
        
        #test that a fake strain gives a 404 error
        fake_test_response = self.client.get('/cohort/some-made-up-cohort/data')
        self.assertEqual(fake_test_response.status_code, 404)          

    def test_strain_measurement_csv(self):
        """This tests the cohort-data-csv view, ensuring that templates are loaded correctly.  

        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        
        test_response = self.client.get('/cohort/fixture-cohort/data.csv')
        self.assertEqual(test_response.status_code, 200)
        self.assertEqual(test_response['Content-Type'], 'text/csv')
        self.assertEqual(test_response['Content-Disposition'], 'attachment; filename=data.csv') 
        
        #test that a fake strain gives a 404 error
        fake_test_response = self.client.get('/cohort/some-made-up-cohort/data.csv')
        self.assertEqual(fake_test_response.status_code, 404)            
        
class MeasurementViewTests(BasicTestCase):
    '''This class tests the views for :class:`~mousedb.data.models.Measurement` objects.'''

    fixtures = ['test_measurement', 'test_animals', 'test_strain', 'test_assay', 'test_experiment', 'test_assay']

    def test_measurement_list(self):
        """This tests the measurement_list view, ensuring that templates are loaded correctly.  

        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        
        test_response = self.client.get('/experiment/data/all')
        self.assertEqual(test_response.status_code, 200)
        self.assertTrue('data_list' in test_response.context)      
        self.assertTemplateUsed(test_response, 'data_table.html')
        self.assertTemplateUsed(test_response, 'data.html')        
        self.assertTemplateUsed(test_response, 'base.html')
        self.assertTemplateUsed(test_response, 'jquery_script.html')  
        self.assertTemplateUsed(test_response, 'menu_script.html')
        self.assertTemplateUsed(test_response, 'jquery_ui_script_css.html')
        self.assertTemplateUsed(test_response, 'sortable_table_script.html')               
        self.assertEqual(test_response.context['data_list'][0].pk,1)

    def test_measurement_csv(self):
        """This tests the measurement_list_csv view, ensuring that headers are set correctly.  

        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        
        test_response = self.client.get('/experiment/data/all.csv')
        self.assertEqual(test_response.status_code, 200)
        self.assertEqual(test_response['Content-Type'], 'text/csv')
        self.assertEqual(test_response['Content-Disposition'], 'attachment; filename=data.csv') 

    def test_strain_measurement_list(self):
        """This tests the strain-data view, ensuring that templates are loaded correctly.  

        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        
        test_response = self.client.get('/strain/fixture-strain/data')
        self.assertEqual(test_response.status_code, 200)
        self.assertTrue('data_list' in test_response.context)      
        self.assertTemplateUsed(test_response, 'data_table.html')
        self.assertTemplateUsed(test_response, 'data.html')        
        self.assertTemplateUsed(test_response, 'base.html')
        self.assertTemplateUsed(test_response, 'jquery_script.html')  
        self.assertTemplateUsed(test_response, 'menu_script.html')
        self.assertTemplateUsed(test_response, 'jquery_ui_script_css.html')
        self.assertTemplateUsed(test_response, 'sortable_table_script.html')               
        self.assertEqual(test_response.context['data_list'][0].pk,1)
        
        #test that a fake strain gives a 404 error
        fake_test_response = self.client.get('/strain/some-made-up-strain/data')
        self.assertEqual(fake_test_response.status_code, 404)          
        self.assertEqual(test_response.context['data_list'][0].animal.Strain.__unicode__(), u'Fixture Strain')

    def test_strain_measurement_csv(self):
        """This tests the strain-data-csv view, ensuring that templates are loaded correctly.  

        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        
        test_response = self.client.get('/strain/fixture-strain/data.csv')
        self.assertEqual(test_response.status_code, 200)
        self.assertEqual(test_response['Content-Type'], 'text/csv')
        self.assertEqual(test_response['Content-Disposition'], 'attachment; filename=data.csv') 
        
        #test that a fake strain gives a 404 error
        fake_test_response = self.client.get('/strain/some-made-up-strain/data.csv')
        self.assertEqual(fake_test_response.status_code, 404)      