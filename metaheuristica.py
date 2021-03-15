import numpy as np

MaxIteraciones=100	#número de iteraciones
Particulas=50		#numero de partículas
a=1			#parámetro a
b=1					#parámetro b
c=1					#parámetro c
k=1

class Metaheuristica(object):   #clase donde realiza las tareas de la metaehuristica
	def __init__(self, instancia, solucion):
		super(Metaheuristica, self).__init__()
		self.phi=((1+np.sqrt(5))/2) #funcion phi que indica en el texto
		self.instancia = instancia 	#instancia obtenida del txt
		self.solucion = solucion 	#solucion/es inicales para particulas
		self.v = self.generarV()	#generar aleatoriamente v
		p=solucion.S.index(min(self.solucion.S)) # conseguir indice , puntero sol
		# #self.Xbest=np.array((np.copy(self.solucion.Y[p]),np.copy(self.solucion.S[p])))				#mejor solucion del grupo actual hay q copiar
		# #self.Xglobal=np.array((np.copy(self.solucion.Y[p]),np.copy(self.solucion.S[p])))			#mejor solucion global 															
		self.Xbest=np.array((self.solucion.Y[p],self.solucion.S[p]))
		self.Xglobal=np.copy(self.Xbest)
		self.mejorAleatoria=self.Xbest[1]
		self.algoritmo()

	def generarV(self): #inicializar velocidad una matriz del mismo tamaño q la mxp
		obj = 2*np.random.random((Particulas,self.instancia.Machines))-1
		return obj
		# obj=[]
		# for i in range (Particulas):
		# 	obj.append(np.array(( 2*np.random.random(self.instancia.Machines)-1)))
		# return np.array(obj)
		
	def algoritmo(self): #funcion que realiza las iteraciones de la metaehuristica
		# rangoTheta=100
		# sinTheta=0
		for p in range (Particulas):  #inicializa partículas 
			paso=False
			intentos=0
			while paso==False:
				intentos+=1
				aux1=self.velocidad(self.Xbest[0],self.Xglobal[0],self.v[p],self.solucion.Y[p]) #guarda en variable temporal (velocidad)
				aux2=self.poscicion(self.solucion.Y[p],aux1,1)									   #guarda en variable temporal (pocicion)
				aux2[np.where(aux2 == 1)]=0.9
				Y=self.solucion.transformar(aux2)
				if intentos>10 and self.solucion.probar_restriccion(Y)==False:
					aux2=aux2 + np.sin((np.random.random(len(aux2))*2*np.pi))
					aux2[np.where(aux2<0)]=0.1
					aux2[np.where(aux2>1)]=0.9
					Y=self.solucion.transformar(aux2)
				if self.solucion.probar_restriccion(Y) == True:    # si es factible la solucion generada, entonces continua asignando las demás variables para generar la solucion
					paso=True
					self.v[p]=aux1  #actualiza velocidad 
					self.solucion.Y[p]=aux2 #actualiza pocicion
					Z=self.solucion.crearZ(self.instancia.Matrix,Y)
					self.solucion.S[p]=self.solucion.solucion(self.instancia.Matrix,Y,Z)
		desv1 = self.desviacionStandar(self.solucion.Y) #almacena las primeras desviaciones estandar
		p=self.solucion.S.index(min(self.solucion.S)) #obtiene la partícula con mejor fitness
		self.Xbest = (np.copy(self.solucion.Y[p]),np.copy(self.solucion.S[p]))
		if self.Xbest[1] < self.Xglobal[1]: #si la mejor solucion es mejor que la anterior, ésta la actualiza
			self.Xglobal = (np.copy(self.solucion.Y[p]),np.copy(self.solucion.S[p]))
		primeraIteracion=self.Xglobal[1]
		for it in range(1,MaxIteraciones):
			if self.Xglobal[1]<=self.instancia.Bsol:                 #utiliza tecnica fordward checking
				break
			for p in range (Particulas):
				paso=False
				intentos=0                       
				while paso==False:
					intentos+=1
					aux1=self.velocidad(self.Xbest[0],self.Xglobal[0],self.v[p],self.solucion.Y[p]) #a
					aux2=self.poscicion(self.solucion.Y[p],aux1,1)
					
					aux2[np.where(aux2 == 1)]=0.9
					

					Y=self.solucion.transformar(aux2)
					if intentos>10 and self.solucion.probar_restriccion(Y)==False:
						aux2=aux2 + np.sin((np.random.random(len(aux2))*2*np.pi))
						
						aux2[np.where(aux2<0)]=0.1
						aux2[np.where(aux2>1)]=0.9

						Y=self.solucion.transformar(aux2)
					if self.solucion.probar_restriccion(Y) == True:
						paso=True
						self.v[p]=aux1
						self.solucion.Y[p]=aux2
						Z=self.solucion.crearZ(self.instancia.Matrix,Y)
						self.solucion.S[p]=self.solucion.solucion(self.instancia.Matrix,Y,Z)
			p=self.solucion.S.index(min(self.solucion.S))
			self.Xbest = (np.copy(self.solucion.Y[p]),np.copy(self.solucion.S[p]))
			if self.Xbest[1] < self.Xglobal[1]:
				self.Xglobal = (np.copy(self.solucion.Y[p]),np.copy(self.solucion.S[p]))
			
			if it%10==0:  #por cada 10 iteraciones realiza un mantenimiento para realizar nuevas exploraciones
				#print("mantenimiento")
				desv2= self.desviacionStandar(self.solucion.Y)  #calcula nueva desviacion estandar
				listaYt = np.where(desv2<desv1)          #obtiene indices de las comparaciones de desviacion estandar que son menores que el anterior
				listaYf = np.where(desv2>desv1)  		#obtiene indices de las comparaciones de desviacion estandar que no cumple con la condicion anterior
				for p in range (Particulas):
					estado=False
					intentos=0
					auxX=np.zeros(self.instancia.Machines)
					while estado==False:
						intentos+=1 
						aux1=self.velocidad(self.Xbest[0][listaYt],self.Xglobal[0][listaYt],self.v[p][listaYt],self.solucion.Y[p][listaYt])  #mismo trabajo que en la iteraciones, pero con diferente trato segun la condicion de las desviaciones estandar
						aux2=self.poscicion(self.solucion.Y[p][listaYt],aux1,np.random.randint(2,6,len(listaYt)))
						aux3=self.velocidad(self.Xbest[0][listaYf],self.Xglobal[0][listaYf],self.v[p][listaYf],self.solucion.Y[p][listaYf])
						aux4=self.poscicion(self.solucion.Y[p][listaYf],aux3,1)
						auxX[listaYt]=aux2
						auxX[listaYf]=aux4
						auxX[np.where(auxX==1)]=0.9
						Y=self.solucion.transformar(auxX) #arreglar tomar auxiliares y unirla en su equivalente		
						if intentos>10 and self.solucion.probar_restriccion(Y)==False:
							auxX=auxX + np.sin((np.random.random(len(auxX))*2*np.pi))
							auxX[np.where(auxX>=1)]=0.9
							auxX[np.where(auxX<=0)]=0.1
							Y=self.solucion.transformar(auxX)
						if self.solucion.probar_restriccion(Y) == True:
							estado=True
							self.solucion.Y[p]=auxX
							self.v[p][listaYt]=aux1
							self.v[p][listaYf]=aux3
				desv1=desv2	
			#print("mejor local: ",self.Xbest[1],"\t mejor global: ",self.Xglobal[1])
		print("mejor solucion aleatoria: ",self.mejorAleatoria,"\t primera iteracion: ",primeraIteracion ,"\t mejor solucion: ",self.Xglobal[1])




	def velocidad(self,Xbest,Xglobal,v,x): #ecuacion velocidad
		return a*v+b*np.random.random(len(v))*(Xbest-x) + c*np.random.random(len(v))*(Xglobal-x)

	def poscicion(self,x,v1,mult):      # ecuacion pocicion
		r3=np.random.randint(-1,2,len(x)) #entrega -1 0 1
		temp1=self.sigmoide(x + mult*r3*self.phi + v1)
		return temp1


	def desviacionStandar(self,Y):  #genera desviacion estandar para cada dimension	
		desvY=np.zeros(self.instancia.Machines) #inicializa listas de desviacion estandar	
		for i in range(self.instancia.Machines): #guarda desviacion estandar para máquinas x celdas
			desvY[i]=np.std(np.array(Y)[:,i],ddof=1)
		return desvY


	def sigmoide(self,x):    #se aplica la regla sigmoidal para transformar cualquier número a numeros entre 0 y 111
		return (1/(1+np.exp(-x/k)))

