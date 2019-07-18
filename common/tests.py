from django.test import TestCase, Client
from django.db.utils import IntegrityError
from django.forms import ValidationError
from django.contrib.admin.sites import AdminSite

from .admin import UserAdmin
from .models import User
from gremios.models import RutGremio

class ObjectCreation(object):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(rut='7264437-9', 
                                             email='test1@test.cl', 
                                             first_name='Test', 
                                             last_name='Testo', 
                                             password='pass.1234')
        self.is_superuser = User.objects.create_superuser(rut='12384351-7',
                                                       email='superuser@test.cl',
                                                       password='pass.1234')
        self.rut_gremio = RutGremio.objects.create_rut_gremio('13064499-6')
        self.valid_rut = '13064499-6'
        self.invalid_rut = '1306499-6'
        self.valid_email = 'francisco.bahamondes90@gmail.com'

    def login(self, username='7264437-9', password='pass.1234'):
        url = '/login/'
        data = {
            'rut': username,
            'password': password
        }
        self.client.post(url,data)
    
    def login_superuser(self, username='12384351-7', password='pass.1234'):
        url = '/login/'
        data = {
            'rut': username,
            'password': password
        }
        self.client.post(url,data)

class UserModelTestCase(ObjectCreation, TestCase):
    def test_string_representation_user(self):
        user = self.user
        self.assertEqual(str(user.get_short_name()), user.rut)

    def test_create_user(self):
        User.objects.create_user(rut=self.valid_rut, 
                                 email=self.valid_email, 
                                 first_name='Test', 
                                 last_name='Testo', 
                                 password='pass.1234')
        self.assertEqual(User.objects.all().filter(rut=self.valid_rut).count() != 0, True)
    
    def test_create_staffuser(self):
        User.objects.create_staffuser(rut=self.valid_rut, 
                                      email=self.valid_email, 
                                      password='pass.1234')
        self.assertEqual(User.objects.all().filter(rut=self.valid_rut).count() != 0, True)
    
    def test_create_superuser(self):
        User.objects.create_superuser(rut=self.valid_rut, 
                                      email=self.valid_email, 
                                      password='pass.1234')
        self.assertEqual(User.objects.all().filter(rut=self.valid_rut).count() != 0, True)
    
    def test_create_user_invalid_rut(self):
        with self.assertRaises(ValueError) as error:
            User.objects.create_user(rut=self.invalid_rut, 
                                     email=self.valid_email, 
                                     first_name='Test', 
                                     last_name='Testo', 
                                     password='pass.1234')
        self.assertEqual(User.objects.all().filter(rut=self.invalid_rut).count() != 0, False)
        self.assertEqual("Rut no válido", str(error.exception))
    
    def test_create_staffuser_invalid_rut(self):
        with self.assertRaises(ValueError) as error:
            User.objects.create_staffuser(rut=self.invalid_rut, 
                                          email=self.valid_email, 
                                          password='pass.1234')
        self.assertEqual(User.objects.all().filter(rut=self.invalid_rut).count() != 0, False)
        self.assertEqual("Rut no válido", str(error.exception))
    
    def test_create_superuser_invalid_rut(self):
        with self.assertRaises(ValueError) as error:
            User.objects.create_superuser(rut=self.invalid_rut, 
                                          email=self.valid_email, 
                                          password='pass.1234')
        self.assertEqual(User.objects.all().filter(rut=self.invalid_rut).count() != 0, False)
        self.assertEqual("Rut no válido", str(error.exception))

    def test_create_user_existing_rut(self):
        with self.assertRaises(IntegrityError) as error:
            User.objects.create_staffuser(rut=self.user.rut, 
                                          email=self.valid_email, 
                                          password='pass.1234')
        self.assertIn("common_user.rut", str(error.exception))

    def test_create_user_existing_email(self):
        with self.assertRaises(IntegrityError) as error:
            User.objects.create_staffuser(rut=self.valid_rut, 
                                          email=self.user.email, 
                                          password='pass.1234')
        self.assertIn("common_user.email", str(error.exception))

class RegisterUserTestCase(ObjectCreation, TestCase):
    def test_register_user_post_method(self):
        url = '/register/'
        data = {
            'first_name': 'Juan',
            'last_name': 'Perez',
            'rut': self.valid_rut,
            'email': self.valid_email,
            'password1': 'pass.1234',
            'password2': 'pass.1234',
        }
        response = self.client.post(url, data)
        self.assertEqual(User.objects.filter(rut=self.valid_rut).count(), 1)
        self.assertIn("Debe validar su direcc", str(response.content))

    def test_register_user_post_method_rut_invalid(self):
        url = '/register/'
        data = {
            'first_name': 'Juan',
            'last_name': 'Perez',
            'rut': self.invalid_rut,
            'email': self.valid_email,
            'password1': 'pass.1234',
            'password2': 'pass.1234',
        }
        response = self.client.post(url, data)
        self.assertEqual(User.objects.filter(rut=self.invalid_rut).count(), 0)
        self.assertIn("El rut ingresado no es", str(response.content))
        self.assertEqual(200, response.status_code)

    def test_register_user_post_method_existing_rut(self):
        url = '/register/'
        data = {
            'first_name': 'Juan',
            'last_name': 'Perez',
            'rut': self.user.rut,
            'email': self.valid_email,
            'password1': 'pass.1234',
            'password2': 'pass.1234',
        }
        response = self.client.post(url, data)
        self.assertEqual(User.objects.filter(rut=self.user.rut).count(), 1)
        # self.assertIn("Ya existe User con este Rut.", str(response.content))
        self.assertEqual(200, response.status_code)

    def test_register_user_post_method_existing_email(self):
        url = '/register/'
        data = {
            'first_name': 'Juan',
            'last_name': 'Perez',
            'rut': self.valid_rut,
            'email': self.user.email,
            'password1': 'pass.1234',
            'password2': 'pass.1234',
        }
        response = self.client.post(url, data)
        self.assertEqual(User.objects.filter(rut=self.valid_rut).count(), 0)
        self.assertIn("Ya existe User con este Email.", str(response.content))
        self.assertEqual(200, response.status_code)

    def test_register_user_post_method_blank_name(self):
        url = '/register/'
        data = {
            'first_name': '',
            'last_name': 'Perez',
            'rut': self.valid_rut,
            'email': self.valid_email,
            'password1': 'pass.1234',
            'password2': 'pass.1234',
        }
        response = self.client.post(url, data)
        self.assertEqual(User.objects.filter(rut=self.valid_rut).count(), 0)
        self.assertIn("Este campo es obligatorio.", str(response.content))
        self.assertEqual(200, response.status_code)

    def test_register_user_post_method_blank_email(self):
        url = '/register/'
        data = {
            'first_name': 'Juan',
            'last_name': 'Perez',
            'rut': self.valid_rut,
            'email': '',
            'password1': 'pass.1234',
            'password2': 'pass.1234',
        }
        response = self.client.post(url, data)
        self.assertEqual(User.objects.filter(rut=self.valid_rut).count(), 0)
        self.assertIn("Este campo es obligatorio.", str(response.content))
        self.assertEqual(200, response.status_code)

    def test_register_user_post_method_blank_rut(self):
        url = '/register/'
        data = {
            'first_name': 'Juan',
            'last_name': 'Perez',
            'rut': '',
            'email': self.valid_email,
            'password1': 'pass.1234',
            'password2': 'pass.1234',
        }
        response = self.client.post(url, data)
        self.assertEqual(User.objects.filter(email=self.valid_email).count(), 0)
        self.assertIn("Este campo es obligatorio.", str(response.content))
        self.assertEqual(200, response.status_code)
    
    def test_register_user_post_method_password_mismatch(self):
        url = '/register/'
        data = {
            'first_name': 'Juan',
            'last_name': 'Perez',
            'rut': self.valid_rut,
            'email': self.valid_email,
            'password1': 'pass.1235',
            'password2': 'pass.1234',
        }
        response = self.client.post(url, data)
        self.assertEqual(User.objects.filter(rut=self.valid_rut).count(), 0)
        self.assertIn("as no coinciden.", str(response.content))
        self.assertEqual(200, response.status_code)

    def test_register_user_post_method_password_short(self):
        url = '/register/'
        data = {
            'first_name': 'Juan',
            'last_name': 'Perez',
            'rut': self.valid_rut,
            'email': self.valid_email,
            'password1': 'pass',
            'password2': 'pass',
        }
        response = self.client.post(url, data)
        self.assertEqual(User.objects.filter(rut=self.valid_rut).count(), 0)
        self.assertEqual(200, response.status_code)
    
    def test_register_user_post_method_password_common(self):
        url = '/register/'
        data = {
            'first_name': 'Juan',
            'last_name': 'Perez',
            'rut': self.valid_rut,
            'email': self.valid_email,
            'password1': '123456789',
            'password2': '123456789',
        }
        response = self.client.post(url, data)
        self.assertEqual(User.objects.filter(rut=self.valid_rut).count(), 0)
        self.assertEqual(200, response.status_code)

class LoginUserTestCase(ObjectCreation, TestCase):
    def test_login_user(self):
        url = '/login/'
        data = {
            'rut': self.user.rut,
            'password': 'pass.1234',
        }
        response = self.client.post(url, data)
        self.assertEqual(302, response.status_code)
        self.assertEqual("/", str(response.url))

    def test_login_user_password_invalid(self):
        url = '/login/'
        data = {
            'rut': self.user.rut,
            'password': 'pass.1235',
        }
        response = self.client.post(url, data)
        self.assertEqual(200, response.status_code)
    
    def test_login_user_rut_invalid(self):
        url = '/login/'
        data = {
            'rut': self.invalid_rut,
            'password': 'pass.1234',
        }
        response = self.client.post(url, data)
        self.assertEqual(200, response.status_code)
    
class UserAdminTestCase(ObjectCreation, TestCase):
    def test_user_admin(self):
        user_admin = UserAdmin(model=User, admin_site=AdminSite())
        user_admin.save_model(obj=User(), request=None, form=None, change=None)

class PasswordChangeTestCase(ObjectCreation, TestCase):
    def test_password_change(self):
        self.client.login(username=self.user.rut,
                          password="pass.1234")
        url = '/change-password/'
        data = {
            'old_password': 'pass.1234', 
            'new_password1': 'pass.1235', 
            'new_password2': 'pass.1235'
        }
        response = self.client.post(url,data)
        self.assertEqual(302, response.status_code)

    def test_password_change_password_mismatch(self):
        self.client.login(username=self.user.rut,
                          password="pass.1234")
        url = '/change-password/'
        data = {
            'old_password': 'pass.1234', 
            'new_password1': 'pass.1235', 
            'new_password2': 'pass.1236'
        }
        response = self.client.post(url,data)
        self.assertEqual(200, response.status_code)

    def test_password_change_wrong_old_password(self):
        self.client.login(username=self.user.rut,
                          password="pass.1234")
        url = '/change-password/'
        data = {
            'old_password': 'pass.1235', 
            'new_password1': 'pass.1236', 
            'new_password2': 'pass.1236'
        }
        response = self.client.post(url,data)
        self.assertEqual(200, response.status_code)

    def test_password_change_short_password(self):
        self.client.login(username=self.user.rut,
                          password="pass.1234")
        url = '/change-password/'
        data = {
            'old_password': 'pass.1234', 
            'new_password1': 'pass', 
            'new_password2': 'pass'
        }
        response = self.client.post(url,data)
        self.assertEqual(200, response.status_code)

    def test_password_change_numeric_password(self):
        self.client.login(username=self.user.rut,
                          password="pass.1234")
        url = '/change-password/'
        data = {
            'old_password': 'pass.1234', 
            'new_password1': '123456789', 
            'new_password2': '123456789'
        }
        response = self.client.post(url,data)
        self.assertEqual(200, response.status_code)
