from django.urls import path
from .views import HomePageView

app_name = 'core'

core_patterns = ([
    path('', HomePageView.as_view(), name="home"),
], 'core')