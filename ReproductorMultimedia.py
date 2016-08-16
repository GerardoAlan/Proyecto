
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
        #plt.show()


