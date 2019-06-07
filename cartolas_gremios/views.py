from django.views.generic.list import ListView
from .models import Cartola

class CartolasListView(ListView):
    model = Cartola

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Cartolas'
        return context
