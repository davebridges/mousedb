from django.test import TestCase
from django.contrib.auth.models import User
from mousedb.animal.models import Animal, Strain, Breeding

class AnimalViewTests(TestCase):
     
    def setUp(self):
        user = User.objects.create_user('testuser', 'user@useremail.com', 'testuserpassword')
        user.save()
        login = self.client.login(username='testuser', password='testuserpassword')
        self.assertEqual(login, True)

    def test_mouse_index(self):
        response = self.client.get('/mouse/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'animal_list.html')


class StrainViewTests(TestCase):

    def setUp(self):
        user = User.objects.create_user('testuser', 'user@useremail.com', 'testuserpassword')
        user.save()
        login = self.client.login(username='testuser', password='testuserpassword')
        self.assertEqual(login, True)

    def test_strain_index(self):
        response = self.client.get('/strain/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'strain_list.html')

