#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random as rd
from os import listdir
import numpy as np
from time import time
import os
from solucion import *
from metaheuristica import *

MaxIteraciones=100	#número de iteraciones
Particulas=50		#numero de partículas
a=1			#parámetro a
b=1					#parámetro b
c=1					#parámetro c
theta=0				#parámetro theta
seed=-1				#parámetro semilla
k=1
solucionOptima=0

if seed>=0:  	#si semilla es positivo, tomara este valor como semilla
	np.random.seed(seed)



class Instancia(object):
	"""docstring for Instancia"""
	def __init__(self, arg):
		super(Instancia, self).__init__()
		self.arg = "BoctorProblem_90_instancias/"+arg
		self.Matrix,self.Machines,self.Parts,self.Cells,self.Mmax,self.Bsol = self.cargar_matriz(self.arg)
		print ("Máquinas: ",self.Machines ,"\t Partes: ",self.Parts,"\t Celdas: ", self.Cells ,"\t Máximo Máquinas: ",self.Mmax,"\t Mejor solucion: ", self.Bsol,"\t") #mostrar informacion de la instancia

	def cargar_matriz(self,PATH_SOURCE):
		TXT_SEP='='
		archivo = open(PATH_SOURCE, "r") 				
		Matrix=[]
		matriz = False
		for linea in archivo.readlines():					#Lee archivo de instancia
			if linea.split(TXT_SEP)[0]=="Machines":
				Machines = int(linea.split(TXT_SEP)[1])
			if linea.split(TXT_SEP)[0]=="Parts":
				Parts = int(linea.split(TXT_SEP)[1])
			if linea.split(TXT_SEP)[0]=="Cells":
				Cells = int(linea.split(TXT_SEP)[1])
			if linea.split(TXT_SEP)[0]=="Mmax":
				Mmax = int(linea.split(TXT_SEP)[1])
			if linea.split(TXT_SEP)[0]=="Best Solution":
				Bsol = int(linea.split(TXT_SEP)[1])
			if matriz == True:
				Matrix.append((linea.strip(' \\\n\r').split(' ')))	
			if linea.split(TXT_SEP)[0]=="Matrix":
				matriz = True
		return np.array(Matrix, dtype='int8'),Machines,Parts,Cells,Mmax,Bsol


def main():
	instancias=listdir("BoctorProblem_90_instancias/")
	contador_optimo=0
	for i in range(len(instancias)):
		print("instancia ",(i+1))
		inicio=time()
		instancia = Instancia(instancias[i])	#crear instancia a partir del archivo
		objetos=Soluciones(instancia)			#generar soluciones en base de la instancia
		inst=Metaheuristica(instancia,objetos) 	#en metaehuristica pasar cuadro y las soluciones
		final=time()
		tiempo=final-inicio
		print("solucion final:", inst.Xglobal[1],"\n\n")
		if inst.Xglobal[1]==instancia.Bsol:
			contador_optimo+=1	
		else:
			print("no se encontro optimo")
	print("porcentaje de optimos: ",100*(contador_optimo/90),'%')
		
		

if __name__ == '__main__':
	main()


#preguntas al profe, cuando se realiza la funcion de busqueda de mejor solucion cada 10 iteraciones, esta se debe hacer el mantenimiento o hacerlo junto con la busqueda de la iteracion 10
#7.9228163e+28	#1.8530202e+15 	3 celdas
#1.8446744e+19	#4294967296		2 celdas