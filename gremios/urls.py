from django.urls import path
from .views import CartolasListView, load_cartolas

gremios_patterns = ([
    path('cartolas', CartolasListView.as_view()),
    path('load', load_cartolas),
], 'gremios')