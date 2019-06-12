from django.urls import path
from .views import CartolasListView, load_cartolas

cartolas_gremios_patterns = ([
    path('', CartolasListView.as_view(), name='cartolas_gremios'),
    path('load', load_cartolas),
], 'cartolas_gremios')