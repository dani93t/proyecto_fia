#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random as rd
from os import listdir
import numpy as np
from time import time
import os
import sys
from solucion import *
from metaheuristica import *
import argparse
from jproperties import Properties # para leer las propiedades


class Instancia(object):
	"""docstring for Instancia"""
	def __init__(self, directorio):
		super(Instancia, self).__init__()
		self.directorio = directorio
		inst = cargar_matriz(self.directorio)
		self.machines = inst['Machines']
		self.parts = inst['Parts']
		self.cells = inst['Cells']
		self.mMax = inst['Mmax']
		self.bSol = inst['Best Solution']
		self.matrix = inst['Matrix']
		print ("Máquinas: ",self.machines ,"\t Partes: ",self.parts,"\t Celdas: ", self.cells ,"\t Máximo Máquinas: ",self.mMax,"\t Solucion óptima: ", self.bSol,"\t") #mostrar informacion de la instancia


def cargar_matriz(FILE_PATH):
	p = Properties()
	with open(FILE_PATH,"rb") as f:
		p.load(f,encoding='utf8')
	instancia = {
		'Machines': int(p['Machines'].data),
		'Parts': int(p['Parts'].data),
		'Cells': int(p['Cells'].data),
		'Mmax': int(p['Mmax'].data),
		'Best Solution': int(p['Best'].data.split("=")[1]),
		'Matrix': np.array(p['Matrix'].data.split()).reshape(int(p['Machines'].data),int(p['Parts'].data)).astype('int8')
	}
	return instancia


def main(parametros):
	contador_optimo=0
	for i, archivo in enumerate(parametros.rutas):
		print("\n\ninstancia ",(i+1))
		inicio=time()
		instancia = Instancia(archivo)						#crear instancia a partir del archivo
		objetos = Soluciones(instancia, parametros)			#generar soluciones en base de la instancia
		inst = Metaheuristica(instancia, objetos, parametros) 				#en metaehuristica pasar cuadro y las soluciones
		final=time()
		tiempo=final-inicio
		print("solucion final:", inst.xGlobal[1],"\tEn",tiempo,"segundos")
		if inst.xGlobal[1]==instancia.bSol:
			contador_optimo+=1	
		else:
			print("no se encontro optimo")
	print("porcentaje de optimos: ",100*(contador_optimo/len(parametros.rutas)),'%')


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("-a", help="parámetro a, por defecto 1", default=1, type=float)
	parser.add_argument("-b", help="parámetro b, por defecto 1", default=1, type=float)
	parser.add_argument("-c", help="parámetro c, por defecto 1", default=1, type=float)
	parser.add_argument("-k", help="parámetro k para la ecuación sigmuidal, por defecto 1", default=1, type=float)
	parser.add_argument("-t","--theta", help="parámetro theta", default=0, type=int)
	parser.add_argument("-s","--semilla", help="semilla de randomización", default=int(time()), type=int)
	parser.add_argument("-i", "--iteraciones", help="iteraciones", default=100, type=int)
	parser.add_argument("-p", "--particulas",help="partículas", default=50, type=int)
	parser.add_argument("-r", "--rutas", help="especificar ruta/s", default=["./BoctorProblem_90_instancias/" + archivo for archivo in listdir("./BoctorProblem_90_instancias/") if os.path.isfile("./BoctorProblem_90_instancias/"+archivo)], nargs= '+', type=str)
	args = parser.parse_args()
	if parser.get_default('rutas') != args.rutas:
		listaRutas = list()
		for ruta in args.rutas:
			if os.path.isdir(ruta):
				listaRutas += [ruta.strip('/\\') +"/"+ archivo for archivo in listdir(ruta) if os.path.isfile(ruta.strip('/\\')+"/"+archivo)]
			else:
				listaRutas.append(ruta)
		args.rutas = listaRutas
	np.random.seed(args.semilla)
	main(args)

#preguntas al profe, cuando se realiza la funcion de busqueda de mejor solucion cada 10 iteraciones, esta se debe hacer el mantenimiento o hacerlo junto con la busqueda de la iteracion 10
#7.9228163e+28	#1.8530202e+15 	3 celdas