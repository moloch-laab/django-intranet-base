from django.test import TestCase, Client

from accounts.models import User
from gremios.models import RutGremio


class ObjectsCreation(object):
    def setup(self):
        self.client = Client()
        self.rut_gremio = [RutGremio.objects.create_rut_gremio(rut='12245453-3'),
                            RutGremio.objects.create_rut_gremio(rut='5169011-7'),
                            RutGremio.objects.create_rut_gremio(rut='13064499-6'),]
        
        self.user = User.objects.create_user(rut='12245453-3', password='pass.1234')
        
        self.staff_user = User.objects.create_staffuser(rut='16747983-9', password='pass.1234')
        
        self.super_user = User.objects.create_superuser(rut='17256372-4', password='pass.1234')

class TestHomePage(ObjectsCreation, TestCase):

    def test_login_page_if_not_authenticated(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        if response.status_code == 302:
            self.assertIn("login", str(response.url))
    
    def test_home_page_if_authenticated(self):
        data = {'rut': '12245453-3', 'password': 'pass.1234'}
        response = self.client.post('/login/', data)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        # self.assertIn("Inicio", str(response.content))

class UserCreateTestCase(ObjectsCreation, TestCase):
    def test_user_create(self):
        url = '/register/'
        data = {
            'rut': '5169011-7',
            'full_name': 'Juan Perez',
            'email': 'jperez@test.cl',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)