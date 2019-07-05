from django.test import TestCase, Client

from accounts.models import User
from .models import Cartola, RutGremio


class ObjectsCreation(object):
    def setUp(self):
        self.client = Client()
        self.rut_gremio = RutGremio.objects.create_rut_gremio(rut='12245453-3')
        self.rut_gremios_list = ['15314993-3', '10634630-5', '9619616-4', '16747983-9', '15971053-K', '6597629-3']
        self.invalid_rut_gremios_list = ['1314993-3', '1063630-5', '961966-4', '1677983-9', '1971053-K', '659629-3']
        self.user = User.objects.create_user(rut='12245453-3', password='pass.1234')
        self.staff_user = User.objects.create_staffuser(rut='16747983-9', password='pass.1234')
        self.super_user = User.objects.create_superuser(rut='17256372-4', password='pass.1234')

class RutGremioModelTestCase(ObjectsCreation, TestCase):
    def test_create_rut_gremio(self):
        RutGremio.objects.create_rut_gremio(rut='5169011-7')
        self.assertEqual(RutGremio.objects.filter(rut='5169011-7').count(), 1)

    def test_create_rut_gremio_rut_not_valid(self):
        rut_gremio = RutGremio.objects.create_rut_gremio(rut='111-k')
        self.assertIn("no válido", rut_gremio)

    def test_create_from_list(self):
        rut_gremios = RutGremio.objects.create_from_list(self.rut_gremios_list)
        self.assertEqual(len(rut_gremios) > 0, True)
    
    def test_create_from_list_rut_not_valid(self):
        rut_gremios = RutGremio.objects.create_from_list(self.invalid_rut_gremios_list)
        not_valid = False
        for rut in rut_gremios:
            if type(rut) == str:
                not_valid = True
        self.assertEqual(not_valid, True)

# class CartolaModelTestCase(ObjectsCreation, TestCase):
    # def test_string_representation_user(self):
    #     user = self.user
    #     self.assertEqual(str(user.get_short_name()), user.rut)

    # def test_create_user(self):
    #     User.objects.create_user(rut='13064499-6', email='test@test.cl', full_name='Test Testo', password='pass.1234')
    #     self.assertEqual(User.objects.all().filter(rut='13064499-6').count() != 0, True)

