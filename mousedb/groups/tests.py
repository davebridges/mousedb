"""This file contains tests for the groups application.

These tests will verify generation of a new group and license object.
"""

from django.test import TestCase
from django.test.client import Client

from mousedb.groups.models import Group, License
 
MODELS = [Group, License]


class GroupsModelTests(TestCase):
    """Test the models contained in the 'groups' app."""
    
    fixtures = ['test_group',]
    
    def setUp(self):
        """Instantiate the test client."""
        self.client = Client()
    def tearDown(self):
        """Depopulate created model instances from test database."""
        for model in MODELS:
            for obj in model.objects.all():
                obj.delete()
    def test_create_group_minimal(self):
        """This is a test for creating a new group object, with only the minimum being entered."""
        new_group = Group(group = "Awesome Lab")
        new_group.save()
        test_group = Group.objects.get(group="Awesome Lab")
        self.assertEquals(test_group, new_group)
        self.assertEquals(test_group.__unicode__(), "Awesome Lab")

    def test_create_license_minimal(self):
        """This is a test for creating a new license object, with only the minimum being entered."""
        new_license = License(license = "Awesome Lab's Site License")
        new_license.save()
	test_license = License.objects.get(license="Awesome Lab's Site License")
        self.assertEquals(test_license, new_license)
        self.assertEquals(test_license.__unicode__(), "Awesome Lab's Site License")

    def test_create_group_all_fields(self):
        """This is a test for creating a new group object, with all fields being entered, except license."""
        license = License(license = "Awesome Lab's Site License")
        license.save()
        new_group = Group(
            group = "Awesome Lab",
            group_slug = "Awesome_Lab",
            group_url = "www.awesomegroup.com",
            license = License.objects.get(pk=1),
            contact_title = "Dr.",
            contact_first = "Mike",
            contact_last = "Awesome",
            contact_email = "m.awesome@awesomegroup.com")
        new_group.save()
	test_group = Group.objects.get(group="Awesome Lab")
        self.assertEquals(test_group, new_group)
        self.assertEquals(test_group.__unicode__(), "Awesome Lab")

    def test_create_license_all_fields(self):
        """This is a test for creating a new license object, with all fields being entered."""
        new_license = License(
            license = "Awesome Lab's Site License",
            website = "sitelicense.com/awesomelab",
            notes = "The terms of the license are blah blah blah")
        new_license.save()
	test_license = License.objects.get(license="Awesome Lab's Site License")
        self.assertEquals(test_license, new_license)
        self.assertEquals(test_license.__unicode__(), "Awesome Lab's Site License")

