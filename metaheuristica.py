import numpy as np

class Metaheuristica(object):   #clase donde realiza las tareas de la metaehuristica
	def __init__(self, instancia, solucion, param):
		super(Metaheuristica, self).__init__()
		self.param = param
		self.phi=((1+np.sqrt(5))/2) #funcion phi que indica en el texto 
		self.instancia = instancia 	#instancia obtenida del txt
		self.solucion = solucion 	#solucion/es inicales para particulas
		self.v = self.generarV()	#generar aleatoriamente v
		p=solucion.s.index(min(self.solucion.s)) # conseguir indice , puntero sol																
		self.xBest=np.array((self.solucion.y[p], self.solucion.s[p]), dtype=object) 	#mejor solucion del grupo actual hay q copiar
		self.xGlobal=np.copy(self.xBest) 								#mejor solucion global 	
		self.mejorAleatoria=self.xBest[1]
		self.algoritmo()

	def generarV(self): #inicializar velocidad una matriz del mismo tamaño q la mxp
		obj = 2*np.random.random((self.param.particulas, self.instancia.machines))-1
		return obj
		# obj=[]
		# for i in range (Particulas):
		# 	obj.append(np.array(( 2*np.random.random(self.instancia.machines)-1)))
		# return np.array(obj)
		
	def algoritmo(self): #funcion que realiza las iteraciones de la metaehuristica
		# rangoTheta=100
		# sinTheta=0
		for p in range (self.param.particulas):  #inicializa partículas 
			paso=False
			intentos=0
			while paso==False:
				intentos+=1
				aux1=self.velocidad(self.xBest[0],self.xGlobal[0],self.v[p],self.solucion.y[p]) #guarda en variable temporal (velocidad)
				aux2=self.poscicion(self.solucion.y[p],aux1,1)									   #guarda en variable temporal (pocicion)
				aux2[np.where(aux2 == 1)]=0.9
				y=self.solucion.transformar(aux2)
				if intentos>10 and self.solucion.probar_restriccion(y)==False:
					aux2=aux2 + np.sin((np.random.random(len(aux2))*2*np.pi))
					aux2[np.where(aux2<0)]=0.1
					aux2[np.where(aux2>1)]=0.9
					y=self.solucion.transformar(aux2)
				if self.solucion.probar_restriccion(y) == True:    # si es factible la solucion generada, entonces continua asignando las demás variables para generar la solucion
					paso=True
					self.v[p]=aux1  #actualiza velocidad 
					self.solucion.y[p]=aux2 #actualiza pocicion
					Z=self.solucion.crearZ(self.instancia.matrix,y)
					self.solucion.s[p]=self.solucion.solucion(self.instancia.matrix,y,Z)
		desv1 = self.desviacionStandar(self.solucion.y) #almacena las primeras desviaciones estandar
		p=self.solucion.s.index(min(self.solucion.s)) #obtiene la partícula con mejor fitness
		self.xBest = (np.copy(self.solucion.y[p]),np.copy(self.solucion.s[p]))
		if self.xBest[1] < self.xGlobal[1]: #si la mejor solucion es mejor que la anterior, ésta la actualiza
			self.xGlobal = (np.copy(self.solucion.y[p]),np.copy(self.solucion.s[p]))
		primeraIteracion=self.xGlobal[1]
		for it in range(1, self.param.iteraciones):
			if self.xGlobal[1]<=self.instancia.bSol:                 #utiliza tecnica fordward checking
				break
			for p in range (self.param.particulas):
				paso=False
				intentos=0                       
				while paso==False:
					intentos+=1
					aux1=self.velocidad(self.xBest[0],self.xGlobal[0],self.v[p],self.solucion.y[p]) #a
					aux2=self.poscicion(self.solucion.y[p],aux1,1)
					aux2[np.where(aux2 == 1)]=0.9
					y=self.solucion.transformar(aux2)
					if intentos>10 and self.solucion.probar_restriccion(y)==False:
						aux2 += np.sin((np.random.random(len(aux2))*2*np.pi))
						aux2[np.where(aux2<0)]=0.1
						aux2[np.where(aux2>1)]=0.9
						y=self.solucion.transformar(aux2)
					if self.solucion.probar_restriccion(y) == True:
						paso=True
						self.v[p]=aux1
						self.solucion.y[p]=aux2
						Z=self.solucion.crearZ(self.instancia.matrix,y)
						self.solucion.s[p]=self.solucion.solucion(self.instancia.matrix,y,Z)
			p=self.solucion.s.index(min(self.solucion.s))
			self.xBest = (np.copy(self.solucion.y[p]),np.copy(self.solucion.s[p]))
			if self.xBest[1] < self.xGlobal[1]:
				self.xGlobal = (np.copy(self.solucion.y[p]),np.copy(self.solucion.s[p]))
			
			if it%10==0:  #por cada 10 iteraciones realiza un mantenimiento para realizar nuevas exploraciones
				#print("mantenimiento")
				desv2= self.desviacionStandar(self.solucion.y)  #calcula nueva desviacion estandar
				listaYt = np.where(desv2<desv1)          #obtiene indices de las comparaciones de desviacion estandar que son menores que el anterior
				listaYf = np.where(desv2>desv1)  		#obtiene indices de las comparaciones de desviacion estandar que no cumple con la condicion anterior
				for p in range (self.param.particulas):
					estado=False
					intentos=0
					auxX=np.zeros(self.instancia.machines)
					while estado==False:
						intentos+=1 
						aux1=self.velocidad(self.xBest[0][listaYt],self.xGlobal[0][listaYt],self.v[p][listaYt],self.solucion.y[p][listaYt])  #mismo trabajo que en la iteraciones, pero con diferente trato segun la condicion de las desviaciones estandar
						aux2=self.poscicion(self.solucion.y[p][listaYt],aux1,np.random.randint(2,6,len(listaYt)))
						aux3=self.velocidad(self.xBest[0][listaYf],self.xGlobal[0][listaYf],self.v[p][listaYf],self.solucion.y[p][listaYf])
						aux4=self.poscicion(self.solucion.y[p][listaYf],aux3,1)
						auxX[listaYt]=aux2
						auxX[listaYf]=aux4
						auxX[np.where(auxX==1)]=0.9
						y=self.solucion.transformar(auxX) #arreglar tomar auxiliares y unirla en su equivalente		
						if intentos>10 and self.solucion.probar_restriccion(y)==False:
							auxX=auxX + np.sin((np.random.random(len(auxX))*2*np.pi))
							auxX[np.where(auxX>=1)]=0.9
							auxX[np.where(auxX<=0)]=0.1
							y=self.solucion.transformar(auxX)
						if self.solucion.probar_restriccion(y) == True:
							estado=True
							self.solucion.y[p]=auxX
							self.v[p][listaYt]=aux1
							self.v[p][listaYf]=aux3
				desv1=desv2	
			#print("mejor local: ",self.Xbest[1],"\t mejor global: ",self.Xglobal[1])
		print("mejor solucion aleatoria: ",self.mejorAleatoria,"\t primera iteracion: ",primeraIteracion ,"\t mejor solucion: ",self.xGlobal[1])

	def velocidad(self,xBest,xGlobal,v,x): #ecuacion velocidad
		return self.param.a*v+self.param.b*np.random.random(len(v))*(xBest-x) + self.param.c*np.random.random(len(v))*(xGlobal-x)

	def poscicion(self,x,v1,mult):      # ecuacion pocicion
		r3=np.random.randint(-1,2,len(x)) #entrega -1 0 1
		temp1=self.sigmoide(x + mult*r3*self.phi + v1)
		return temp1

	def desviacionStandar(self,y):  #genera desviacion estandar para cada dimension	
		desvY=np.zeros(self.instancia.machines) #inicializa listas de desviacion estandar	
		for i in range(self.instancia.machines): #guarda desviacion estandar para máquinas x celdas
			desvY[i]=np.std(np.array(y)[:,i],ddof=1)
		return desvY


	def sigmoide(self,x): #se aplica la regla sigmoidal para transformar cualquier número a numeros entre 0 y 111
		return (1/(1+np.exp(-x/self.param.k)))
