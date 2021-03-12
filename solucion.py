import numpy as np

Particulas=50		#numero de partículas

class Soluciones(object):	#clase donde guarda la solucion
	def __init__(self, arg):
		super(Soluciones, self).__init__()
		self.instancia = arg
		self.Y=[] 				#Matriz maquina x celdas 
		self.Z=[] 				#Matriz parte x celdas
		self.S=[] 				#solucion/fitness
		for p in range (Particulas): #llenar las 3 matrices
			y,z,s = self.trabajo() #ejecuta las tareas de generacion y guardado de matrices
			self.Y.append(y)
			self.Z.append(z)
			self.S.append(s)

	def trabajo(self): # método donde genera las matrices MxC y PxC aleatorias para generar solucion
		A=self.instancia.Matrix
		restriccion=False
		while restriccion==False:	
			Yuniforme=np.random.uniform(size=self.instancia.Machines) #inicializa las variables de manera uniforme
			Zuniforme=np.random.uniform(size=self.instancia.Parts) #inicializa las variables de manera uniforme
			Y=self.transformar(Yuniforme) 	# Trasnforma las matrices de continua a discreta segun las celdas
			Z=self.crearZ(A,Y)	# Trasnforma las matrices de continua a discreta segun las celdas
			restriccion=self.probar_restriccion(Y) # llama a verificar factibilidad de la funcion
		Solucion=self.solucion(A,Y,Z) #resultado FO , fitness
		return Yuniforme,Z,Solucion	#devuelve las 3 matrices 

	def transformar(self,matriz):  #funcion que transforma de numeros uniforme a binarios
		Cells=self.instancia.Cells
		arreglo_discreta=np.zeros((len(matriz),Cells),dtype='int8') #llenar matriz de MXP
		# j = (Cells*matriz).astype(int)
		for i in range(len(matriz)): #multiplicar fila x columna para ver que tenga un 1
			j=int(matriz[i]*Cells)
			arreglo_discreta[i][j]=1
		return arreglo_discreta

	def probar_restriccion(self,Y):  #verificar factibilidad de problema
		valido=True
		for k in range(self.instancia.Cells): #solo comprueba la restriccion 3 ya que las primeras dos automaticamente está resuelta
			if sum(Y[:,k])>self.instancia.Mmax:
				valido=False
		return valido	

	def solucion(self,A,Y,Z):     #mostrar solucion
		suma_total=0
		for k in range(self.instancia.Cells):
			for i in range (self.instancia.Machines):
				for j in range(self.instancia.Parts):
					suma_total=suma_total+int(A[i][j])*Z[j][k]*(1-Y[i][k])
		return suma_total	

	def crearZ(self,A,Y):
		Z=np.zeros((self.instancia.Parts,self.instancia.Cells),dtype='int8')
		for k in range(self.instancia.Cells):
			for j in range(self.instancia.Parts):
				Z[j][k]=np.sum(A[np.where(Y[:,k]==1),j])
		for j in range(self.instancia.Parts):  #establecer seleccion aleatoria cuando existe misma cantidad de elementos
			aux=np.zeros(self.instancia.Cells)  
			rep,indice = self.repetido(Z[j])
			if rep==True:
				aux[  indice[np.random.randint(0,len(indice))]] = 1
				Z[j]=aux
			else:
				aux[np.argmax(Z[j])]=1
				Z[j]=aux
		return Z

	def repetido(self,tupla): #genera en caso de haber maximos repetidos, obtener los indices de las cuales se repite
		maximo=np.max(tupla)
		index=np.array((),dtype='int16')
		count=0
		if maximo>0: #si el numero maximo es superior a 0, entonces cuenta la cantidad
			for i in range(len(tupla)):
				if tupla[i]==maximo:
					count+=1
					index=np.hstack((index,i))
		if count >= 2 :
			return True,index 
		return False,index

	def  mostrarMatriz(self,A,Y,Z):
		matriz = np.zeros((self.instancia.Machines,self.instancia.Parts))
		x=0
		y=0
		for k in range(self.instancia.Cells):
			for i in range (self.instancia.Machines):
				if Y[i][k]==1:
					matriz[x][y]=A[:,j]
					matriz[i][y]=A[:,x]
			for j in range(self.instancia.Parts):
				print("no implementado")