from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.shortcuts import render
from django.http import HttpResponse
import logging

from .models import Cartola, RutGremio
from core.utils import rows_from_txt

class CartolasListView(LoginRequiredMixin, ListView):
    model = Cartola

    def get_queryset(self):
        logging.getLogger("info_logger").info("Cartolas Gremios User: " + self.request.user.rut)
        rut_gremio = RutGremio.objects.filter(user_id=self.request.user).first()
        return Cartola.objects.filter(rut_gremio_id=rut_gremio)
    
class LoadCartolasView(TemplateView):
    def get(self, request, *args, **kwargs):
        model = Cartola()
        new_ruts = RutGremio.objects.create_rut_from_file()
        resultado = Cartola.objects.create_from_path()
        if resultado:
            logging.getLogger("info_logger").info('Cartolas cargadas')
            return HttpResponse('Cartolas cargadas')
        else:
            logging.getLogger("error_logger").error('Error al cargar cartolas')
            return HttpResponse('Error al cargar cartolas')