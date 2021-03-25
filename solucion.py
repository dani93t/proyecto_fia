import numpy as np

class Soluciones(object):	#clase donde guarda la solucion
	def __init__(self, instancia, param):
		super(Soluciones, self).__init__()
		self.instancia = instancia
		self.y=[] 				#Matriz maquina x celdas 
		self.z=[] 				#Matriz parte x celdas
		self.s=[] 				#solucion/fitness
		for _ in range (param.particulas): #llenar las 3 matrices
			y,z,s = self.trabajo() #ejecuta las tareas de generacion y guardado de matrices
			self.y.append(y)
			self.z.append(z)
			self.s.append(s)

	def trabajo(self): # método donde genera las matrices MxC y PxC aleatorias para generar solucion
		a=self.instancia.matrix
		restriccion=False
		while restriccion==False:
			yUniforme=np.random.uniform(size=self.instancia.machines) #inicializa las variables de manera uniforme
			# Zuniforme=np.random.uniform(size=self.instancia.parts) #inicializa las variables de manera uniforme
			y=self.transformar(yUniforme) 	# Trasnforma las matrices de continua a discreta segun las celdas
			z=self.crearZ(a,y)	# Trasnforma las matrices de continua a discreta segun las celdas
			restriccion=self.probar_restriccion(y) # llama a verificar factibilidad de la funcion
		solucion=self.solucion(a,y,z) #resultado FO , fitness
		return yUniforme,z,solucion	#devuelve las 3 matrices 

	def transformar(self,matriz):  #funcion que transforma de numeros uniforme a binarios
		cells=self.instancia.cells
		arreglo_discreta=np.zeros((len(matriz),cells),dtype='int8') #llenar matriz de MXP
		# j = (Cells*matriz).astype(int)
		for i in range(len(matriz)): #multiplicar fila x columna para ver que tenga un 1
			j=int(matriz[i]*cells)
			arreglo_discreta[i][j]=1
		return arreglo_discreta

	def probar_restriccion(self,Y):  #verificar factibilidad de problema
		valido=True
		for k in range(self.instancia.cells): #solo comprueba la restriccion 3 ya que las primeras dos automaticamente está resuelta
			if sum(Y[:,k])>self.instancia.mMax:
				valido=False
		return valido	

	def solucion(self,A,Y,Z):     #mostrar solucion
		suma_total=0
		for k in range(self.instancia.cells):
			for i in range (self.instancia.machines):
				for j in range(self.instancia.parts):
					suma_total=suma_total+int(A[i][j])*Z[j][k]*(1-Y[i][k])
		return suma_total	

	def crearZ(self,a,y):
		z=np.zeros((self.instancia.parts,self.instancia.cells),dtype='int8')
		for k in range(self.instancia.cells):
			for j in range(self.instancia.parts):
				z[j][k]=np.sum(a[np.where(y[:,k]==1),j])
		for j in range(self.instancia.parts):  #establecer seleccion aleatoria cuando existe misma cantidad de elementos
			aux=np.zeros(self.instancia.cells)  
			rep,indice = self.repetido(z[j])
			if rep==True:
				aux[indice[np.random.randint(0,len(indice))]] = 1
				z[j]=aux
			else:
				aux[np.argmax(z[j])]=1
				z[j]=aux
		return z

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

	# def  mostrarMatriz(self,A,Y,Z):
	# 	matriz = np.zeros((self.instancia.machines,self.instancia.parts))
	# 	x=0
	# 	y=0
	# 	for k in range(self.instancia.cells):
	# 		for i in range (self.instancia.machines):
	# 			if Y[i][k]==1:
	# 				matriz[x][y]=A[:,j]
	# 				matriz[i][y]=A[:,x]
	# 		for j in range(self.instancia.parts):
	# 			print("no implementado")
