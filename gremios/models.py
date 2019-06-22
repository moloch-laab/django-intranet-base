from django.db import models
from core.utils import ls
from django.core.files import File
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from accounts.models import User
import os, shutil
import datetime as dt

class RutGremioManager(models.Manager):
    def create_rut_gremio(self, rut):
        rut_gremio_obj = RutGremio()
        rut_gremio_obj.rut = rut
        rut_gremio_obj.save()
        return rut_gremio_obj

    def create_from_file(self, file_path="files/cartolas_gremios/RUTS.txt"):
        pass


class RutGremio(models.Model):
    rut = models.CharField('Rut de gremio', max_length=20, unique=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    objects = RutGremioManager()

class CartolaManager(models.Manager):
    def create_cartola(self, rut_gremio, desde, hasta, pdf_file, file_name):
        cartola_obj = Cartola()
        cartola_obj.rut_gremio = rut_gremio
        cartola_obj.desde = desde
        cartola_obj.hasta = hasta
        cartola_obj.pdf_file.save(pdf_file.name, pdf_file)
        cartola_obj.save()
        return cartola_obj

    def create_from_files(self, path_in="files/cartolas_gremios/"):
        cartolas = []
        files = ls(path_in)
        for f in files:
            # Obtenemos rut, desde y hasta del nombre de cada archivo
            fs = f
            rut_gremio = fs[:fs.find("_")]
            fs = fs[fs.find("_") + 1:]
            desde = fs[:fs.find("_")]
            fs = fs[fs.find("_") + 1:]
            hasta = fs[:fs.find(".")]
            # Definimos los direcorios de los archivos de entrada y salida
            file_preproc = path_in + f
            # Convertimos las cadenas en fechas
            desde_dt = dt.datetime.strptime(desde, '%Y%m%d')
            hasta_dt = dt.datetime.strptime(hasta, '%Y%m%d')
            file_name = rut_gremio + "_" + desde + "_" + hasta + ".pdf"
            # Agregamos el archivo
            pdf_file = open(file_preproc, 'rb')
            pdf_file = File(pdf_file)
            # Guardamos los datos en la base de datos
            cartolas.append(self.create_cartola(rut_gremio, desde_dt, hasta_dt, pdf_file, file_name))
        return cartolas

class Cartola(models.Model):
    rut_gremio = models.CharField(max_length=20)
    desde = models.DateTimeField('Movimientos desde', auto_now=False, auto_now_add=False)
    hasta = models.DateTimeField("Movimientos hasta", auto_now=False, auto_now_add=False)
    pub_date = models.DateTimeField('date published',auto_now_add=True)
    pdf_file = models.FileField("Archivo PDF de cartola", upload_to=settings.MEDIA_ROOT + "/cartolas_gremios", max_length=300)

    objects = CartolaManager()
