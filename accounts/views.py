from django.contrib.auth import authenticate, login, get_user_model
from django.views.generic import (CreateView, 
                                  FormView, 
                                  TemplateView)
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.utils.http import is_safe_url
from django.contrib.auth.mixins import LoginRequiredMixin

from core.mixins import NextUrlMixin, RequestFormAttachMixin
from .forms import (LoginForm, 
                    RegisterForm,
                    ChangePasswordForm)

class LoginView(NextUrlMixin, RequestFormAttachMixin, FormView):
    form_class = LoginForm
    success_url = '/'
    template_name = 'accounts/login.html'
    default_next = '/'

    # def form_valid(self, form):
    #     next_path = self.get_next_url()
    #     return redirect(next_path)
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        request = self.request
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None
        rut  = form.cleaned_data.get("rut")
        password  = form.cleaned_data.get("password")
        user = authenticate(request, username=rut, password=password)
        if user is not None:
            login(request, user)
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect("/")
        return super(LoginView, self).form_invalid(form)

class RegisterView(CreateView):
    model = get_user_model()
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Registro'
        return context

class ChangePasswordView(LoginRequiredMixin, FormView):
    template_name = "accounts/change_password.html"
    form_class = ChangePasswordForm
    def get_context_data(self, **kwargs):
        context = super(ChangePasswordView, self).get_context_data(**kwargs)
        return context
    
    def post(self, request, *args, **kwargs):
        error, errors = "", ""
        form = ChangePasswordForm(request.POST, user=request.user)
        if form.is_valid():
            user = request.user
            user.set_password(request.POST.get('password2'))
            user.active = True
            user.save()
            return HttpResponseRedirect('/login/?next=/&passchanged=True')
        else:
            errors = form.errors
        return render(request, self.template_name,
                      {'error': error, 'errors': errors,
                       'change_password_form': form})