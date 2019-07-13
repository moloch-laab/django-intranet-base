import os
import datetime as dt
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.files import File
from django.core.files.storage import FileSystemStorage

from core.utils import ls, valida_rut, rm, rows_from_txt
from common.models import User

class RutGremioManager(models.Manager):
    def create_rut_gremio(self, rut):
        if not valida_rut(rut):
            return "Rut '%s' no válido" % (rut)
        rut_gremio_obj = RutGremio()
        rut_gremio_obj.rut = rut
        rut_gremio_obj.save()
        return rut_gremio_obj
    
    def create_rut_from_file(self, file_path="files/cartolas_gremios/RUTS.txt"):
        rut_rows = rows_from_txt(file_path)
        if rut_rows:
            new_ruts = self.create_from_list(rut_rows)

    def create_from_list(self, rows):
        rut_gremios= []
        for rut in rows:
            if RutGremio.objects.filter(rut = rut).count() == 0:
                rut_gremios.append(self.create_rut_gremio(rut))
        return rut_gremios
    
class RutGremio(models.Model):
    rut       = models.CharField('Rut de gremio', max_length=20, unique=True)
    active    = models.BooleanField(default=True) # can sign in
    timestamp = models.DateTimeField(auto_now_add=True)
    updated   = models.DateTimeField(auto_now=True)
    user_id   = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE, 
                                blank=True, 
                                null=True)
    objects = RutGremioManager()

    def __str__(self):
        return self.rut

class CartolaManager(models.Manager):
    def create_cartola(self, rut_gremio, desde, hasta, pdf_file, file_name):
        cartola_obj               = Cartola()
        cartola_obj.rut_gremio_id = rut_gremio
        cartola_obj.desde         = desde
        cartola_obj.hasta         = hasta
        cartola_obj.pdf_file.save(pdf_file.name, pdf_file)
        cartola_obj.save()
        return cartola_obj

    def create_from_path(self, path_in="files/cartolas_gremios/"):
        cartolas = []
        files = ls(path_in)
        for f in files:
            if f.find(".pdf") > -1:
                # Agregamos el archivo
                pdf_file = self.__open_file(os.path.join(path_in,f))
                # Obtenemos los campos del modelo desde el nombre del archivo
                fields = self.__fields_from_file(f)
                # Obtenemos el Rut de Gremio
                rut_gremio = RutGremio.objects.filter(rut=fields["rut_gremio"]).first()
                # Guardamos los datos en la base de datos
                cartolas.append(self.create_cartola(rut_gremio, 
                                                    fields["desde"], 
                                                    fields["hasta"], 
                                                    pdf_file, f))
                pdf_file.close()
                rm(os.path.join(path_in,f))
        return cartolas
    def __open_file(self, f):
        return File(open(f, 'rb'))

    def __fields_from_file(self, f):
        fields = {}
        fields["rut_gremio"] = f[:f.find("_")]
        f = f[f.find("_") + 1:]
        fields["desde"] = timezone.make_aware(dt.datetime.strptime(f[:f.find("_")], '%Y%m%d'),
                                              timezone.get_default_timezone())
        f = f[f.find("_") + 1:]
        fields["hasta"] =  timezone.make_aware(dt.datetime.strptime(f[:f.find(".")], '%Y%m%d'),
                                               timezone.get_default_timezone())
        return fields

class Cartola(models.Model):
    rut_gremio_id = models.ForeignKey(to=RutGremio,
                                      on_delete=models.CASCADE, 
                                      blank=False, 
                                      null=False)
    desde         = models.DateTimeField('Movimientos desde', auto_now=False, auto_now_add=False)
    hasta         = models.DateTimeField('Movimientos hasta', auto_now=False, auto_now_add=False)
    pub_date      = models.DateTimeField('date published',auto_now_add=True)
    pdf_file      = models.FileField("Archivo PDF de cartola",
                                     upload_to="../media/cartolas_gremios", 
                                     max_length=300)
    active        = models.BooleanField(default=True) # can show in datatable
    updated       = models.DateTimeField(auto_now=True)
    objects       = CartolaManager()
    
    def __str__(self):
        return self.pdf_file.name
