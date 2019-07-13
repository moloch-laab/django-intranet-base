from django.test import TestCase, Client

from common.models import User

class ObjectCreation(object):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(rut='7264437-9', 
                                             email='test1@test.cl', 
                                             first_name='Test', 
                                             last_name='Testo', 
                                             password='pass.1234')
        self.superuser = User.objects.create_superuser(rut='12384351-7',
                                                       email='superuser@test.cl',
                                                       password='pass.1234')
        self.staffuser = User.objects.create_staffuser(rut='16747983-9', 
                                                       email='staffuser@test.cl',
                                                       password='pass.1234')

    def login(self, username='7264437-9', password='pass.1234'):
        url = '/login/'
        data = {
            'rut': username,
            'password': password
        }
        self.client.post(url,data)

    def register_user_post_method(self):
        url = '/register/'
        data = {
            'first_name': 'Juan',
            'last_name': 'Perez',
            'rut': '13064499-6',
            'email': 'test2@test.cl',
            'password1': 'pass.1234',
            'password2': 'pass.1234',
        }
        self.client.post(url, data)

class HomeViewTestCase(ObjectCreation, TestCase):
    def test_home_page_guest(self):
        response = self.client.get('/')
        self.assertEqual(302, response.status_code)
        self.assertIn("/login/", str(response.url))

    def test_home_page_login_user(self):
        response = self.login()
        response = self.client.get('/')
        self.assertEqual(200, response.status_code)

    def test_home_page_login_inactive_user(self):
        response = self.register_user_post_method
        response = self.login(username='13064499-6', password='pass.1234')
        response = self.client.get('/')
        self.assertEqual(302, response.status_code)
        self.assertIn("/login/", str(response.url))

class AdminPageTestCase(ObjectCreation, TestCase):
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
            'rut': self.staffuser.rut, 
            'password': 'pass.1234',
        }
        response = self.client.post('/login/', data)
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)

    def test_admin_page_pass_if_super_user(self):
        data = {
            'rut': self.superuser.rut, 
            'password': 'pass.1234',
        }
        response = self.client.post('/login/', data)
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)
