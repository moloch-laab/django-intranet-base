from django.urls import path
from .views import HomePageView

core_patterns = ([
    path('', HomePageView.as_view(), name="home"),
], 'core')