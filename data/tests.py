"""This file contains tests for the data application.

These tests will verify generation and function of a all objects in the data application.
"""

import datetime

from django.test import TestCase
from django.test.client import Client

from mousedb.animal.models import Animal
from mousedb.data.models import Experiment, Measurement, Assay, Researcher, Study, Treatment, Vendor, Diet, Environment, Implantation, Pharmaceutical, Transplantation

MODELS = [Experiment, Measurement, Assay, Researcher, Study, Treatment, Vendor, Diet, Environment, Implantation, Pharmaceutical, Transplantation]

class ExperimentModelTests(TestCase):
    """Test the Experiment model contained in the 'data' application."""
    fixtures = ['test_data']
    
    def setUp(self):
        """Instantiate the test client."""
        self.client = Client()
    
    def tearDown(self):
        """Depopulate created model instances from test database."""
        for model in MODELS:
            for obj in model.objects.all():
                obj.delete()
    
    def test_create_experiment_minimal(self):
        """This is a test for creating a new experiment object, with only the minimum fields being entered"""
        test_experiment = Experiment(
            date = "2020-01-01", 
            )
        test_experiment.save()
        self.assertEquals(test_experiment.__unicode__(), "2020-01-01-fed")
        print "create_experiment_minimal... passed"

    def test_experiment_unicode(self):
        """This test verifies that the unicode representation of an experiment is date-feeding state"""
        test_experiment = Experiment.objects.get(pk=1)
        self.assertEquals(test_experiment.__unicode__(), "2010-08-21-fed")
        print "experiment_unicode... passed"

    def test_experiment_get_absolute_url(self):
        """This test verifies the absolute url of an experiment object."""
        test_experiment = Experiment.objects.get(pk=1)
        self.assertEquals(test_experiment.get_absolute_url(), "/experiment/1/")
        print "experiment_get_absolute_url... passed"
