from django.urls import include, path

from .views import (
                    LoginView, 
                    RegisterView, 
                    PasswordChangeView,
                    Activate
                    )
from django.contrib.auth.views import LogoutView

common_patterns = ([
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('change-password/', PasswordChangeView.as_view(), name='change-password'),
    path('activate/<str:uidb64>/<str:token>', Activate.as_view(), name='activate'),
    path('logout/', LogoutView.as_view(), name='logout'),
], 'common')