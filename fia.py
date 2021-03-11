#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random as rd
from os import listdir
import numpy as np
from solucion import *


			#parámetro theta
seed=0				#parámetro semilla



if seed>=0:  	#si semilla es positivo, tomara este valor como semilla
	np.random.seed(seed)


log=open("log.txt","w")
log.write(str(("\ta: ",a,"\tb: ",b,"\tc: ",c)))
log.close()
log=open("log.txt","a")

class problema(object):
	"""docstring for problema"""
	def __init__(self, arg):
		super(problema, self).__init__()
		self.arg = "BoctorProblem_90_instancias/"+arg
		self.Matrix,self.Machines,self.Parts,self.Cells,self.Mmax,self.Bsol = self.cargar_matriz(self.arg)
		log.write(str(("Máquinas: ",self.Machines ,"\t Partes: ",self.Parts,"\t Celdas: ", self.Cells ,"\t Máximo Máquinas: ",self.Mmax,"\t Mejor solucion: ", self.Bsol,"\t\n")))
		print ("Máquinas: ",self.Machines ,"\t Partes: ",self.Parts,"\t Celdas: ", self.Cells ,"\t Máximo Máquinas: ",self.Mmax,"\t Mejor solucion: ", self.Bsol,"\t\n") #mostrar informacion de la instancia

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
		return Matrix,Machines,Parts,Cells,Mmax,Bsol



def main():
	instancias=listdir("BoctorProblem_90_instancias/")
	for i in range(len(instancias)):
		instancia = problema(instancias[i])	#crear instancia a partir del archivo
		objetos=soluciones(instancia)			#generar soluciones en base de la instancia
		metaehuristia(instancia,objetos) 	#en metaehuristica pasar cuadro y las soluciones
		
		


if __name__ == '__main__':
	main()


#por qué se cuelga la funcion (me fije por las altos numeros de velocidad y eso afecta la asociacion  de los random) donde llega un momento que realiza pruebas de movimiento y las soluciones dadas ya no da soluciones factibles
#preguntas al profe, cuando se realiza la funcion de busqueda de mejor solucion cada 10 iteraciones, esta se debe hacer el mantenimiento o hacerlo junto con la busqueda de la iteracion 10
#a qué se refiere solucion local que aparece en el texto y como se agrega? 