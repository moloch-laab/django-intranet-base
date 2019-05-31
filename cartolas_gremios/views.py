from django.views.generic.list import ListView
from django.shortcuts import render
from .models import Document

class CartolasListView(ListView):
    model = Document
