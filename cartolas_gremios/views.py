from django.views.generic.list import ListView
from .models import Cartola

class CartolasListView(ListView):
    model = Cartola
