#!/usr/bin/env python
import sys
import stat
from os import scandir, getcwd, chmod, remove
from os.path import abspath
from itertools import cycle



def ls(ruta = getcwd()):
    return [arch.name for arch in scandir(ruta) if arch.is_file()]

def ls_a(ruta = getcwd()):
    return [abspath(arch.path) for arch in scandir(ruta) if arch.is_file()]

def rm(ruta = getcwd()):
	chmod(ruta, stat.S_IWRITE)
	return remove(ruta)

def valida_rut(rut):
	rut = rut.upper()
	rut = rut.replace("-","")
	rut = rut.replace(".","")
	aux = rut[:-1]
	dv = rut[-1:]
 
	revertido = map(int, reversed(str(aux)))
	factors = cycle(range(2,8))
	s = sum(d * f for d, f in zip(revertido,factors))
	res = (-s)%11
 
	if str(res) == dv:
		return True
	elif dv=="K" and res==10:
		return True
	else:
		return False

def valida_rut_gremio(rut):
	from gremios.models import RutGremio
	if RutGremio.objects.filter(rut__contains = rut).count() > 0:
		return True
	else:
		return False
	return true