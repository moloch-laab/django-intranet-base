from django.test import TestCase, Client

from accounts.models import User
from .models import Cartola, RutGremio


class ObjectsCreation(object):
    def setUp(self):
        self.client = Client()
        self.rut_gremio = RutGremio.objects.create_rut_gremio(rut='12245453-3')
        self.user = User.objects.create_user(rut='12245453-3', password='pass.1234')
        self.staff_user = User.objects.create_staffuser(rut='16747983-9', password='pass.1234')
        self.super_user = User.objects.create_superuser(rut='17256372-4', password='pass.1234')

class RutGremioModelTestCase(ObjectsCreation, TestCase):
    def test_create_rut_gremio(self):
        RutGremio.objects.create_rut_gremio(rut='5169011-7')
        self.assertEqual(RutGremio.objects.filter(rut='5169011-7').count(), 1)

    def test_create_from_file(self):
        rut_gremios = RutGremio.objects.create_from_file()
        self.assertEqual(RutGremio.objects.all().count() > 1, True)

# class CartolaModelTestCase(ObjectsCreation, TestCase):
    # def test_string_representation_user(self):
    #     user = self.user
    #     self.assertEqual(str(user.get_short_name()), user.rut)

    # def test_create_user(self):
    #     User.objects.create_user(rut='13064499-6', email='test@test.cl', full_name='Test Testo', password='pass.1234')
    #     self.assertEqual(User.objects.all().filter(rut='13064499-6').count() != 0, True)

