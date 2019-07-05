from django.test import TestCase, Client

from accounts.models import User
from gremios.models import RutGremio


class ObjectsCreation(object):
    def setUp(self):
        self.client = Client()
        self.rut_gremio = RutGremio.objects.create_rut_gremio(rut='12245453-3')
        self.user = User.objects.create_user(rut='12245453-3', password='pass.1234')
        self.staff_user = User.objects.create_staffuser(rut='16747983-9', password='pass.1234')
        self.super_user = User.objects.create_superuser(rut='17256372-4', password='pass.1234')

class HomePageTestCase(ObjectsCreation, TestCase):

    def test_redirect_to_login_page_if_not_authenticated(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        if response.status_code == 302:
            self.assertIn("login", str(response.url))
    
    def test_home_page_pass_if_authenticated(self):
        data = {
            'rut': self.user.rut, 
            'password': 'pass.1234',
        }
        response = self.client.post('/login/', data)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Inicio", str(response.content))

    def test_home_page_pass_if_staff_user(self):
        data = {
            'rut': self.staff_user.rut, 
            'password': 'pass.1234',
        }
        response = self.client.post('/login/', data)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Inicio", str(response.content))

    def test_home_page_pass_if_super_user(self):
        data = {
            'rut': self.super_user.rut, 
            'password': 'pass.1234',
        }
        response = self.client.post('/login/', data)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Inicio", str(response.content))

class AdminPageTestCase(ObjectsCreation, TestCase):
    def test_admin_page_redirect_if_authenticated(self):
        data = {
            'rut': self.user.rut, 
            'password': 'pass.1234',
        }
        response = self.client.post('/login/', data)
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 302)

    def test_admin_page_pass_if_staff_user(self):
        data = {
            'rut': self.staff_user.rut, 
            'password': 'pass.1234',
        }
        response = self.client.post('/login/', data)
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)

    def test_admin_page_pass_if_super_user(self):
        data = {
            'rut': self.super_user.rut, 
            'password': 'pass.1234',
        }
        response = self.client.post('/login/', data)
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)