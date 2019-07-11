from django.test import TestCase, Client

from common.models import User
from .models import Cartola, RutGremio


class ObjectsCreation(object):
    def setUp(self):
        self.client = Client()
        self.rut_gremio = RutGremio.objects.create_rut_gremio(rut='12245453-3')
        self.rut_gremios_list = ['15314993-3', '10634630-5', '9619616-4', '16747983-9', '15971053-K', '6597629-3']
        self.invalid_rut_gremios_list = ['1314993-3', '1063630-5', '961966-4', '1677983-9', '1971053-K', '659629-3']
        self.user = User.objects.create_user(rut='12245453-3', password='pass.1234')
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

class GremiosPageTestCase(ObjectsCreation, TestCase):
    def test_gremios_cartolas_page_guest(self):
        response = self.client.get("/gremios/cartolas")
        self.assertEqual(302, response.status_code)
    
    def test_gremios_cartolas_page_authenticated_user(self):
        response = self.client.login(username=self.user.rut, password='pass.1234')
        response = self.client.get("/gremios/cartolas")
        self.assertEqual(200, response.status_code)

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

class LoadCartolasTestCase(ObjectsCreation, TestCase):
    def test_load_cartolas(self):
        response = self.client.get("/gremios/load")
        self.assertEqual(200, response.status_code)
