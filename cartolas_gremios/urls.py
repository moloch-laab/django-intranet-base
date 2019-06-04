from django.urls import path
from .views import CartolasListView

cartolas_gremios_patterns = ([
    path('', CartolasListView.as_view(), name='cartolas_gremios'),
], 'cartolas_gremios')