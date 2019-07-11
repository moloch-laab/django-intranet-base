import logging
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = "core/home.html"
    def get(self, request, *args, **kwargs):
        logging.getLogger("info_logger").info("Home Page User: " + self.request.user.rut)
        return render(request, self.template_name)
