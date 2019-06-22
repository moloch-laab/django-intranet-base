from django.views.generic.list import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.http import HttpResponse

from .models import Cartola, CartolaManager
from core.decorators import group_required

@method_decorator(group_required("Gremios"), name='dispatch')
class CartolasListView(LoginRequiredMixin, ListView):
    model = Cartola

def load_cartolas(request):
    model = CartolaManager()
    resultado = model.create_from_files()
    if resultado:
        return render(request, 'cartolas_gremios/cartolas_load.html')
    else:
        return HttpResponse('<h1>Error al cargar cartolas</h1>')