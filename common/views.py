import logging
from django.contrib.auth import authenticate, login, get_user_model, update_session_auth_hash
from django.views.generic import (CreateView, 
                                  FormView, 
                                  TemplateView)
from django.http import (HttpResponseRedirect)
from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render,redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordContextMixin
from .forms import (
                    LoginForm, 
                    RegisterForm,
                    PasswordChangeForm
                    )

class RegisterView(CreateView):
    model = get_user_model()
    form_class = RegisterForm
    template_name = 'common/register.html'
    success_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class LoginView(FormView):
    template_name = "common/login.html"
    form_class = LoginForm
    success_url = '/'
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        request = self.request
        rut  = form.cleaned_data.get("rut")
        password  = form.cleaned_data.get("password")
        user = authenticate(request, username=rut, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        return super(LoginView, self).form_invalid(form)

class PasswordChangeView(PasswordContextMixin, FormView):
    form_class = PasswordChangeForm
    success_url = '/'
    template_name = 'common/change-password.html'
    title = _('Password change')

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        # Updating the password logs out all other sessions for the user
        # except the current one.
        update_session_auth_hash(self.request, form.user)
        return super().form_valid(form)