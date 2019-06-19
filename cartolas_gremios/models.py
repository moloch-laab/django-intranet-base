from django.db import models
from core.utils import ls
from django.core.files import File
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from accounts.models import User
import os, shutil
import datetime as dt

class CartolaManager(models.Manager):
    def create_cartola(self, user_id, desde, hasta, pdf_file, file_name):
        cartola_obj = Cartola()
        cartola_obj.user_id = user_id
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
            rut = fs[:fs.find("_")]
            fs = fs[fs.find("_") + 1:]
            desde = fs[:fs.find("_")]
            fs = fs[fs.find("_") + 1:]
            hasta = fs[:fs.find(".")]
            # Obtenemos el id de usuario de la cartola
            # breakpoint()
            user_obj = User.objects.filter(rut=rut).first()
            # Definimos los direcorios de los archivos de entrada y salida
            file_preproc = path_in + f
            # Convertimos las cadenas en fechas
            desde_dt = dt.datetime.strptime(desde, '%Y%m%d')
            hasta_dt = dt.datetime.strptime(hasta, '%Y%m%d')
            file_name = rut + "_" + desde + "_" + hasta + ".pdf"
            # Agregamos el archivo
            pdf_file = open(file_preproc, 'rb')
            pdf_file = File(pdf_file)
            # Guardamos los datos en la base de datos
            cartolas.append(self.create_cartola(user_obj, desde_dt, hasta_dt, pdf_file, file_name))
        return cartolas

class Cartola(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    desde = models.DateTimeField('Movimientos desde', auto_now=False, auto_now_add=False)
    hasta = models.DateTimeField("Movimientos hasta", auto_now=False, auto_now_add=False)
    pub_date = models.DateTimeField('date published',auto_now_add=True)
    pdf_file = models.FileField("Archivo PDF de cartola", upload_to=settings.MEDIA_ROOT + "/cartolas_gremios", max_length=300)

    objects = CartolaManager()
