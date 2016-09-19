
#-*- coding:utf-8 -*-

import TransformadaRapidaFourier
import matplotlib.pyplot as plot
import numpy as np

def generarFFT(rutaOrigen, rutaDestino, nombre):
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
		theta.append(elementos[1])
		lowalpha.append(elementos[2])
		highalpha.append(elementos[3])
		lowbeta.append(elementos[4])
		highbeta.append(elementos[5])
		lowgamma.append(elementos[6])
		midgamma.append(elementos[7])
		meditation.append(elementos[8])
		attention.append(elementos[9])

	FFT = TransformadaRapidaFourier.TransformadaRapidaFourier(arreglo = delta)
	erdelta = FFT.obtenerEjeReal()
	eidelta = FFT.obtenerEjeImaginario()
	
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

	archivoEscritura = open(rutaDestino + nombre, "w")
	for x in range(len(lineas)):
		linea = str(erdelta[x]) + "," + str(eidelta[x]) + ","
		linea += str(ertheta[x]) + "," + str(eitheta[x]) + ","
		linea += str(erlowalpha[x]) + "," + str(eilowalpha[x]) + ","
		linea += str(erhighalpha[x]) + "," + str(eihighalpha[x]) + ","
		linea += str(erlowbeta[x]) + "," + str(eilowbeta[x]) + ","
		linea += str(erhighbeta[x]) + "," + str(eihighbeta[x]) + ","
		linea += str(erlowgamma[x]) + "," + str(eilowgamma[x]) + ","
		linea += str(ermidgamma[x]) + "," + str(eimidgamma[x]) + ","
		linea += str(ermeditation[x]) + "," + str(eimeditation[x]) + ","
		linea += str(erattention[x]) + "," + str(eiattention[x]) + "\n"

		archivoEscritura.write(linea)

	archivoEscritura.close()


def crearGraficaTransformada(rutaOrigen, rutaDestino, nombre):
	archivoLectura = open(rutaOrigen + nombre, "r")
	lineas = archivoLectura.readlines()

	# Canales
	deltaReal = []
	deltaImag = []
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
		deltaReal.append(elementos[0])
		deltaImag.append(elementos[1])
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
	
	nombre = nombre[:len(nombre)-4]
	
	# Grafica de canal Delta
	plot.subplot(3,3,1)
	plot.plot(deltaReal, deltaImag)
	# Limitar los valores de los ejes.
	#plot.xlim(0, xlimite)
	plot.axhline(0, color="black")
	plot.axvline(0, color="black")
	plot.title('FFT Canal Delta')
	plot.xlabel(u'Frecuencia Hz')
	plot.ylabel(u'Magnitud')

	# Grafica de canal Theta
	plot.subplot(3,3,2)
	plot.plot(thetaReal,thetaImag)
	# Limitar los valores de los ejes.
	#plot.xlim(0, xlimite)
	plot.axhline(0, color="black")
	plot.axvline(0, color="black")
	plot.title('FFT Canal Theta')
	plot.xlabel(u'Frecuencia Hz')
	plot.ylabel(u'Magnitud')

	# Grafica de canal Lowalpha
	plot.subplot(3,3,3)
	plot.plot(lowalphaReal,lowalphaImag)
	# Limitar los valores de los ejes.
	#plot.xlim(0, xlimite)
	plot.axhline(0, color="black")
	plot.axvline(0, color="black")
	plot.title('FFT Canal LowAlpha')
	plot.xlabel(u'Frecuencia Hz')
	plot.ylabel(u'Magnitud')

	# Grafica de canal Highalpha
	plot.subplot(3,3,4)
	plot.plot(highalphaReal,highalphaImag)
	# Limitar los valores de los ejes.
	#plot.xlim(0, xlimite)
	plot.axhline(0, color="black")
	plot.axvline(0, color="black")
	plot.title('FFT Canal HighAlpha')
	plot.xlabel(u'Frecuencia Hz')
	plot.ylabel(u'Magnitud')

	# Grafica de canal LowBeta
	plot.subplot(3,3,5)
	plot.plot(lowbetaReal,lowbetaImag)
	# Limitar los valores de los ejes.
	#plot.xlim(0, xlimite)
	plot.axhline(0, color="black")
	plot.axvline(0, color="black")
	plot.title('FFT Canal LowBeta')
	plot.xlabel(u'Frecuencia Hz')
	plot.ylabel(u'Magnitud')

	# Grafica de canal HighBeta
	plot.subplot(3,3,6)
	plot.plot(highbetaReal,highbetaImag)
	# Limitar los valores de los ejes
	#plot.xlim(0, xlimite)
	plot.axhline(0, color="black")
	plot.axvline(0, color="black")
	plot.title('FFT Canal HighBeta')
	plot.xlabel(u'Frecuencia Hz')
	plot.ylabel(u'Magnitud')

	# Grafica de canal LowGamma
	plot.subplot(3,3,7)
	plot.plot(lowgammaReal,lowgammaImag)
	# Limitar los valores de los ejes
	#plot.xlim(0, xlimite)
	plot.axhline(0, color="black")
	plot.axvline(0, color="black")
	plot.title('FFT Canal LowGamma')
	plot.xlabel(u'Frecuencia Hz')
	plot.ylabel(u'Magnitud')

	# Grafica de canal MidGamma
	plot.subplot(3,3,8)
	plot.plot(midgammaReal,midgammaImag)
	# Limitar los valores de los ejes
	#plot.xlim(0, xlimite)
	plot.axhline(0, color="black")
	plot.axvline(0, color="black")
	plot.title('FFT Canal MidGamma')
	plot.xlabel(u'Frecuencia Hz')
	plot.ylabel(u'Magnitud')

	# Grafica de atencion y meditacion
	plot.subplot(3,3,9)
	plot.plot(meditationReal,meditationImag, 'b-' ,label=u"Meditation")
	plot.plot(attentionReal,attentionImag, 'g',label= u"Attention")
	#plot.plot(x, [poorSignal[i] for i in x], 'r' , label=u"PoorSignal")
	plot.legend(shadow = True, fancybox= True)

	# Limitar los valores de los ejes.
	#plot.xlim(0, xlimite)

	# Establecer el color de los ejes.
	plot.axhline(0, color="black")
	plot.axvline(0, color="black")
	plot.title('FFT Datos Adicionales')
	plot.xlabel(u'Frecuencia Hz')
	plot.ylabel(u'Magnitud')

	# Mostramos en pantalla
	manager = plot.get_current_fig_manager()
	manager.window.showMaximized()
	plot.tight_layout()

	plot.savefig(rutaDestino + nombre + ".png")
	plot.show()


generarFFT("MuestrasFormato/","MuestrasTransformadas/",u"Miguel_Romero_GutiérrezRelajante.txt")
crearGraficaTransformada("MuestrasTransformadas/","GraficasTransformadas/",u"Miguel_Romero_GutiérrezRelajante.txt")


