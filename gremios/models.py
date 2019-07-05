import os
import datetime as dt
from django.db import models
from django.core.files import File
from django.core.files.storage import FileSystemStorage

from core.utils import ls, valida_rut, rm
from accounts.models import User

class RutGremioManager(models.Manager):
    def create_rut_gremio(self, rut):
        if not valida_rut(rut):
            raise ValueError("Rut '%s' no válido" % (rut))
        rut_gremio_obj = RutGremio()
        rut_gremio_obj.rut = rut
        rut_gremio_obj.save()
        return rut_gremio_obj

    def create_from_file(self, file_path="files/cartolas_gremios/RUTS.txt"):
        rut_file = open(file_path, 'r')
        rut_gremios= []
        for row in rut_file:
            row = row.replace("\n","")
            if RutGremio.objects.filter(rut = row).count() == 0:
                rut_gremios.append(self.create_rut_gremio(row))
        rut_file.close()
        rm(os.path.join(file_path))
        return rut_gremios
    

class RutGremio(models.Model):
    rut = models.CharField('Rut de gremio', max_length=20, unique=True)

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
            if f.find(".pdf") > -1:
                # Definimos los directorios de los archivos de entrada y salida
                file_preproc = path_in + f
                # Agregamos el archivo
                pdf_file = open(file_preproc, 'rb')
                pdf_file = File(pdf_file)
                # Obtenemos los campos del modelo desde el nombre del archivo
                fields = self.__fields_from_file(f)
                # Guardamos los datos en la base de datos
                cartolas.append(self.create_cartola(fields["rut_gremio"], fields["desde"], fields["hasta"], pdf_file, f))
                pdf_file.close()
                rm(os.path.join(path_in,f))
        return cartolas

    def __fields_from_file(self, f):
        fields = {}
        fields["rut_gremio"] = f[:f.find("_")]
        f = f[f.find("_") + 1:]
        fields["desde"] = dt.datetime.strptime(f[:f.find("_")], '%Y%m%d')
        f = f[f.find("_") + 1:]
        fields["hasta"] = dt.datetime.strptime(f[:f.find(".")], '%Y%m%d')
        return fields

class Cartola(models.Model):
    rut_gremio = models.CharField(max_length=20)
    desde = models.DateTimeField('Movimientos desde', auto_now=False, auto_now_add=False)
    hasta = models.DateTimeField("Movimientos hasta", auto_now=False, auto_now_add=False)
    pub_date = models.DateTimeField('date published',auto_now_add=True)
    pdf_file = models.FileField("Archivo PDF de cartola", upload_to="../media/cartolas_gremios", max_length=300)

    objects = CartolaManager()
