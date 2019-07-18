import logging
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.shortcuts import render
from django.http import HttpResponse

from .models import Cartola, RutGremio
from core.utils import rows_from_txt, get_client_ip

class CartolasListView(LoginRequiredMixin, ListView):
    model = Cartola
    log_message = "GET Cartola List Page User: {0} From: {1}"

    def get_queryset(self):
        rut_gremio = RutGremio.objects.filter(user_id=self.request.user).first()
        logging.getLogger("info_logger").info(self.log_message.format(self.request.user.rut, get_client_ip(self.request)))
        return Cartola.objects.filter(rut_gremio_id=rut_gremio)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            logging.getLogger("error_logger").error(self.log_message.format(request.user, get_client_ip(request)))
        return super().dispatch(request, *args, **kwargs)
    
class LoadCartolasView(TemplateView):
    log_message = "{0} From: {1}"
    def get(self, request, *args, **kwargs):
        model = Cartola()
        new_ruts = RutGremio.objects.create_rut_from_file()
        resultado = Cartola.objects.create_from_path()
        log_message = "GET Load Cartolas Message: {0} From: {1}"

        if resultado:
            logging.getLogger("info_logger").info(self.log_message.format('Cartolas cargadas', get_client_ip(request)))
            return HttpResponse('Cartolas cargadas')

        else:
            logging.getLogger("error_logger").error(self.log_message.format('Error al cargar cartolas', get_client_ip(request)))
            return HttpResponse('Error al cargar cartolas')