"""This file contains tests for the animal application.

These tests will verify generation and function of a new breeding, strain and animal object.
"""

import datetime

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User

from mousedb.animal.models import Animal, Strain, Breeding

MODELS = [Breeding, Animal, Strain]

class BreedingModelTests(TestCase):
    """Test the models contained in the 'groups' app."""
    
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
        example_strain = Strain(Strain="Example Strain")
        example_strain.save()
        new_breeding = Breeding(Strain = example_strain)
        new_breeding.save()
	test_breeding = Breeding.objects.get(Strain=example_strain)
        self.assertEquals(test_breeding, new_breeding)
        self.assertEquals(test_breeding.__unicode__(), "Example Strain Breeding Cage: None starting on None")

    def test_autoset_active_state(self):
        """This is a test for creating a new breeding object, with only the minimum being entered.  That object is then tested for the active state being automatically set when a End date is specified."""
        example_strain = Strain(Strain="Example Strain")
        example_strain.save()
        new_breeding = Breeding(Strain = example_strain)
        new_breeding.save()
	test_breeding = Breeding.objects.get(Strain=example_strain)
        self.assertEquals(test_breeding.Active, True)
        test_breeding.End = datetime.date.today()
        test_breeding.save()
        self.assertEquals(test_breeding.Active, False)
