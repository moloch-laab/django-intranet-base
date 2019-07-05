from django.views.generic.list import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.http import HttpResponse

from .models import Cartola, CartolaManager, RutGremioManager
from core.decorators import group_required
from core.utils import rows_from_txt

# @method_decorator(group_required("Gremios"), name='dispatch')
class CartolasListView(LoginRequiredMixin, ListView):
    model = Cartola

    def get_queryset(self):
        return Cartola.objects.filter(rut_gremio=self.request.user.rut)
    

def load_cartolas(request):
    model = CartolaManager()
    rut_gremios = RutGremioManager()
    rut_rows = rows_from_txt("files/cartolas_gremios/RUTS.txt")
    if rut_rows:
        new_ruts = rut_gremios.create_from_list(rut_rows)
    resultado = model.create_from_files()
    if resultado:
        return render(request, 'gremios/cartolas_load.html')
    else:
        return HttpResponse('<h1>Error al cargar cartolas</h1>')