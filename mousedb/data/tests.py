"""This file contains tests for the data application.

These tests will verify generation of new experiment, measurement, assay, researcher, study, treatment, vendor, diet, environment, implantation, transplantation and pharnaceutical objects.
"""
import datetime

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User

from mousedb.data.models import Study
from mousedb.animal.models import Strain

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
				
class TreatmentViewTests(BasicTestCase):
    """These tests test the views associated with Treatment objects."""

    fixtures = ['test_treatment','test_study']

    def test_treatment_detail(self):
        """This test checks the view which displays a treatment-detail page.  It checks for the correct templates and status code."""        

        response = self.client.get('/treatment/1/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'jquery_script.html')
        self.assertTemplateUsed(response, 'jquery_ui_script_css.html')
        self.assertTemplateUsed(response, 'treatment_detail.html')
        self.assertTemplateUsed(response, 'sortable_table_script.html')
