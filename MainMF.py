
#-*- coding:utf-8 -*-

import MagnitudFase
import QuickSort
import matplotlib.pyplot as plt
import numpy as np
from boto.dynamodb.condition import NULL

def generarMF(rutaOrigen, rutaDestino, nombre):
	archivoLectura = open(rutaOrigen + nombre, "r")
	lineas = archivoLectura.readlines()
	# Canales
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
	for linea in lineas:
		elementos = linea.split(',')
		delta.append(elementos[0])
		delta.append(elementos[1])
		'''
		lowalpha.append(elementos[2])
		highalpha.append(elementos[3])
		lowbeta.append(elementos[4])
		highbeta.append(elementos[5])
		lowgamma.append(elementos[6])
		midgamma.append(elementos[7])
		meditation.append(elementos[8])
		attention.append(elementos[9])
	'''
	MF = MagnitudFase.MagnitudFase(arreglo = delta)
	magnitudDelta = MF.obtenerMagnitud()
	faseDelta = MF.obtenerFase()
	veces = len(magnitudDelta)
	
	arregloAux = []
	for x in range(veces):
		arregloDentro = []
		arregloDentro.append(faseDelta[x])
		arregloDentro.append(magnitudDelta[x])
		arregloAux.append(arregloDentro)
	
	QS = QuickSort.QuickSort(arreglo=arregloAux)
	
	magnitudDelta = []
	faseDelta = []
	for x in arregloAux:
		faseDelta.append(x[0])
		magnitudDelta.append(x[1])
	
	'''
	FFT = TransformadaRapidaFourier.TransformadaRapidaFourier(arreglo = theta)
	ertheta = FFT.obtenerEjeReal()
	eitheta = FFT.obtenerEjeImaginario()
	
	FFT = TransformadaRapidaFourier.TransformadaRapidaFourier(arreglo = lowalpha)
	erlowalpha = FFT.obtenerEjeReal()
	eilowalpha = FFT.obtenerEjeImaginario()
	
	FFT = TransformadaRapidaFourier.TransformadaRapidaFourier(arreglo = highalpha)
	erhighalpha = FFT.obtenerEjeReal()
	eihighalpha = FFT.obtenerEjeImaginario()

	FFT = TransformadaRapidaFourier.TransformadaRapidaFourier(arreglo = lowbeta)
	erlowbeta = FFT.obtenerEjeReal()
	eilowbeta = FFT.obtenerEjeImaginario()

	FFT = TransformadaRapidaFourier.TransformadaRapidaFourier(arreglo = highbeta)
	erhighbeta = FFT.obtenerEjeReal()
	eihighbeta = FFT.obtenerEjeImaginario()

	FFT = TransformadaRapidaFourier.TransformadaRapidaFourier(arreglo = lowgamma)
	erlowgamma = FFT.obtenerEjeReal()
	eilowgamma = FFT.obtenerEjeImaginario()

	FFT = TransformadaRapidaFourier.TransformadaRapidaFourier(arreglo = midgamma)
	ermidgamma = FFT.obtenerEjeReal()
	eimidgamma = FFT.obtenerEjeImaginario()

	FFT = TransformadaRapidaFourier.TransformadaRapidaFourier(arreglo = meditation)
	ermeditation = FFT.obtenerEjeReal()
	eimeditation = FFT.obtenerEjeImaginario()

	FFT = TransformadaRapidaFourier.TransformadaRapidaFourier(arreglo = attention)
	erattention = FFT.obtenerEjeReal()
	eiattention = FFT.obtenerEjeImaginario()
	'''
	archivoEscritura = open(rutaDestino + nombre, "w")
	for x in range(len(lineas)):
		linea = str(magnitudDelta[x]) + "," + str(faseDelta[x]) + "\n"
		'''
		linea += str(ertheta[x]) + "," + str(eitheta[x]) + ","
		linea += str(erlowalpha[x]) + "," + str(eilowalpha[x]) + ","
		linea += str(erhighalpha[x]) + "," + str(eihighalpha[x]) + ","
		linea += str(erlowbeta[x]) + "," + str(eilowbeta[x]) + ","
		linea += str(erhighbeta[x]) + "," + str(eihighbeta[x]) + ","
		linea += str(erlowgamma[x]) + "," + str(eilowgamma[x]) + ","
		linea += str(ermidgamma[x]) + "," + str(eimidgamma[x]) + ","
		linea += str(ermeditation[x]) + "," + str(eimeditation[x]) + ","
		linea += str(erattention[x]) + "," + str(eiattention[x]) + "\n"
		'''
		
		archivoEscritura.write(linea)

	archivoEscritura.close()


def crearGraficaMagnitudFase(rutaOrigen, rutaDestino, nombre):
	archivoLectura = open(rutaOrigen + nombre, "r")
	lineas = archivoLectura.readlines()

	# Canales
	deltaMagnitud = []
	deltaFase = []
	thetaReal = []
	thetaImag = []
	lowalphaReal = []
	lowalphaImag = []
	highalphaReal = []
	highalphaImag = []
	lowbetaReal = []
	lowbetaImag = []
	highbetaReal = []
	highbetaImag = []
	lowgammaReal = []
	lowgammaImag = []
	midgammaReal = []
	midgammaImag = []

	# Datos Adicionales
	meditationReal = []
	meditationImag = []
	attentionReal = []
	attentionImag = []

	for linea in lineas:
		elementos = linea.split(',')
		deltaMagnitud.append(elementos[0])
		deltaFase.append(elementos[1])
		'''
		thetaReal.append(elementos[2])
		thetaImag.append(elementos[3])
		lowalphaReal.append(elementos[4])
		lowalphaImag.append(elementos[5])
		highalphaReal.append(elementos[6])
		highalphaImag.append(elementos[7])
		lowbetaReal.append(elementos[8])
		lowbetaImag.append(elementos[9])
		highbetaReal.append(elementos[10])
		highbetaImag.append(elementos[11])
		lowgammaReal.append(elementos[12])
		lowgammaImag.append(elementos[13])
		midgammaReal.append(elementos[14])
		midgammaImag.append(elementos[15])
		meditationReal.append(elementos[16])
		meditationImag.append(elementos[17])
		attentionReal.append(elementos[18])
		attentionImag.append(elementos[19])
	'''
	nombre = nombre[:len(nombre)-4]
	
	# Grafica de canal Delta
	plt.subplot(3,3,1)
	plt.plot(deltaFase,deltaMagnitud)
	# Limitar los valores de los ejes.
	#plt.xlim(0, xlimite)
	plt.axhline(0, color="black")
	plt.axvline(0, color="black")
	plt.title('Magnitud y Fase Canal Delta')
	plt.xlabel(u'Fase (-π, π)')
	plt.ylabel(u'Magnitud')
	'''
	# Grafica de canal Theta
	plt.subplot(3,3,2)
	plt.plot(thetaReal,thetaImag)
	# Limitar los valores de los ejes.
	#plt.xlim(0, xlimite)
	plt.axhline(0, color="black")
	plt.axvline(0, color="black")
	plt.title('FFT Canal Theta')
	plt.xlabel(u'Frecuencia Hz')
	plt.ylabel(u'Magnitud')

	# Grafica de canal Lowalpha
	plt.subplot(3,3,3)
	plt.plot(lowalphaReal,lowalphaImag)
	# Limitar los valores de los ejes.
	#plt.xlim(0, xlimite)
	plt.axhline(0, color="black")
	plt.axvline(0, color="black")
	plt.title('FFT Canal LowAlpha')
	plt.xlabel(u'Frecuencia Hz')
	plt.ylabel(u'Magnitud')

	# Grafica de canal Highalpha
	plt.subplot(3,3,4)
	plt.plot(highalphaReal,highalphaImag)
	# Limitar los valores de los ejes.
	#plt.xlim(0, xlimite)
	plt.axhline(0, color="black")
	plt.axvline(0, color="black")
	plt.title('FFT Canal HighAlpha')
	plt.xlabel(u'Frecuencia Hz')
	plt.ylabel(u'Magnitud')

	# Grafica de canal LowBeta
	plt.subplot(3,3,5)
	plt.plot(lowbetaReal,lowbetaImag)
	# Limitar los valores de los ejes.
	#plt.xlim(0, xlimite)
	plt.axhline(0, color="black")
	plt.axvline(0, color="black")
	plt.title('FFT Canal LowBeta')
	plt.xlabel(u'Frecuencia Hz')
	plt.ylabel(u'Magnitud')

	# Grafica de canal HighBeta
	plt.subplot(3,3,6)
	plt.plot(highbetaReal,highbetaImag)
	# Limitar los valores de los ejes
	#plt.xlim(0, xlimite)
	plt.axhline(0, color="black")
	plt.axvline(0, color="black")
	plt.title('FFT Canal HighBeta')
	plt.xlabel(u'Frecuencia Hz')
	plt.ylabel(u'Magnitud')

	# Grafica de canal LowGamma
	plt.subplot(3,3,7)
	plt.plot(lowgammaReal,lowgammaImag)
	# Limitar los valores de los ejes
	#plt.xlim(0, xlimite)
	plt.axhline(0, color="black")
	plt.axvline(0, color="black")
	plt.title('FFT Canal LowGamma')
	plt.xlabel(u'Frecuencia Hz')
	plt.ylabel(u'Magnitud')

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


generarMF("MuestrasTransformadas/","MuestrasMagnitudFase/",u"Miguel_Romero_GutiérrezRelajante.txt")
crearGraficaMagnitudFase("MuestrasMagnitudFase/","MuestrasGraficasMagnitudFase/",u"Miguel_Romero_GutiérrezRelajante.txt")


