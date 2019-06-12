from django.views.generic.list import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from core.decorators import group_required
from django.shortcuts import render
from .models import Cartola, CartolaManager

@method_decorator(group_required("Gremios"), name='dispatch')
class CartolasListView(LoginRequiredMixin, ListView):
    model = Cartola

def load_cartolas(request):
    model = CartolaManager()
    resultado = model.create_from_files()
    if resultado:
        return render(request, 'cartolas_gremios/cartolas_load.html', resultado)
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')