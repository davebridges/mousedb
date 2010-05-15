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
    
    def test_create_animal_minimal(self):
        """This is a test for creating a new animal object, with only the minimum fields being entered"""
        example_strain = Strain(Strain="Example Strain")
        example_strain.save()
        animal = Animal(Strain = example_strain, Genotype="-/-", Background="Mixed")
        animal.save()
        animal_id = animal.id
        self.assertEquals(animal.__unicode__(), "Example Strain (%s)" % animal_id)

    def test_unicode(self):
        """This is a test for creating a new animal object, with only the minimum fields being entered.  It then tests that the correct unicode representation is being generated."""
        example_strain = Strain(Strain="Example Strain")
        example_strain.save()
        animal = Animal(Strain = example_strain, Genotype="-/-", Background="Mixed")
        animal.save()
        animal_id = animal.id
        self.assertEquals(animal.__unicode__(), "Example Strain (%s)" % animal_id)
        animal.MouseID = 1234
        animal.save()
        self.assertEquals(animal.__unicode__(), "Example Strain-EarTag #1234")

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

    def test_update_breeding_cage_automatically_move_animal(self):
        """This is a test for creating a new breeding object, with only the minimum being entered.  It also tests whether the cages are updated to the breeding cage when that attribute is set.  This tests if only one female is in a breeding set."""
        example_strain = Strain(Strain="Example Strain")
        example_strain.save()
        example_male = Animal(Strain = example_strain, Genotype="-/-", Background="Mixed", Gender='M', Cage=1111)
        example_male.save()
        self.assertEquals(example_male.Cage, 1111)
        example_female = Animal(Strain = example_strain, Genotype="-/-", Background="Mixed", Gender='F', Cage=2222)
        example_female.save()
        self.assertEquals(example_female.Cage, 2222)
        new_breeding = Breeding(Strain = example_strain, Cage=3333)
        new_breeding.male = example_male
        new_breeding.females = example_female
        new_breeding.save()
        self.assertEquals(example_male.Cage, 3333)
        self.assertEquals(example_female.Cage, 3333)
	
    def test_update_breeding_cage_automatically_move_animal_two_females(self):
        """This is a test for creating a new breeding object, with only the minimum being entered.  It also tests whether the cages are updated to the breeding cage when that attribute is set.  This tests if more than one female is in a breeding set."""
        example_strain = Strain(Strain="Example Strain")
        example_strain.save()
        example_male = Animal(Strain = example_strain, Genotype="-/-", Background="Mixed", Gender='M', Cage=1111)
        example_male.save()
        self.assertEquals(example_male.Cage, 1111)
        example_female1 = Animal(Strain = example_strain, Genotype="-/-", Background="Mixed", Gender='F', Cage=2222)
        example_female1.save()
        example_female2 = Animal(Strain = example_strain, Genotype="-/-", Background="Mixed", Gender='F', Cage=3333)
        example_female2.save()
        self.assertEquals(example_female1.Cage, 2222)
        self.assertEquals(example_female2.Cage, 3333)
        new_breeding = Breeding(Strain = example_strain, Cage=4444)
        new_breeding.male = example_male
        new_breeding.females = example_female1, example_female2
        new_breeding.save()
        self.assertEquals(example_male.Cage, 4444)
        self.assertEquals(example_female1.Cage, 4444)
        self.assertEquals(example_female2.Cage, 4444)
