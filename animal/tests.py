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
        print "create_animal_minimal... passed"

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
        print "animal_unicode... passed"

    def test_create_breeding_minimal(self):
        """This is a test for creating a new breeding object, with only the minimum being entered."""
        example_strain = Strain(Strain="Example Strain")
        example_strain.save()
        new_breeding = Breeding(Strain = example_strain)
        new_breeding.save()
	test_breeding = Breeding.objects.get(Strain=example_strain)
        self.assertEquals(test_breeding, new_breeding)
        self.assertEquals(test_breeding.__unicode__(), "Example Strain Breeding Cage: None starting on None")
        print "create_breeding_minimal... passed"

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
        print "autoset_breeding_active_state... passed"
		
	def test_male_breeding_location_type(self):
	    """This is a test that the breeding_location_type attribute is being set correctly.
		
        Normal function is that if the breeding cage of a Breeding object and the cage of an Animal object are the same then the breeding male is set to "resident breeder", if not then it is a "non-resident breeder"""
        example_strain = Strain(Strain="Example Strain")
        example_strain.save()
        animal = Animal(Strain = example_strain, Genotype="-/-", Background="Mixed", Cage=1234, Gender='M')
        animal.save()		
        test_breeding = Breeding(Strain = example_strain, Male=animal, Cage=1234)
        test_breeding.save()
        self.assertEquals(test_breeding.male_breeding_location_type, "resident breeder")
        test_breeding_nr = Breeding(Strain = example_strain, Male=animal, Cage=5678)
        self.assertEquals(test_breeding.male_breeding_location_type, "non-resident breeder")
        print "male_breeding_location_type... passed"
		
    #def test_update_breeding_cage_automatically_move_animal(self):
    #    """This is a test for creating a new breeding object, with only the minimum being entered.  It also tests whether the cages are updated to the breeding cage when that attribute is set.  This tests if only one female is in a breeding set."""
    #    example_strain = Strain(Strain="Example Strain")
    #    example_strain.save()
    #    example_male = Animal(Strain = example_strain, Genotype="-/-", Background="Mixed", Gender='M', Cage=1111)
    #    example_male.save()
    #    self.assertEquals(example_male.Cage, 1111)
    #    example_female = Animal(Strain = example_strain, Genotype="-/-", Background="Mixed", Gender='F', Cage=2222)
    #    example_female.save()
    #    self.assertEquals(example_female.Cage, 2222)
    #    new_breeding = Breeding(Strain = example_strain, Cage=3333)
    #    new_breeding.Male = example_male
    #    new_breeding.Females = example_female
    #    new_breeding.save()
    #    self.assertEquals(example_male.Cage, 3333)
    #    self.assertEquals(example_female.Cage, 3333)
	
    #def test_update_breeding_cage_automatically_move_animal_two_females(self):
    #    """This is a test for creating a new breeding object, with only the minimum being entered.  It also tests whether the cages are updated to the breeding cage when that attribute is set.  This tests if more than one female is in a breeding set."""
    #    example_strain = Strain(Strain="Example Strain")
    #    example_strain.save()
    #    example_male = Animal(Strain = example_strain, Genotype="-/-", Background="Mixed", Gender='M', Cage=1111)
    #    example_male.save()
    #    self.assertEquals(example_male.Cage, 1111)
    #    example_female1 = Animal(Strain = example_strain, Genotype="-/-", Background="Mixed", Gender='F', Cage=2222)
    #    example_female1.save()
    #    example_female2 = Animal(Strain = example_strain, Genotype="-/-", Background="Mixed", Gender='F', Cage=3333)
    #    example_female2.save()
    #    self.assertEquals(example_female1.Cage, 2222)
    #    self.assertEquals(example_female2.Cage, 3333)
    #    new_breeding = Breeding(Strain = example_strain, Cage=4444)
    #    new_breeding.save()
    #    new_breeding.Male = example_male
    #    new_breeding.Females = example_female1, example_female2
    #    new_breeding.save()
    #    self.assertEquals(example_male.Cage, 4444)
    #    self.assertEquals(example_female1.Cage, 4444)
    #    self.assertEquals(example_female2.Cage, 4444)

    #def test_update_breeding_rack_automatically_move_animal(self):
    #    """This is a test for creating a new breeding object, with only the minimum being entered.  It also tests whether the rack is updated to the breeding rack when that attribute is set.  This tests if only one female is in a breeding set."""
    #    example_strain = Strain(Strain="Example Strain")
    #    example_strain.save()
    #    example_male = Animal(Strain = example_strain, Genotype="-/-", Background="Mixed", Gender='M', Rack="A")
    #    example_male.save()
    #    self.assertEquals(example_male.Rack, "A")
    #    example_female = Animal(Strain = example_strain, Genotype="-/-", Background="Mixed", Gender='F', Rack="B")
    #    example_female.save()
    #    self.assertEquals(example_female.Rack, "B")
    #    new_breeding = Breeding(Strain = example_strain, Rack="C")
    #    new_breeding.male = example_male
    #    new_breeding.females = example_female
    #    new_breeding.save()
    #    self.assertEquals(example_male.Rack, "C")
    #    self.assertEquals(example_female.Rack, "C")
	
    #def test_update_breeding_rack_automatically_move_animal_two_females(self):
    #    """This is a test for creating a new breeding object, with only the minimum being entered.  It also tests whether the rack is updated to the breeding cage when that attribute is set.  This tests if more than one female is in a breeding set."""
     #   example_strain = Strain(Strain="Example Strain")
     #   example_strain.save()
     #   example_male = Animal(Strain = example_strain, Genotype="-/-", Background="Mixed", Gender='M', Rack="A")
     #   example_male.save()
     #   self.assertEquals(example_male.Rack, "A")
     #   example_female1 = Animal(Strain = example_strain, Genotype="-/-", Background="Mixed", Gender='F', Rack="B")
     #   example_female1.save()
     #   example_female2 = Animal(Strain = example_strain, Genotype="-/-", Background="Mixed", Gender='F', Rack="C")
     #   example_female2.save()
     #   self.assertEquals(example_female1.Rack, "B")
     #   self.assertEquals(example_female2.Rack, "C")
     #   new_breeding = Breeding(Strain = example_strain, Rack="D")
     #   new_breeding.male = example_male
     #   new_breeding.females = example_female1, example_female2
     #   new_breeding.save()
     #   self.assertEquals(example_male.Rack, "D")
     #   self.assertEquals(example_female1.Rack, "D")
     #   self.assertEquals(example_female2.Rack, "D")

    #def test_update_breeding_rack_position_automatically_move_animal(self):
    #    """This is a test for creating a new breeding object, with only the minimum being entered.  It also tests whether the rack position is updated to the breeding rack when that attribute is set.  This tests if only one female is in a breeding set."""
    #    example_strain = Strain(Strain="Example Strain")
    #    example_strain.save()
    #    example_male = Animal(Strain = example_strain, Genotype="-/-", Background="Mixed", Gender='M', Rack_Position="A1")
    #    example_male.save()
    #    self.assertEquals(example_male.Rack_Position, "A1")
    #    example_female = Animal(Strain = example_strain, Genotype="-/-", Background="Mixed", Gender='F', Rack_Position="B1")
    #    example_female.save()
    #    self.assertEquals(example_female.Rack_Position, "B1")
    #    new_breeding = Breeding(Strain = example_strain, Rack_Position="C1")
    #    new_breeding.male = example_male
    #    new_breeding.females = example_female
    #    new_breeding.save()
    #    self.assertEquals(example_male.Rack_Position, "C1")
    #    self.assertEquals(example_female.Rack_Position, "C1")
	
    #def test_update_breeding_rack_automatically_move_animal_two_females(self):
    #    """This is a test for creating a new breeding object, with only the minimum being entered.  It also tests whether the rack position is updated to the breeding cage when that attribute is set.  This tests if more than one female is in a breeding set."""
    #    example_strain = Strain(Strain="Example Strain")
    #    example_strain.save()
    #    example_male = Animal(Strain = example_strain, Genotype="-/-", Background="Mixed", Gender='M', Rack_Position="A1")
    #    example_male.save()
    #    self.assertEquals(example_male.Rack_Position, "A1")
    #    example_female1 = Animal(Strain = example_strain, Genotype="-/-", Background="Mixed", Gender='F', Rack_Position="B1")
    #    example_female1.save()
    #    example_female2 = Animal(Strain = example_strain, Genotype="-/-", Background="Mixed", Gender='F', Rack_Position="C1")
    #    example_female2.save()
    #    self.assertEquals(example_female1.Rack_Position, "B1")
    #    self.assertEquals(example_female2.Rack_Position, "C1")
    #    new_breeding = Breeding(Strain = example_strain, Rack_Position="D1")
    #    new_breeding.male = example_male
    #    new_breeding.females = example_female1, example_female2
    #    new_breeding.save()
    #    self.assertEquals(example_male.Rack_Position, "D1")
    #    self.assertEquals(example_female1.Rack_Position, "D1")
    #    self.assertEquals(example_female2.Rack_Position, "D1")


class BreedingViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.test_user = User.objects.create_user('blah', 'blah@blah.com', 'blah')
        self.test_user.is_superuser = True
        self.test_user.save()
        self.client.login(username='blah', password='blah')

    def tearDown(self):
        self.client.logout()
        self.test_user.delete()

    def test_breeding_list(self):
        response = self.client.get('/breeding/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'sortable_table_script.html')
        self.assertTemplateUsed(response, 'breeding.html')
        print "breeding_list ... passed"

    def test_breeding_list_all(self):
        response = self.client.get('/breeding/all/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'sortable_table_script.html')
        self.assertTemplateUsed(response, 'breeding.html')
        print "breeding_list_all ... passed"

    def test_breeding_new(self):
        response = self.client.get('/breeding/new/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'breeding_form.html')
        print "breeding_new ... passed"
