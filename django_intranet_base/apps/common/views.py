import logging
from django.core.mail import send_mail
from django.views.generic import (CreateView, 
                                  FormView, 
                                  TemplateView,
                                  View)
from django.http import (HttpResponseRedirect)
from django.shortcuts import render, redirect, resolve_url
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.utils.encoding import force_bytes, force_text
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth import (authenticate,
                                 login, 
                                 get_user_model, 
                                 update_session_auth_hash)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordContextMixin
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site

from django_intranet_base.apps.general_functions import get_client_ip
from .forms import (
                    LoginForm, 
                    RegisterForm,
                    PasswordChangeForm
                    )
#from gremios.models import RutGremio

User = get_user_model()

class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'common/register.html'
    success_url = '/login/'
    log_message = "Register User: {0} From: {1}"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        user = form.save()
        self.__confirmation_email_sender(user)
        logging.getLogger("info_logger").info(self.log_message.format(user.rut, get_client_ip(self.request)))
        super().form_valid(form)
        return render(self.request, 'common/redirect.html', {'message': 'Debe validar su dirección de correo.', 
                                                             'url_redirect': resolve_url('common:login')})

    def form_invalid(self, form):
        rut = form.cleaned_data.get("rut")
        logging.getLogger("error_logger").error(self.log_message.format(rut, get_client_ip(self.request)))
        return super().form_invalid(form)

    def __confirmation_email_sender(self, user):
        current_site = get_current_site(self.request)
        mail_message = {
            "subject": "Active su cuenta",
            "message": render_to_string('common/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':user.confirmation_key,
            })
        }
        try:
            send_mail(mail_message["subject"], mail_message["message"], None, (user.email,))
        except:
            return logging.getLogger("error_logger").error("Error sending mail to: {0}".format(user.email))
        logging.getLogger("info_logger").info("Mail send to: {0}".format(user.email))
        

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

class Activate(View):
    log_message = "User activate: {0} From: {1}"
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            user_email = user.confirm_email(token)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and user.is_confirmed:
            user.is_active = True
            user.save()
            login(request, user)
            logging.getLogger("info_logger").info(self.log_message.format(user.rut, get_client_ip(self.request)))
            return render(request, 'common/redirect.html', {'message': 'Su cuenta ha sido activada.', 
                                                            'url_redirect': resolve_url('core:home')})
        else:
            logging.getLogger("error_logger").error(self.log_message.format(None, get_client_ip(self.request)))
            return HttpResponse('Enlace de activación inválido!')
