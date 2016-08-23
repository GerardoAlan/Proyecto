
#-*- coding:utf-8 -*-

import MagnitudFase
import QuickSort
import matplotlib.pyplot as plt
import numpy as np

def generarMagnitudFase(rutaOrigen, rutaDestino, nombre):
	# Leemos el archivo que contiene la informacion de la Transformada Rapida de Fourier
	archivoLectura = open(rutaOrigen + nombre, "r")
	lineas = archivoLectura.readlines()
	# Creamos los arreglos donde almacenaremos cada Canal
	delta = []
	theta = []
	lowalpha = []
	highalpha = []
	lowbeta = []
	highbeta = []
	lowgamma = []
	midgamma = []
	meditation = []
	attention = []
	
	# Iteramos sobre todas las lineas de dicho archivo
	for linea in lineas:
		# En el arreglo elementos obtenemos cada valor de la linea que esta separado entre comas
		elementos = linea.split(',')
		# Agregamos el valor del elemento con su canal correspondiente
		delta.append(elementos[0])
		delta.append(elementos[1])
		theta.append(elementos[2])
		theta.append(elementos[3])
		lowalpha.append(elementos[4])
		lowalpha.append(elementos[5])
		highalpha.append(elementos[6])
		highalpha.append(elementos[7])
		lowbeta.append(elementos[8])
		lowbeta.append(elementos[9])
		highbeta.append(elementos[10])
		highbeta.append(elementos[11])
		lowgamma.append(elementos[12])
		lowgamma.append(elementos[13])
		
	# Procedemos a obtener la Magnitud y la Fase de dichos valores utilizando la clase GeneradorMagnitudFase
	
	# Asignamos al constructor el canal Delta
	MF = MagnitudFase.MagnitudFase(arreglo = delta)
	# Obtenemos el arreglo que representa la Magnitud de Delta
	magnitudDelta = MF.obtenerMagnitud()
	# Obtenemos el arreglo que representa la Fase de Delta
	faseDelta = MF.obtenerFase()
	# El metodo ordenarFase requiere el arreglo que representa la Fase y Magnitud de Delta
	# Posterior a ello regresa la direccion de los arreglos ya ordenados y limpios (Fase > 0)
	faseDelta,magnitudDelta = ordenarFase(faseDelta, magnitudDelta)
	
	# Realizamos el mismo procedimiento para los siguientes Canales
	
	# Canal Thetha
	MF = MagnitudFase.MagnitudFase(arreglo = theta)
	faseTheta = MF.obtenerFase()
	magnitudTheta = MF.obtenerMagnitud()
	faseTheta,magnitudTheta = ordenarFase(faseTheta, magnitudTheta)
	
	# Canal Lowalpha
	MF = MagnitudFase.MagnitudFase(arreglo = lowalpha)
	faseLowalpha = MF.obtenerFase()
	magnitudLowalpha = MF.obtenerMagnitud()
	faseLowalpha,magnitudLowalpha = ordenarFase(faseLowalpha, magnitudLowalpha)

	# Canal Highalpha
	MF = MagnitudFase.MagnitudFase(arreglo = highalpha)
	faseHighalpha = MF.obtenerFase()
	magnitudHighalpha = MF.obtenerMagnitud()
	faseHighalpha,magnitudHighalpha = ordenarFase(faseHighalpha, magnitudHighalpha)
	
	# Canal Lowbeta
	MF = MagnitudFase.MagnitudFase(arreglo = lowbeta)
	faseLowbeta = MF.obtenerFase()
	magnitudLowbeta = MF.obtenerMagnitud()
	faseLowbeta,magnitudLowbeta = ordenarFase(faseLowbeta, magnitudLowbeta)
	
	# Canal Highbeta
	MF = MagnitudFase.MagnitudFase(arreglo = highbeta)
	faseHighbeta = MF.obtenerFase()
	magnitudHighbeta = MF.obtenerMagnitud()
	faseHighbeta,magnitudHighbeta = ordenarFase(faseHighbeta, magnitudHighbeta)

	# Canal Lowgamma
	MF = MagnitudFase.MagnitudFase(arreglo = lowgamma)
	faseLowgamma = MF.obtenerFase()
	magnitudLowgamma = MF.obtenerMagnitud()
	faseLowgamma,magnitudLowgamma = ordenarFase(faseLowgamma, magnitudLowgamma)
		
	# Para obtener las longitudes de cada Fase
	longitudDelta = len(faseDelta)
	longitudTheta = len(faseTheta)
	longitudLowalpha = len(faseLowalpha)
	longitudHighalpha = len(faseHighalpha)
	longitudLowbeta = len(faseLowbeta)
	longitudHighbeta = len(faseHighbeta)
	longitudLowgamma = len(faseLowgamma)
	
	longitudMaxima = calcularLongitudMaxima(longitudDelta,longitudTheta,longitudLowalpha,longitudHighalpha,longitudLowbeta,longitudHighbeta,longitudLowgamma)	
	
	# Abrimos un archivo para escribir la Magnitud y Fase obtenidos para cada canal
	archivoEscritura = open(rutaDestino + nombre, "w")
	for x in range(longitudMaxima):
		linea = ""
		linea += crearLinea(x, longitudDelta, magnitudDelta, faseDelta)
		linea += crearLinea(x, longitudTheta, magnitudTheta, faseTheta)
		linea += crearLinea(x, longitudLowalpha, magnitudLowalpha, faseLowalpha)
		linea += crearLinea(x, longitudHighalpha, magnitudHighalpha, faseHighalpha)
		linea += crearLinea(x, longitudLowbeta, magnitudLowbeta, faseLowbeta)
		linea += crearLinea(x, longitudHighbeta, magnitudHighbeta, faseHighbeta)
		linea += crearLinea(x, longitudLowgamma, magnitudLowgamma, faseLowgamma)
		
		linea += "\n"
		
		archivoEscritura.write(linea)

	archivoEscritura.close()

# Metodo para obtener el arreglo mas largo
def calcularLongitudMaxima(longitudDelta, longitudTheta, longitudLowalpha, longitudHighalpha, longitudLowbeta, longitudHighbeta, longitudLowgamma):
	longitudMaxima = longitudDelta
	if longitudTheta > longitudMaxima:
		longitudMaxima = longitudTheta
	if longitudLowalpha > longitudMaxima:
		longitudMaxima = longitudLowalpha
	if longitudHighalpha > longitudMaxima:
		longitudMaxima = longitudHighalpha	
	if longitudLowbeta > longitudMaxima:
		longitudMaxima = longitudLowbeta	
	if longitudHighbeta > longitudMaxima:
		longitudMaxima = longitudHighbeta
	if longitudLowgamma > longitudMaxima:
		longitudMaxima = longitudLowgamma
	
	return longitudMaxima

# Metodo que evalua si el canal aun puede escribir el dato, en cuyo caso lo obtiene de los arreglos y lo retorna
def crearLinea(posicionActual, longitudCanal, magnitud, fase):
	if posicionActual < longitudCanal:
		return str(magnitud[posicionActual]) + "," + str(fase[posicionActual]) + ","
	else:
		return " , ,"

# Metodo que se encarga de ordenar el arreglo fase y modificar los dos arreglos manteniendo la relacion entre ellos
def ordenarFase(fase, magnitud):
	
	# Este arreglo se utiliza para almacenar las tuplas de los contenidos de cada arreglo 
	arregloAuxiliar = []
	
	# La variable elemento toma los valores desde 0 hasta el numero de elementos en el arreglo fase -1
	for elemento in range(len(fase)):
		
		# Validamos que la fase sea positiva para no repetir valores
		if fase[elemento] > 0:
			# Este arreglo sirve para juntar ambos valores y que cuando se realize el ordenamiento no se revuelvan
			arregloInterno = []
			# Agregamos el valor que se encuentra en ambos arreglos, sobre la misma posicion 
			arregloInterno.append(fase[elemento])
			arregloInterno.append(magnitud[elemento])
			# Una vez creada la tupla la agregamos a la lista arregloAuxiliar
			arregloAuxiliar.append(arregloInterno)
	
	# En esta sentencia utilizamos la clase QuickSort la cual se encarga de ordenar la lista arregloAuxiliar
	ejecutaOrdenamiento = QuickSort.QuickSort(arreglo=arregloAuxiliar)
	
	magnitud = []
	fase = []
	# Iteramos sobre el arregloAuxiliar, cada iteracion devuelve el arreglo llamado elemento
	for elemento in arregloAuxiliar:
		# La primera posicion de dicho arreglo contiene el valor que representa la fase
		fase.append(elemento[0])
		# La segunda posicion de dicho arreglo contiene el valor que representa la magnitud 
		magnitud.append(elemento[1])
	# regresamos las direcciones de los nuevos arreglos
	return fase,magnitud


# Este metodo crea la Grafica con los datos del archivo dentro de la carpeta MuestrasMagnitudFase
# Almacena la Grafica en la carpeta GraficasMagnitudFase
def crearGraficaMagnitudFase(rutaOrigen, rutaDestino, nombre):
	archivoLectura = open(rutaOrigen + nombre, "r")
	lineas = archivoLectura.readlines()

	# Canales
	deltaMagnitud = []
	deltaFase = []
	thetaMagnitud = []
	thetaFase = []
	lowalphaMagnitud = []
	lowalphaFase = []
	highalphaMagnitud = []
	highalphaFase = []
	lowbetaMagnitud = []
	lowbetaFase = []
	highbetaMagnitud = []
	highbetaFase = []
	lowgammaMagnitud = []
	lowgammaFase = []
	
	midgammaReal = []
	midgammaImag = []

	# Datos Adicionales
	meditationReal = []
	meditationImag = []
	attentionReal = []
	attentionImag = []

	for linea in lineas:
		elementos = linea.split(',')
		if elementos[0] != " ":
			deltaMagnitud.append(elementos[0])
			deltaFase.append(elementos[1])
		if elementos[2] != " ":
			thetaMagnitud.append(elementos[2])
			thetaFase.append(elementos[3])
		if elementos[4] != " ":
			lowalphaMagnitud.append(elementos[4])
			lowalphaFase.append(elementos[5])
		if elementos[6] != " ":
			highalphaMagnitud.append(elementos[6])
			highalphaFase.append(elementos[7])
		if elementos[8] != " ":
			lowbetaMagnitud.append(elementos[8])
			lowbetaFase.append(elementos[9])
		if elementos[10] != " ":
			highbetaMagnitud.append(elementos[10])
			highbetaFase.append(elementos[11])
		if elementos[12] != " ":
			lowgammaMagnitud.append(elementos[12])
			lowgammaFase.append(elementos[13])
			
	# Para quitarle al nombre el .txt del final	
	nombre = nombre[:len(nombre)-4]
	
	# Grafica de canal Delta
	plt.subplot(3,3,1)
	plt.plot(deltaFase, deltaMagnitud)
	# Configurar grafica
	plt.xlim(0, 3.2) # limite en x de 0 a 3.2 ya que el mayor es pi
	plt.axhline(0, color="black")
	plt.axvline(0, color="black")
	plt.title('Magnitud y Fase Canal Delta')
	plt.xlabel(u'Fase (0, π)')
	plt.ylabel(u'Magnitud')
	
	# Grafica de canal Theta
	plt.subplot(3,3,2)
	plt.plot(thetaFase, thetaMagnitud)
	# Configurar grafica
	plt.xlim(0, 3.2) # limite en x de 0 a 3.2 ya que el mayor es pi
	plt.axhline(0, color="black")
	plt.axvline(0, color="black")
	plt.title('Magnitud y Fase Canal Theta')
	plt.xlabel(u'Fase (0, π)')
	plt.ylabel(u'Magnitud')

	# Grafica de canal Lowalpha
	plt.subplot(3,3,3)
	plt.plot(lowalphaFase, lowalphaMagnitud)
	# Configurar grafica
	plt.xlim(0, 3.2) # limite en x de 0 a 3.2 ya que el mayor es pi
	plt.axhline(0, color="black")
	plt.axvline(0, color="black")
	plt.title('Magnitud y Fase Canal Lowalpha')
	plt.xlabel(u'Fase (0, π)')
	plt.ylabel(u'Magnitud')

	# Grafica de canal Highalpha
	plt.subplot(3,3,4)
	plt.plot(highalphaFase, highalphaMagnitud)
	# Configurar grafica
	plt.xlim(0, 3.2) # limite en x de 0 a 3.2 ya que el mayor es pi
	plt.axhline(0, color="black")
	plt.axvline(0, color="black")
	plt.title('Magnitud y Fase Canal Highalpha')
	plt.xlabel(u'Fase (0, π)')
	plt.ylabel(u'Magnitud')

	# Grafica de canal Lowbeta
	plt.subplot(3,3,5)
	plt.plot(lowbetaFase, lowbetaMagnitud)
	# Configurar grafica
	plt.xlim(0, 3.2) # limite en x de 0 a 3.2 ya que el mayor es pi
	plt.axhline(0, color="black")
	plt.axvline(0, color="black")
	plt.title('Magnitud y Fase Canal Lowbeta')
	plt.xlabel(u'Fase (0, π)')
	plt.ylabel(u'Magnitud')

	# Grafica de canal Highbeta
	plt.subplot(3,3,6)
	plt.plot(highbetaFase, highbetaMagnitud)
	# Configurar grafica
	plt.xlim(0, 3.2) # limite en x de 0 a 3.2 ya que el mayor es pi
	plt.axhline(0, color="black")
	plt.axvline(0, color="black")
	plt.title('Magnitud y Fase Canal Highbeta')
	plt.xlabel(u'Fase (0, π)')
	plt.ylabel(u'Magnitud')

	# Grafica de canal Lowgamma
	plt.subplot(3,3,7)
	plt.plot(lowgammaFase, lowgammaMagnitud)
	# Configurar grafica
	plt.xlim(0, 3.2) # limite en x de 0 a 3.2 ya que el mayor es pi
	plt.axhline(0, color="black")
	plt.axvline(0, color="black")
	plt.title('Magnitud y Fase Canal Lowgamma')
	plt.xlabel(u'Fase (0, π)')
	plt.ylabel(u'Magnitud')
				
	'''
	# Grafica de canal MidGamma
	plt.subplot(3,3,8)
	plt.plot(midgammaReal,midgammaImag)
	# Limitar los valores de los ejes
	#plt.xlim(0, xlimite)
	plt.axhline(0, color="black")
	plt.axvline(0, color="black")
	plt.title('FFT Canal MidGamma')
	plt.xlabel(u'Frecuencia Hz')
	plt.ylabel(u'Magnitud')

	# Grafica de atencion y meditacion
	plt.subplot(3,3,9)
	plt.plot(meditationReal,meditationImag, 'b-' ,label=u"Meditation")
	plt.plot(attentionReal,attentionImag, 'g',label= u"Attention")
	#plt.plot(x, [poorSignal[i] for i in x], 'r' , label=u"PoorSignal")
	plt.legend(shadow = True, fancybox= True)

	# Limitar los valores de los ejes.
	#plt.xlim(0, xlimite)

	# Establecer el color de los ejes.
	plt.axhline(0, color="black")
	plt.axvline(0, color="black")
	plt.title('FFT Datos Adicionales')
	plt.xlabel(u'Frecuencia Hz')
	plt.ylabel(u'Magnitud')
	'''
	# Mostramos en pantalla
	manager = plt.get_current_fig_manager()
	manager.window.showMaximized()
	plt.tight_layout()

	plt.savefig(rutaDestino + nombre + ".png")
	plt.show()


generarMagnitudFase("MuestrasTransformadas/","MuestrasMagnitudFase/",u"Miguel_Romero_GutiérrezRelajante.txt")
crearGraficaMagnitudFase("MuestrasMagnitudFase/","GraficasMagnitudFase/",u"Miguel_Romero_GutiérrezRelajante.txt")


