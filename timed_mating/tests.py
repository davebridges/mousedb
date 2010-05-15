"""This file contains tests for the timed_mating application.

These tests will verify generation of a new PlugEvent object.
"""

import datetime

from django.test import TestCase
from django.test.client import Client

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

    def test_set_plugevet_inactive(self):
        """This is a test for the automatic inactivation of a cage when the SacrificeDate is entered."""
        plugevent = PlugEvents(PlugDate = datetime.date.today() )
        plugevent.save()
        self.assertEquals(plugevent.__unicode__(), "Plug Event - 1")
        self.assertEquals(plugevent.Active, True)
        plugevent = PlugEvents(id = 1, PlugDate = datetime.date.today(), SacrificeDate = datetime.date.today() )
        plugevent.save()
        self.assertEquals(plugevent.Active, False)

