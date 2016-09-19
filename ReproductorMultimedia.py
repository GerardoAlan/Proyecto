
#-*- coding:utf-8 -*-

import threading
import time
import os
import sys
from PyQt4 import QtGui, QtCore
from PyQt4.phonon import Phonon
import scipy as sp
import matplotlib.pyplot as plt
import ThinkGearProtocol
import logging
import logging.handlers

import TransformadaRapidaFourier
import matplotlib.pyplot as plot
import numpy as np

import MagnitudFase
import QuickSort
import matplotlib.pyplot as plotMF


class ReproductorMultimedia(QtGui.QWidget):

    def __init__(self, name=None, archivo=None, ruta=None):
        super(ReproductorMultimedia, self).__init__()

        self.puerto = "COM10"

        rutaAbs = os.path.abspath(os.path.curdir)
        self.ruta = rutaAbs + ruta
        self.carpeta = "Muestras/"
        self.carpetaDestino = "MuestrasFormato/"
        self.carpetaImagen = "MuestrasGraficas/"

        self.setWindowTitle('Reproductor Multimedia')
        self.media = Phonon.MediaObject(self)
        self.media.stateChanged.connect(self.handleStateChanged)
        self.video = Phonon.VideoWidget(self)
        self.video.setMinimumSize(800, 400)
        self.audio = Phonon.AudioOutput(Phonon.VideoCategory, self)
        Phonon.createPath(self.media, self.audio)
        Phonon.createPath(self.media, self.video)
        self.button = QtGui.QPushButton('Reproducir Video', self)
        self.button.clicked.connect(self.handleButton)
        self.button.setMinimumSize(100, 30)
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.video, 1)
        layout.addWidget(self.button)
        self.closeThread = False
        self.datos = name
        self.nombreArchivo = archivo
        self.setWindowIcon(QtGui.QIcon('Icon/icon.jpg'))
        self.show()

    # Se acciona cuando se pulsa el boton
    def handleButton(self):
        if self.media.state() == Phonon.PlayingState:
            # Entra cuando se esta reproduciendo el video
            self.media.stop()
            self.closeThread = True
        else:
            # Entra cuando el video no se esta reproduciendo

            self.media.setCurrentSource(Phonon.MediaSource(self.ruta))

            # Se crea el hilo y se ejecuta
            self.t = threading.Thread(target=self.guardarDatos, args=(self.puerto, self.nombreArchivo, self.datos, ))
            self.t.start()

            # Se reproduce el video
            self.media.play()

    # Se acciona cuando ocurre un evento
    def handleStateChanged(self, newstate, oldstate):
        if newstate == Phonon.PlayingState:
            self.button.setText('Detener')
        elif (newstate != Phonon.LoadingState and
              newstate != Phonon.BufferingState):
            self.media.stop()
            self.closeThread = True

            # Crear el archivo con el formato
            self.convertirArchivo(self.carpeta, self.carpetaDestino, self.nombreArchivo+".txt")
            # Crear la grafica con el archivo ya formateado
            self.crearGrafica(self.carpetaDestino,self.carpetaImagen, self.nombreArchivo+".txt")

        
            # FFT
            self.generarFFT("MuestrasFormato/","MuestrasTransformadas/",self.nombreArchivo+".txt")
            self.crearGraficaTransformada("MuestrasTransformadas/","GraficasTransformadas/",self.nombreArchivo+".txt")

            
            # Representacion de la FFT con su magnitud y fase ordenadas para poderlas graficar
            self.generarMagnitudFase("MuestrasTransformadas/","MuestrasMagnitudFase/",self.nombreArchivo+".txt")
            self.crearGraficaMagnitudFase("MuestrasMagnitudFase/","GraficasMagnitudFase/",self.nombreArchivo+".txt")
            

            self.close()
            
            if newstate == Phonon.ErrorState:
                source = self.media.currentSource().fileName()
                print('ERROR: could not play:', source.toLocal8Bit().data())
                print('  %s' % self.media.errorString().toLocal8Bit().data())

    # Metodo que almacena los datos en un archivo
    def guardarDatos(self, puerto, nombre, datosUsuario):
        global packet_log
        packet_log = []
        logging.basicConfig(level=logging.DEBUG)

        nombre = str(nombre)
        archi = open(self.carpeta + nombre + ".txt", 'w')
        archi.write(datosUsuario + "\n")
        tg = ThinkGearProtocol.ThinkGearProtocol(puerto)

        for pkt in tg.get_packets():
            for powerData in pkt:
                if isinstance(powerData, ThinkGearProtocol.ThinkGearEEGPowerData):
                    archi.write(str(powerData.value))
            for meditation in pkt:
                if isinstance(meditation, ThinkGearProtocol.ThinkGearMeditationData):
                    archi.write("Meditation: " + str(meditation.value) + ", ")
            for attention in pkt:
                if isinstance(attention, ThinkGearProtocol.ThinkGearAttentionData):
                    archi.write("Attention: " + str(attention.value) + ", ")
            for poorSignal in pkt:
                if isinstance(poorSignal, ThinkGearProtocol.ThinkGearPoorSignalData):
                    archi.write("PoorSignal: " + str(poorSignal.value) + "\n")

            if (self.closeThread):
                archi.close()
                tg.closeSerial()
                break

    def convertirArchivo(self, rutaOrigen, rutaDestino, nombre):

        archivoLectura = open(rutaOrigen + nombre, "r")
        archivoEscritura = open(rutaDestino + nombre, "w")

        primeraLinea = False

        lineas = archivoLectura.readlines()

        for linea in lineas:

            if primeraLinea:
                deltaPosicionComa = linea.find(",")
                valorDelta = linea[19:deltaPosicionComa]
                nuevaLinea = valorDelta + ","

                thetaPosicionComa = linea.find(",", deltaPosicionComa + 1)
                valorTheta = linea[deltaPosicionComa + 8:thetaPosicionComa]
                nuevaLinea += valorTheta + ","

                lowalphaPosicionComa = linea.find(",", thetaPosicionComa + 1)
                valorLowAlpha = linea[thetaPosicionComa + 11:lowalphaPosicionComa]
                nuevaLinea += valorLowAlpha + ","

                highalphaPosicionComa = linea.find(",", lowalphaPosicionComa + 1)
                valorHighAlpha = linea[lowalphaPosicionComa + 12:highalphaPosicionComa]
                nuevaLinea += valorHighAlpha + ","

                lowbetaPosicionComa = linea.find(",", highalphaPosicionComa + 1)
                valorLowBeta = linea[highalphaPosicionComa + 10:lowbetaPosicionComa]
                nuevaLinea += valorLowBeta + ","

                highbetaPosicionComa = linea.find(",", lowbetaPosicionComa + 1)
                valorHighBeta = linea[lowbetaPosicionComa + 11:highbetaPosicionComa]
                nuevaLinea += valorHighBeta + ","

                lowgammaPosicionComa = linea.find(",", highbetaPosicionComa + 1)
                valorLowGamma = linea[highbetaPosicionComa + 11:lowgammaPosicionComa]
                nuevaLinea += valorLowGamma + ","

                midgammaPosicionParentesis = linea.find(")")
                valorMidGamma = linea[lowgammaPosicionComa + 11:midgammaPosicionParentesis]
                nuevaLinea += valorMidGamma + ","

                meditationPosicionComa = linea.find(",", midgammaPosicionParentesis + 1)
                valorMeditation = linea[midgammaPosicionParentesis + 13:meditationPosicionComa]
                nuevaLinea += valorMeditation + ","

                attentionPosicionComa = linea.find(",", meditationPosicionComa + 1)
                valorAttention = linea[meditationPosicionComa + 13:attentionPosicionComa]
                nuevaLinea += valorAttention + ","

                nuevaLinea += linea[attentionPosicionComa + 14:]

                if valorDelta=="0" and valorTheta=="0" and valorLowAlpha=="0" and valorHighAlpha=="0" and valorLowBeta=="0" and valorHighBeta=="0" and valorLowGamma=="0" and valorMidGamma=="0" and valorMeditation=="0" and valorAttention=="0":
                    pass
                else:
                    archivoEscritura.write(nuevaLinea)
            else:
                primeraLinea = True

        archivoLectura.close()
        archivoEscritura.close()

    def crearGrafica(self, rutaDestino, rutaImagen, nombre):
        archivoLectura = open(rutaDestino + nombre, "r")
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

        # Datos Adicionales
        meditation = []
        attention = []
        poorSignal = []

        contador = 0

        for linea in lineas:

            deltaPosicionComa = linea.find(",")
            delta.append(linea[:deltaPosicionComa])

            thetaPosicionComa = linea.find(",", deltaPosicionComa+1)
            theta.append(linea[deltaPosicionComa+1:thetaPosicionComa])

            lowalphaPosicionComa = linea.find(",", thetaPosicionComa+1)
            lowalpha.append(linea[thetaPosicionComa+1:lowalphaPosicionComa])

            highalphaPosicionComa = linea.find(",", lowalphaPosicionComa+1)
            highalpha.append(linea[lowalphaPosicionComa+1:highalphaPosicionComa])

            lowbetaPosicionComa = linea.find(",", highalphaPosicionComa+1)
            lowbeta.append(linea[highalphaPosicionComa+1:lowbetaPosicionComa])

            highbetaPosicionComa = linea.find(",", lowbetaPosicionComa+1)
            highbeta.append(linea[lowbetaPosicionComa+1:highbetaPosicionComa])

            lowgammaPosicionComa = linea.find(",", highbetaPosicionComa+1)
            lowgamma.append(linea[highbetaPosicionComa+1:lowgammaPosicionComa])

            midgammaPosicionComa = linea.find(",", lowgammaPosicionComa+1)
            midgamma.append(linea[lowgammaPosicionComa+1:midgammaPosicionComa])

            meditationPosicionComa = linea.find(",", midgammaPosicionComa+1)
            meditation.append(linea[midgammaPosicionComa+1:meditationPosicionComa])

            attentionPosicionComa = linea.find(",", meditationPosicionComa+1)
            attention.append(linea[meditationPosicionComa+1:attentionPosicionComa])

            poorSignalPosicionComa = linea.find(",", attentionPosicionComa+1)
            poorSignal.append(linea[attentionPosicionComa+1:poorSignalPosicionComa])

            contador += 1

        nombre = nombre[:len(nombre)-4]
        video = nombre[len(nombre)-6:]
        if video=="Estres":
            video = "Estresor"
        else:
            video = "Relajante"

        xlimite = len(lineas)-1

        # Creamos el array x de la medida de los datos
        x = range(0, xlimite)

        # Grafica de canal Delta
        plt.subplot(3,3,1)
        plt.plot(x, [delta[i] for i in x])
        # Limitar los valores de los ejes.
        plt.xlim(0, xlimite)
        plt.title('Canal Delta')
        plt.xlabel(u'Tiempo(t)')
        plt.ylabel(u'Representación numerica')

        # Grafica de canal Theta
        plt.subplot(3,3,2)
        plt.plot(x, [theta[i] for i in x])
        # Limitar los valores de los ejes.
        plt.xlim(0, xlimite)
        plt.title('Canal Theta')
        plt.xlabel(u'Tiempo(t)')
        plt.ylabel(u'Representación numerica')

        # Grafica de canal Lowalpha
        plt.subplot(3,3,3)
        plt.plot(x, [lowalpha[i] for i in x])
        # Limitar los valores de los ejes.
        plt.xlim(0, xlimite)
        plt.title('Canal LowAlpha')
        plt.xlabel(u'Tiempo(t)')
        plt.ylabel(u'Representación numerica')

        # Grafica de canal Highalpha
        plt.subplot(3,3,4)
        plt.plot(x, [highalpha[i] for i in x])
        # Limitar los valores de los ejes.
        plt.xlim(0, xlimite)
        plt.title('Canal HighAlpha')
        plt.xlabel(u'Tiempo(t)')
        plt.ylabel(u'Representación numerica')

        # Grafica de canal LowBeta
        plt.subplot(3,3,5)
        plt.plot(x, [lowbeta[i] for i in x])
        # Limitar los valores de los ejes.
        plt.xlim(0, xlimite)
        plt.title('Canal LowBeta')
        plt.xlabel(u'Tiempo(t)')
        plt.ylabel(u'Representación numerica')

        # Grafica de canal HighBeta
        plt.subplot(3,3,6)
        plt.plot(x, [highbeta[i] for i in x])
        # Limitar los valores de los ejes
        plt.xlim(0, xlimite)
        plt.title('Canal HighBeta')
        plt.xlabel('Tiempo(t)')
        plt.ylabel(u'Representación numerica')

        # Grafica de canal LowGamma
        plt.subplot(3,3,7)
        plt.plot(x, [lowgamma[i] for i in x])
        # Limitar los valores de los ejes
        plt.xlim(0, xlimite)
        plt.title('Canal LowGamma')
        plt.xlabel('Tiempo(t)')
        plt.ylabel(u'Representación numerica')

        # Grafica de canal MidGamma
        plt.subplot(3,3,8)
        plt.plot(x, [midgamma[i] for i in x])
        # Limitar los valores de los ejes
        plt.xlim(0, xlimite)
        plt.title('Canal MidGamma')
        plt.xlabel('Tiempo(t)')
        plt.ylabel(u'Representación numerica')

        # Grafica de atencion, meditacion y fuerza de la senal

        plt.subplot(3,3,9)
        plt.plot(x, [meditation[i] for i in x], 'b-' ,label=u"Meditation")
        plt.plot(x, [attention[i] for i in x], 'g',label= u"Attention")
        plt.plot(x, [poorSignal[i] for i in x], 'r' , label=u"PoorSignal")
        plt.legend(shadow = True, fancybox= True)

        # Limitar los valores de los ejes.
        plt.xlim(0, xlimite)

        # Establecer el color de los ejes.
        plt.axhline(0, color="black")
        plt.axvline(0, color="black")
        plt.title('Datos Adicionales')
        plt.xlabel(u'Tiempo(t)')
        plt.ylabel(u'Representación numerica')

        # Mostramos en pantalla
        manager = plt.get_current_fig_manager()
        manager.window.showMaximized()
        plt.tight_layout()

        plt.savefig(rutaImagen + nombre + ".png")
        plt.close()
        #plt.show()


    def generarFFT(self, rutaOrigen, rutaDestino, nombre):
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


    def crearGraficaTransformada(self, rutaOrigen, rutaDestino, nombre):
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
        plot.close()
        #plot.show()
    

    def generarMagnitudFase(self, rutaOrigen, rutaDestino, nombre):
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
            midgamma.append(elementos[14])
            midgamma.append(elementos[15])
            meditation.append(elementos[16])
            meditation.append(elementos[17])
            attention.append(elementos[18])
            attention.append(elementos[19])
            
        # Procedemos a obtener la Magnitud y la Fase de dichos valores utilizando la clase GeneradorMagnitudFase
        
        # Asignamos al constructor el canal Delta
        MF = MagnitudFase.MagnitudFase(arreglo = delta)
        # Obtenemos el arreglo que representa la Magnitud de Delta
        magnitudDelta = MF.obtenerMagnitud()
        # Obtenemos el arreglo que representa la Fase de Delta
        faseDelta = MF.obtenerFase()
        # El metodo ordenarFase requiere el arreglo que representa la Fase y Magnitud de Delta
        # Posterior a ello regresa la direccion de los arreglos ya ordenados y limpios (Fase > 0)
        faseDelta,magnitudDelta = self.ordenarFase(faseDelta, magnitudDelta)
        
        # Realizamos el mismo procedimiento para los siguientes Canales
        
        # Canal Thetha
        MF = MagnitudFase.MagnitudFase(arreglo = theta)
        faseTheta = MF.obtenerFase()
        magnitudTheta = MF.obtenerMagnitud()
        faseTheta,magnitudTheta = self.ordenarFase(faseTheta, magnitudTheta)
        
        # Canal Lowalpha
        MF = MagnitudFase.MagnitudFase(arreglo = lowalpha)
        faseLowalpha = MF.obtenerFase()
        magnitudLowalpha = MF.obtenerMagnitud()
        faseLowalpha,magnitudLowalpha = self.ordenarFase(faseLowalpha, magnitudLowalpha)
    
        # Canal Highalpha
        MF = MagnitudFase.MagnitudFase(arreglo = highalpha)
        faseHighalpha = MF.obtenerFase()
        magnitudHighalpha = MF.obtenerMagnitud()
        faseHighalpha,magnitudHighalpha = self.ordenarFase(faseHighalpha, magnitudHighalpha)
        
        # Canal Lowbeta
        MF = MagnitudFase.MagnitudFase(arreglo = lowbeta)
        faseLowbeta = MF.obtenerFase()
        magnitudLowbeta = MF.obtenerMagnitud()
        faseLowbeta,magnitudLowbeta = self.ordenarFase(faseLowbeta, magnitudLowbeta)
        
        # Canal Highbeta
        MF = MagnitudFase.MagnitudFase(arreglo = highbeta)
        faseHighbeta = MF.obtenerFase()
        magnitudHighbeta = MF.obtenerMagnitud()
        faseHighbeta,magnitudHighbeta = self.ordenarFase(faseHighbeta, magnitudHighbeta)
    
        # Canal Lowgamma
        MF = MagnitudFase.MagnitudFase(arreglo = lowgamma)
        faseLowgamma = MF.obtenerFase()
        magnitudLowgamma = MF.obtenerMagnitud()
        faseLowgamma,magnitudLowgamma = self.ordenarFase(faseLowgamma, magnitudLowgamma)
        
        # Canal Midgamma
        MF = MagnitudFase.MagnitudFase(arreglo = midgamma)
        faseMidgamma = MF.obtenerFase()
        magnitudMidgamma = MF.obtenerMagnitud()
        faseMidgamma,magnitudMidgamma = self.ordenarFase(faseMidgamma, magnitudMidgamma)
    
        # Canal Meditation
        MF = MagnitudFase.MagnitudFase(arreglo = meditation)
        faseMeditation = MF.obtenerFase()
        magnitudMeditation = MF.obtenerMagnitud()
        faseMeditation,magnitudMeditation = self.ordenarFase(faseMeditation, magnitudMeditation)
    
        # Canal Attention
        MF = MagnitudFase.MagnitudFase(arreglo = attention)
        faseAttention = MF.obtenerFase()
        magnitudAttention = MF.obtenerMagnitud()
        faseAttention,magnitudAttention = self.ordenarFase(faseAttention, magnitudAttention)
            
            
        # Para obtener las longitudes de cada Fase
        longitudDelta = len(faseDelta)
        longitudTheta = len(faseTheta)
        longitudLowalpha = len(faseLowalpha)
        longitudHighalpha = len(faseHighalpha)
        longitudLowbeta = len(faseLowbeta)
        longitudHighbeta = len(faseHighbeta)
        longitudLowgamma = len(faseLowgamma)
        longitudMidgamma = len(faseMidgamma)
        longitudMeditation = len(faseMeditation)
        longitudAttention = len(faseAttention)
        
        longitudMaxima = self.calcularLongitudMaxima(longitudDelta,longitudTheta,longitudLowalpha,longitudHighalpha,longitudLowbeta,longitudHighbeta,longitudLowgamma,longitudMidgamma,longitudMeditation,longitudAttention)    
        
        # Abrimos un archivo para escribir la Magnitud y Fase obtenidos para cada canal
        archivoEscritura = open(rutaDestino + nombre, "w")
        for x in range(longitudMaxima):
            linea = ""
            linea += self.crearLinea(x, longitudDelta, magnitudDelta, faseDelta)
            linea += self.crearLinea(x, longitudTheta, magnitudTheta, faseTheta)
            linea += self.crearLinea(x, longitudLowalpha, magnitudLowalpha, faseLowalpha)
            linea += self.crearLinea(x, longitudHighalpha, magnitudHighalpha, faseHighalpha)
            linea += self.crearLinea(x, longitudLowbeta, magnitudLowbeta, faseLowbeta)
            linea += self.crearLinea(x, longitudHighbeta, magnitudHighbeta, faseHighbeta)
            linea += self.crearLinea(x, longitudLowgamma, magnitudLowgamma, faseLowgamma)
            linea += self.crearLinea(x, longitudMidgamma, magnitudMidgamma, faseMidgamma)
            linea += self.crearLinea(x, longitudMeditation, magnitudMeditation, faseMeditation)
            linea += self.crearLinea(x, longitudAttention, magnitudAttention, faseAttention)
    
            linea += "\n"
            
            archivoEscritura.write(linea)
    
        archivoEscritura.close()
    
    # Metodo para obtener el arreglo mas largo
    def calcularLongitudMaxima(self, longitudDelta, longitudTheta, longitudLowalpha, longitudHighalpha, longitudLowbeta, longitudHighbeta, longitudLowgamma, longitudMidgamma, longitudMeditation, longitudAttention):
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
        if longitudMidgamma > longitudMaxima:
            longitudMaxima = longitudMidgamma
        if longitudMeditation > longitudMaxima:
            longitudMaxima = longitudMeditation
        if longitudAttention > longitudMaxima:
            longitudMaxima = longitudAttention
            
        return longitudMaxima
    
    # Metodo que evalua si el canal aun puede escribir el dato, en cuyo caso lo obtiene de los arreglos y lo retorna
    def crearLinea(self, posicionActual, longitudCanal, magnitud, fase):
        if posicionActual < longitudCanal:
            return str(magnitud[posicionActual]) + "," + str(fase[posicionActual]) + ","
        else:
            return " , ,"
    
    # Metodo que se encarga de ordenar el arreglo fase y modificar los dos arreglos manteniendo la relacion entre ellos
    def ordenarFase(self, fase, magnitud):
        
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
    def crearGraficaMagnitudFase(self, rutaOrigen, rutaDestino, nombre):
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
        midgammaMagnitud = []
        midgammaFase = []
    
        # Datos Adicionales
        meditationMagnitud = []
        meditationFase = []
        attentionMagnitud = []
        attentionFase = []
    
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
            if elementos[14] != " ":
                midgammaMagnitud.append(elementos[14])
                midgammaFase.append(elementos[15])    
            if elementos[16] != " ":
                meditationMagnitud.append(elementos[16])
                meditationFase.append(elementos[17])    
            if elementos[18] != " ":
                attentionMagnitud.append(elementos[18])
                attentionFase.append(elementos[19])    
                
        # Para quitarle al nombre el .txt del final    
        nombre = nombre[:len(nombre)-4]
        
        # Grafica de canal Delta
        plotMF.subplot(3,3,1)
        plotMF.plot(deltaFase, deltaMagnitud)
        # Configurar grafica
        plotMF.xlim(0, 3.2) # limite en x de 0 a 3.2 ya que el mayor es pi
        plotMF.axhline(0, color="black")
        plotMF.axvline(0, color="black")
        plotMF.title('Magnitud y Fase Canal Delta')
        plotMF.xlabel(u'Fase (0, π)')
        plotMF.ylabel(u'Magnitud')
        
        # Grafica de canal Theta
        plotMF.subplot(3,3,2)
        plotMF.plot(thetaFase, thetaMagnitud)
        # Configurar grafica
        plotMF.xlim(0, 3.2) # limite en x de 0 a 3.2 ya que el mayor es pi
        plotMF.axhline(0, color="black")
        plotMF.axvline(0, color="black")
        plotMF.title('Magnitud y Fase Canal Theta')
        plotMF.xlabel(u'Fase (0, π)')
        plotMF.ylabel(u'Magnitud')
    
        # Grafica de canal Lowalpha
        plotMF.subplot(3,3,3)
        plotMF.plot(lowalphaFase, lowalphaMagnitud)
        # Configurar grafica
        plotMF.xlim(0, 3.2) # limite en x de 0 a 3.2 ya que el mayor es pi
        plotMF.axhline(0, color="black")
        plotMF.axvline(0, color="black")
        plotMF.title('Magnitud y Fase Canal Lowalpha')
        plotMF.xlabel(u'Fase (0, π)')
        plotMF.ylabel(u'Magnitud')
    
        # Grafica de canal Highalpha
        plotMF.subplot(3,3,4)
        plotMF.plot(highalphaFase, highalphaMagnitud)
        # Configurar grafica
        plotMF.xlim(0, 3.2) # limite en x de 0 a 3.2 ya que el mayor es pi
        plotMF.axhline(0, color="black")
        plotMF.axvline(0, color="black")
        plotMF.title('Magnitud y Fase Canal Highalpha')
        plotMF.xlabel(u'Fase (0, π)')
        plotMF.ylabel(u'Magnitud')
    
        # Grafica de canal Lowbeta
        plotMF.subplot(3,3,5)
        plotMF.plot(lowbetaFase, lowbetaMagnitud)
        # Configurar grafica
        plotMF.xlim(0, 3.2) # limite en x de 0 a 3.2 ya que el mayor es pi
        plotMF.axhline(0, color="black")
        plotMF.axvline(0, color="black")
        plotMF.title('Magnitud y Fase Canal Lowbeta')
        plotMF.xlabel(u'Fase (0, π)')
        plotMF.ylabel(u'Magnitud')
    
        # Grafica de canal Highbeta
        plotMF.subplot(3,3,6)
        plotMF.plot(highbetaFase, highbetaMagnitud)
        # Configurar grafica
        plotMF.xlim(0, 3.2) # limite en x de 0 a 3.2 ya que el mayor es pi
        plotMF.axhline(0, color="black")
        plotMF.axvline(0, color="black")
        plotMF.title('Magnitud y Fase Canal Highbeta')
        plotMF.xlabel(u'Fase (0, π)')
        plotMF.ylabel(u'Magnitud')
    
        # Grafica de canal Lowgamma
        plotMF.subplot(3,3,7)
        plotMF.plot(lowgammaFase, lowgammaMagnitud)
        # Configurar grafica
        plotMF.xlim(0, 3.2) # limite en x de 0 a 3.2 ya que el mayor es pi
        plotMF.axhline(0, color="black")
        plotMF.axvline(0, color="black")
        plotMF.title('Magnitud y Fase Canal Lowgamma')
        plotMF.xlabel(u'Fase (0, π)')
        plotMF.ylabel(u'Magnitud')
    
        # Grafica de canal Midgamma
        plotMF.subplot(3,3,8)
        plotMF.plot(midgammaFase, midgammaMagnitud)
        # Configurar grafica
        plotMF.xlim(0, 3.2) # limite en x de 0 a 3.2 ya que el mayor es pi
        plotMF.axhline(0, color="black")
        plotMF.axvline(0, color="black")
        plotMF.title('Magnitud y Fase Canal Midgamma')
        plotMF.xlabel(u'Fase (0, π)')
        plotMF.ylabel(u'Magnitud')
    
    
        # Grafica de atencion y meditacion
        plotMF.subplot(3,3,9)
        plotMF.plot(meditationFase,meditationMagnitud, 'b-' ,label=u"Meditation")
        plotMF.plot(attentionFase,attentionMagnitud, 'g',label= u"Attention")
        #plotMF.plot(x, [poorSignal[i] for i in x], 'r' , label=u"PoorSignal")
        plotMF.legend(shadow = True, fancybox= True)
    
        # Limitar los valores de los ejes.
        plotMF.xlim(0, 3.2) # limite en x de 0 a 3.2 ya que el mayor es pi
        
        # Establecer el color de los ejes.
        plotMF.axhline(0, color="black")
        plotMF.axvline(0, color="black")
        plotMF.title('Magnitud y Fase Datos Adicionales')
        plotMF.xlabel(u'Fase (0, π)')
        plotMF.ylabel(u'Magnitud')
    
                    
        # Mostramos en pantalla
        manager = plotMF.get_current_fig_manager()
        manager.window.showMaximized()
        plotMF.tight_layout()
    
        plotMF.savefig(rutaDestino + nombre + ".png")
        plotMF.close()
        #plotMF.show()
    
