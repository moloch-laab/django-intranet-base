from django.db import models
from utils import ls
import os, shutil

class CartolaManager():
    def create_cartola(self, rut, desde, hasta, path):
        cartola_obj = Cartola()
        cartola_obj.rut = rut
        cartola_obj.desde = desde
        cartola_obj.hasta = hasta
        cartola_obj.path = path
        cartola_obj.save()

    def create_from_files(self, path_in="files/cartolas_gremios/", path_out = "core/static/cartolas_gremios/"):
        try:
            files = self.ls(path_in)
            file_array = []
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

                # Guardamos los datos en la base de datos
                cartola = self.create_cartola(rut, desde, hasta, file_proc)

                # Movemos el archivo a la carpeta static
                shutil.move(file_preproc, file_proc)

                # Verificamos si el archivo fue movido y llenamos el array para retornar
                if os.path.exists(file_proc):
                    file_array.append(file_proc)
                else:
                    return False
            return file_array
        except:
            return False
        


class Cartola(models.Model):
    rut = models.CharField("Rut de gremio", max_length=50)
    desde = models.DateTimeField('Movimientos desde', auto_now=False, auto_now_add=False)
    hasta = models.DateTimeField("Movimientos hasta", auto_now=False, auto_now_add=False)
    pub_date = models.DateTimeField('date published',auto_now_add=True)
    path = models.CharField("Directorio de archivo de cartolas", null=True, max_length=200)
    
    

