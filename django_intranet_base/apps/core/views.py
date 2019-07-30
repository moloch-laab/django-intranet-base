import logging
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from django_intranet_base.apps.general_functions import get_client_ip


class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = "core/home.html"
    log_message = "GET Home Page User: {0} From: {1}"
    def get(self, request, *args, **kwargs):
        logging.getLogger("info_logger").info(self.log_message.format(request.user.rut, get_client_ip(request)))
        return render(request, self.template_name)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            logging.getLogger("error_logger").error(self.log_message.format(request.user, get_client_ip(request)))
        return super().dispatch(request, *args, **kwargs)
