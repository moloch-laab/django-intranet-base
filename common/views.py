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

from core.utils import get_client_ip
from .forms import (
                    LoginForm, 
                    RegisterForm,
                    PasswordChangeForm
                    )
from gremios.models import RutGremio

class RegisterView(CreateView):
    model = get_user_model()
    form_class = RegisterForm
    template_name = 'common/register.html'
    success_url = '/login/'
    log_message = "Register User: {0} From: {1}"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    def form_valid(self, form):
        user = form.save()
        logging.getLogger("info_logger").info(self.log_message.format(user.rut, get_client_ip(self.request)))
        rut_gremio = RutGremio.objects.filter(rut=form.cleaned_data.get("rut")).first()
        rut_gremio.user_id = user
        rut_gremio.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        rut = form.cleaned_data.get("rut")
        logging.getLogger("error_logger").error(self.log_message.format(rut, get_client_ip(self.request)))
        return super().form_invalid(form)

class LoginView(FormView):
    template_name = "common/login.html"
    form_class = LoginForm
    success_url = '/'
    log_message = "Login User: {0} From: {1}"
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
            logging.getLogger("info_logger").info(self.log_message.format(user.rut, get_client_ip(self.request)))
            return redirect("/")
        return super(LoginView, self).form_invalid(form)

    def form_invalid(self, form):
        rut = form.cleaned_data.get("rut")
        logging.getLogger("error_logger").error(self.log_message.format(rut, get_client_ip(self.request)))
        return super().form_invalid(form)

class PasswordChangeView(PasswordContextMixin, FormView):
    form_class = PasswordChangeForm
    success_url = '/'
    template_name = 'common/change-password.html'
    title = _('Password change')
    log_message = "Password Change User: {0} From: {1}"

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
        logging.getLogger("info_logger").info(self.log_message.format(self.request.user.rut, get_client_ip(self.request)))
        return super().form_valid(form)
    
    def form_invalid(self, form):
        rut = form.cleaned_data.get("rut")
        logging.getLogger("error_logger").error(self.log_message.format(rut, get_client_ip(self.request)))
        return super().form_invalid(form)