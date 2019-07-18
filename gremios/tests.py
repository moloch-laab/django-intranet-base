from fpdf import FPDF
from django.core.files import File
from django.test import TestCase, Client
import datetime as dt
from django.utils import timezone

from common.models import User
from .models import Cartola, RutGremio


class ObjectsCreation(object):
    def setUp(self):
        self.client = Client()
        self.rut_gremio = RutGremio.objects.create_rut_gremio(rut='12245453-3')
        self.rut_gremios_list = ['15314993-3', '10634630-5', '9619616-4', '16747983-9', '15971053-K', '6597629-3']
        self.invalid_rut_gremios_list = ['1314993-3', '1063630-5', '961966-4', '1677983-9', '1971053-K', '659629-3']
        self.user = self.register_user_post_method()
        self.is_superuser = User.objects.create_superuser(rut='12384351-7',
                                                       email='superuser@test.cl',
                                                       password='pass.1234')
        self.is_staffuser = User.objects.create_staffuser(rut='16747983-9', 
                                                        email='staffuser@test.cl',
                                                        password='pass.1234')

        self.desde = timezone.make_aware(dt.datetime.strptime('20190601', '%Y%m%d'),timezone.get_default_timezone())
        self.hasta = timezone.make_aware(dt.datetime.strptime('20190615', '%Y%m%d'),timezone.get_default_timezone())
        self.cartola_pdf = self.__create_dummy_pdf_file(self.rut_gremio.rut + "_20190601_20190615.pdf")
    
    def register_user_post_method(self):
        url = '/register/'
        data = {
            'first_name': 'Juan',
            'last_name': 'Perez',
            'rut': self.rut_gremio.rut,
            'email': 'test1@test.cl',
            'password1': 'pass.1234',
            'password2': 'pass.1234',
        }
        response = self.client.post(url, data)
        user = User.objects.filter(rut=self.rut_gremio.rut).first()
        user.confirm_email(user.confirmation_key)
        user.is_active = user.is_confirmed
        user.save()
        return user

    def __create_dummy_pdf_file(self, filename):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Dummy File!", ln=1, align="C")
        pdf.output("files/cartolas_gremios/" + filename)
    
    def open_file(self, f):
        return File(open(f, 'rb'))

class GremiosPageTestCase(ObjectsCreation, TestCase):
    def test_gremios_cartolas_page_guest(self):
        response = self.client.get("/gremios/cartolas")
        self.assertEqual(302, response.status_code)
    
    def test_gremios_cartolas_page_authenticated_user(self):
        response = self.client.login(username=self.user.rut, password='pass.1234')
        response = self.client.get("/gremios/cartolas")
        self.assertEqual(200, response.status_code)
    
    def test_gremios_cartolas_page_datatable(self):
        response = self.client.login(username=self.user.rut, password='pass.1234')
        response = self.client.get("/gremios/load")
        response = self.client.get("/gremios/cartolas")
        self.assertIn("12245453-3_20190601_20190615", str(response.content))

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

class CartolasModelTestCase(ObjectsCreation, TestCase):
    def test_create_cartola(self):
        cartola_pdf = self.open_file("files/cartolas_gremios/12245453-3_20190601_20190615.pdf")
        cartola = Cartola.objects.create_cartola(rut_gremio = self.rut_gremio, desde=self.desde, hasta=self.hasta, pdf_file=cartola_pdf, file_name=cartola_pdf.name)
        self.assertEqual(Cartola.objects.filter(rut_gremio_id=self.rut_gremio).count() == 1, True)
    
    def test_create_from_path(self):
        cartolas = Cartola.objects.create_from_path()
        self.assertEqual(Cartola.objects.filter(rut_gremio_id=self.rut_gremio).count() != 0, True)

class LoadCartolasTestCase(ObjectsCreation, TestCase):
    def test_load_cartolas(self):
        response = self.client.get("/gremios/load")
        self.assertEqual(200, response.status_code)
        self.assertIn("Cartolas cargadas", str(response.content))
        self.assertEqual(Cartola.objects.filter(rut_gremio_id=self.rut_gremio).count() == 1, True)
    
    def test_load_cartolas_empty_folder(self):
        response = self.client.get("/gremios/load")
        response = self.client.get("/gremios/load")
        self.assertEqual(200, response.status_code)
        self.assertIn("Error al cargar cartolas", str(response.content))
