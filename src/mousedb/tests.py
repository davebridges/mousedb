"""This file contains tests for the root application.

These tests will verify function of the home and logout views.
"""

from django.test import TestCase
from django.test.client import Client, RequestFactory

class RootViewTests(TestCase):
    """These are tests for the root views.  Included are tests for home and logout."""
    fixtures = ['test_breeding', 'test_animals', 'test_strain']

    def setUp(self):
        self.client = Client()
        self.test_user = User.objects.create_user('blah', 'blah@blah.com', 'blah')
        self.test_user.is_superuser = True
        self.test_user.is_active = True
        self.test_user.save()
        self.client.login(username='blah', password='blah')
        self.factory = RequestFactory()

    def tearDown(self):
        self.client.logout()
        self.test_user.delete()

    def test_home(self):
        """This test checks the view which displays the home page.  It checks for the correct templates and status code."""        
        response = self.client.get('/index/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'home.html')
        factory_request = self.factory.get('/index/'')
        response_factory = home(factory_request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'home.html') 

    def test_logout(self):
        """This test checks the view which displays the logout page.  It checks for the correct templates and status code."""        
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'logout.html')
        factory_request = self.factory.get('/logout/'')
        response_factory = home(factory_request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'logout.html')          


