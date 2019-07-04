from django.test import TestCase, Client

from accounts.models import User
from gremios.models import RutGremio


class ObjectsCreation(object):
    def setUp(self):
        self.client = Client()
        self.rut_gremio = [RutGremio.objects.create_rut_gremio(rut='12245453-3'),
                            RutGremio.objects.create_rut_gremio(rut='5169011-7'),
                            RutGremio.objects.create_rut_gremio(rut='13064499-6'),]
        
        self.user = User.objects.create_user(rut='12245453-3', password='pass.1234')
        
        self.staff_user = User.objects.create_staffuser(rut='16747983-9', password='pass.1234')
        
        self.super_user = User.objects.create_superuser(rut='17256372-4', password='pass.1234')

class UserModelTestCase(ObjectsCreation, TestCase):
    def test_string_representation_user(self):
        user = self.user
        self.assertEqual(str(user.get_short_name()), user.rut)

    def test_create_user(self):
        User.objects.create_user(rut='13064499-6', email='test@test.cl', full_name='Test Testo', password='pass.1234')
        self.assertEqual(User.objects.all().filter(rut='13064499-6').count() != 0, True)

class UserCreateTestCase(ObjectsCreation, TestCase):
    def test_user_create(self):
        url = '/register/'
        data = {
            'rut': '5169011-7',
            'full_name': 'Juan Perez',
            'email': 'jperez@test.cl',
            'password1': 'pass.1234',
            'password2': 'pass.1234',
        }
        response = self.client.post(url, data)
        self.assertEqual(User.objects.filter(rut='5169011-7').count(), 1)

    def test_user_create_not_in_rut_gremios(self):
        url = '/register/'
        data = {
            'rut': '76438153-K',
            'full_name': 'Juan Roa',
            'email': 'jroa@test.cl',
            'password1': 'pass.1234',
            'password2': 'pass.1234',
        }
        response = self.client.post(url, data)
        self.assertEqual(User.objects.filter(rut='76438153-K').count(), 0)

    def test_user_create_rut_not_valid(self):
        url = '/register/'
        data = {
            'rut': '1111-K',
            'full_name': 'Juan Test',
            'email': 'jtest@test.cl',
            'password1': 'pass.1234',
            'password2': 'pass.1234',
        }
        response = self.client.post(url, data)
        self.assertEqual(User.objects.filter(rut='1111-K').count(), 0)

    def test_user_create_password_not_match(self):
        url = '/register/'
        data = {
            'rut': '13064499-6',
            'full_name': 'Juan Prueba',
            'email': 'jprueba@test.cl',
            'password1': 'pass.1235',
            'password2': 'pass.1234',
        }
        response = self.client.post(url, data)
        self.assertEqual(User.objects.filter(rut='13064499-6').count(), 0)
    
    def test_user_create_rut_exists(self):
        url = '/register/'
        data = {
            'rut': '12245453-3',
            'full_name': 'Juan Prueba',
            'email': 'jprueba@test.cl',
            'password1': 'pass.1234',
            'password2': 'pass.1234',
        }
        response = self.client.post(url, data)
        self.assertEqual(User.objects.filter(rut='12245453-3').count(), 1)
        self.assertIn('Ya existe User con este Rut.', str(response.content))

