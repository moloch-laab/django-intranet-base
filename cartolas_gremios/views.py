from django.views.generic.list import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from core.decorators import group_required
from django.shortcuts import render
from .models import Cartola

@method_decorator(group_required("Gremios"), name='dispatch')
class CartolasListView(LoginRequiredMixin, ListView):
    model = Cartola