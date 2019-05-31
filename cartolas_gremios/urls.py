from django.urls import path
from . import views
from .views import CartolasListView

urlpatterns = [
    path('', CartolasListView.as_view(), name='cartolas_gremios'),
]