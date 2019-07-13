#!/usr/bin/env python
import sys
import stat
from os import scandir, getcwd, chmod, remove
from os.path import abspath
from itertools import cycle

def ls(ruta = getcwd()):
	""" Return a list with file names in a path """
	return [arch.name for arch in scandir(ruta) if arch.is_file()]

def ls_a(ruta = getcwd()):
	""" Return a list with full file names in a path """
	return [abspath(arch.path) for arch in scandir(ruta) if arch.is_file()]

def rm(ruta = getcwd()):
	""" chmod 777 and remove file """
	chmod(ruta, 0o777)
	return remove(ruta)

def rows_from_txt(ruta = getcwd()):
	""" Return a list with rows in text file """
	try:
		file_txt = open(ruta, 'r')
	except FileNotFoundError:
		return False
	file_rows = []
	for row in file_txt:
		row = row.replace("\n","")
		file_rows.append(row)
	file_txt.close()
	return file_rows

def valida_rut(rut):
	""" Return true if the argument is a valid rut or false if not """
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
	""" Return true if argument is in RutGremio model or false if not """
	from gremios.models import RutGremio
	rut_gremio = RutGremio.objects.filter(rut = rut).first()
	if rut_gremio:
		if rut_gremio.active:
			return True
		else:
			return False
	else:
		return False