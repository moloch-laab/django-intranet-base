from django.urls import path
from django.contrib.auth import urls
from .views import (LoginView, 
                    RegisterView, 
                    ChangePasswordView)
from django.contrib.auth.views import LogoutView

accounts_patterns = ([
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('logout/', LogoutView.as_view(), name='logout'),
], 'accounts')