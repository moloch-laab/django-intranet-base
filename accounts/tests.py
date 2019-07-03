from django.test import TestCase, Client

from accounts.models import User
from gremios.models import RutGremio


class ObjectsCreation(object):
    def set_up(self):
        self.client = Client()
        self.rut_gremio = RutGremio.objects.create_rut_gremio(rut='12245453-3')
        self.user = User.objects.create_user(rut='12245453-3', password='pass.1234')
        self.staff_user = User.objects.create_staffuser(rut='16747983-9', password='pass.1234')
        self.super_user = User.objects.create_superuser(rut='17256372-4', password='pass.1234')

class TestHomePage(ObjectsCreation, TestCase):
    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        if response.status_code == 200:
            self.assertIn("", str(response.content))