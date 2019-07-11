from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.shortcuts import render
from django.http import HttpResponse

from .models import Cartola, CartolaManager, RutGremioManager
from core.utils import rows_from_txt

class CartolasListView(LoginRequiredMixin, ListView):
    model = Cartola

    def get_queryset(self):
        return Cartola.objects.filter(rut_gremio=self.request.user.rut)
    
class LoadCartolasView(TemplateView):
    def get(self, request, *args, **kwargs):
        model = CartolaManager()
        rut_gremios = RutGremioManager()
        new_ruts = rut_gremios.create_rut_from_file()
        resultado = model.create_from_files()
        if resultado:
            return HttpResponse('Cartolas cargadas')
        else:
            return HttpResponse('Error al cargar cartolas')