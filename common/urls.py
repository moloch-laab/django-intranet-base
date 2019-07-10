from django.urls import path
from django.contrib.auth import urls
from .views import (
                    LoginView, 
                    RegisterView, 
                    PasswordChangeView
                    )
from django.contrib.auth.views import LogoutView

common_patterns = ([
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('change-password/', PasswordChangeView.as_view(), name='change-password'),
    path('logout/', LogoutView.as_view(), name='logout'),
], 'common')