from django.test import TestCase, Client

from accounts.models import User
from gremios.models import RutGremio


class ObjectsCreation(object):
    def set_up(self):
        self.client = Client()
        self.rut_gremio = RutGremio.objects.create_rut_gremio(rut='17256372-4')