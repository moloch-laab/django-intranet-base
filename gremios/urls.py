from django.urls import path
from .views import CartolasListView, LoadCartolasView

gremios_patterns = ([
    path('cartolas', CartolasListView.as_view(), name="cartolas"),
    path('load', LoadCartolasView.as_view(), name="load"),
], 'gremios')