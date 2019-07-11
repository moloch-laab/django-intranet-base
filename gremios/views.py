from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.shortcuts import render
from django.http import HttpResponse
import logging

from .models import Cartola, CartolaManager, RutGremioManager
from core.utils import rows_from_txt

class CartolasListView(LoginRequiredMixin, ListView):
    model = Cartola

    def get_queryset(self):
        logging.getLogger("info_logger").info("User: " + self.request.user.rut)
        return Cartola.objects.filter(rut_gremio=self.request.user.rut)
    
class LoadCartolasView(TemplateView):
    def get(self, request, *args, **kwargs):
        model = CartolaManager()
        rut_gremios = RutGremioManager()
        new_ruts = rut_gremios.create_rut_from_file()
        resultado = model.create_from_path()
        if resultado:
            logging.getLogger("info_logger").info('Cartolas cargadas')
            return HttpResponse('Cartolas cargadas')
        else:
            logging.getLogger("error_logger").error('Error al cargar cartolas')
            return HttpResponse('Error al cargar cartolas')