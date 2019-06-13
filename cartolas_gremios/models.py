from django.db import models
from core.utils import ls
import os, shutil
import datetime as dt

class CartolaManager():
    def create_cartola(self, rut, desde, hasta, path):
        cartola_obj = Cartola()
        cartola_obj.rut = rut
        cartola_obj.desde = desde
        cartola_obj.hasta = hasta
        cartola_obj.path = path
        cartola_obj.save()

    def create_from_files(self, path_in="files/cartolas_gremios/", path_out = "core/media/cartolas_gremios/"):
        try:
            files = ls(path_in)
            for f in files:
                # Obtenemos rut, desde y hasta del nombre de cada archivo
                fs = f
                rut = fs[:fs.find("_")]
                fs = fs[fs.find("_") + 1:]
                desde = fs[:fs.find("_")]
                fs = fs[fs.find("_") + 1:]
                hasta = fs[:fs.find(".")]
                # Definimos los direcorios de los archivos de entrada y salida
                file_preproc = path_in + f
                file_proc = path_out + rut + "/" + f

                # Creamos una carpeta para el rut del gremio si esta no existe
                try:
                    os.stat(path_out + rut)
                except:
                    os.mkdir(path_out + rut)
                # breakpoint()
                # Convertimos las cadenas en fechas
                desde_dt = dt.datetime.strptime(desde, '%Y%m%d')
                hasta_dt = dt.datetime.strptime(hasta, '%Y%m%d')

                # Guardamos los datos en la base de datos
                cartola = self.create_cartola(rut, desde_dt, hasta_dt, file_proc)
                
                # Movemos el archivo a la carpeta media
                shutil.move(file_preproc, file_proc)
                # breakpoint()
                # Verificamos si el archivo fue movido
                if os.path.exists(file_proc):
                    pass
                else:
                    return False
            # breakpoint()
            return True
        except:
            return False
        


class Cartola(models.Model):
    rut = models.CharField("Rut de gremio", max_length=50)
    desde = models.DateTimeField('Movimientos desde', auto_now=False, auto_now_add=False)
    hasta = models.DateTimeField("Movimientos hasta", auto_now=False, auto_now_add=False)
    pub_date = models.DateTimeField('date published',auto_now_add=True)
    path = models.CharField("Directorio de archivo de cartolas", null=True, max_length=200)
    
    

