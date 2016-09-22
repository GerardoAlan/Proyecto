
#-*- coding:utf-8 -*-
import threading
import sys
import os
from PyQt4 import QtGui
import ReproductorMultimedia
import CuestionarioEstres
import ThinkGearProtocol
import subprocess
import logging
import logging.handlers
import time
import matplotlib.pyplot as plt
import numpy as np
import RegistroUsuario

class MenuUsuario(QtGui.QWidget):

    def __init__(self, name=None, archivo=None):
        super(MenuUsuario, self).__init__()
        self.puerto = 'COM10'
        self.btnWidth = 235
        self.btnHigh = 40
        self.widWidth = 300
        self.widHigh = 340
        self.duracion = 300
        self.children = []
        self.datos = name
        self.archivo = archivo
        self.rutaVideoEstres = "/Video/videoEstres.wmv"
        self.rutaVideoRelajante = "/Video/videoRelajacion.wmv"
        
        self.rutaCuestionarioEstres = "Cuestionario/Estres/"
        self.rutaCuestionarioPuntuacion = "Cuestionario/Puntuacion/"
        
        self.rutaJuego = "DatoEstimulo/Juego/Muestra/"
        self.rutaJuegoGrafica = "DatoEstimulo/Juego/Grafica/"
        self.rutaJuegoFormato = "DatoEstimulo/Juego/Formato/"
        
        self.rutaEstres = "DatoEstimulo/VideoEstres/Muestra/"
        self.rutaEstresGrafica = "DatoEstimulo/VideoEstres/Grafica/"
        self.rutaEstresFormato = "DatoEstimulo/VideoEstres/Formato/"
        
        self.rutaRelajacion = "DatoEstimulo/VideoRelajante/Muestra/"
        self.rutaRelajacionGrafica = "DatoEstimulo/VideoRelajante/Grafica/"
        self.rutaRelajacionFormato = "DatoEstimulo/VideoRelajante/Formato/"
        self.closeThread = False
        self.initUI()

    def initUI(self):

        marginLeft = 33
        contTop = 30

        buttonContenidoMultimediaE = QtGui.QPushButton(
            'Presentar Contenido Estresor', self)
        buttonContenidoMultimediaE.clicked.connect(
            self.presentarContenidoMultimediaEstresor)
        buttonContenidoMultimediaE.move(marginLeft, contTop)
        
        contTop += 52
        buttonJuegoEstresante = QtGui.QPushButton(
            'Presentar Juego Online', self)
        buttonJuegoEstresante.clicked.connect(
            self.grabarJuegoEstresante)
        buttonJuegoEstresante.move(marginLeft, contTop)

        contTop += 52
        buttonTestMatematico = QtGui.QPushButton(
            u'Presentar Test Matemático', self)
        buttonTestMatematico.clicked.connect(self.presentarContenidoMatematico)
        buttonTestMatematico.move(marginLeft, contTop)

        contTop += 52
        buttonContenidoMultimediaR = QtGui.QPushButton('Presentar Contenido Relajante', self)
        buttonContenidoMultimediaR.clicked.connect(self.presentarContenidoMultimediaRelajante)
        buttonContenidoMultimediaR.move(marginLeft, contTop)

        contTop += 52
        buttonCuestionario = QtGui.QPushButton('Realizar Cuestionario', self)
        buttonCuestionario.clicked.connect(self.presentarCuestionarioEstres)
        buttonCuestionario.move(marginLeft, contTop)


        contTop += 52
        buttonSalir = QtGui.QPushButton(
            'Salir', self)
        buttonSalir.clicked.connect(
            self.salirMenuUsuario)
        buttonSalir.move(marginLeft+160, contTop)


        buttonContenidoMultimediaE.setMinimumSize(self.btnWidth, self.btnHigh)
        buttonJuegoEstresante.setMinimumSize(self.btnWidth, self.btnHigh)
        buttonTestMatematico.setMinimumSize(self.btnWidth, self.btnHigh)
        buttonContenidoMultimediaR.setMinimumSize(self.btnWidth, self.btnHigh)
        buttonCuestionario.setMinimumSize(self.btnWidth, self.btnHigh)
        buttonSalir.setMinimumSize(50, 30)

        self.setFixedSize(self.widWidth, self.widHigh)
        self.setWindowTitle('Menu de Usuario')
        self.setWindowIcon(QtGui.QIcon('Icon/icon.jpg'))
        self.show()

    def presentarContenidoMultimediaEstresor(self):
        nuevaVentana = ReproductorMultimedia.ReproductorMultimedia(
            puerto=self.puerto, name=self.datos, archivo=self.archivo, rutaVideo=self.rutaVideoEstres, carpeta=self.rutaEstres, carpetaDestino=self.rutaEstresFormato, carpetaImagen=self.rutaEstresGrafica,)
        self.children.append(nuevaVentana)

    def presentarContenidoMultimediaRelajante(self):
        nuevaVentana = ReproductorMultimedia.ReproductorMultimedia(
            puerto=self.puerto, name=self.datos, archivo=self.archivo, rutaVideo=self.rutaVideoRelajante, carpeta=self.rutaRelajacion, carpetaDestino=self.rutaRelajacionFormato, carpetaImagen=self.rutaRelajacionGrafica,)
        self.children.append(nuevaVentana)

    def grabarJuegoEstresante(self):
        self.juego = threading.Thread(target=self.ejecutarCatMario, args=())
        self.juego.start()
        # Se crea el hilo y se ejecuta
        self.t = threading.Thread(target=self.guardarDatos, args=(self.puerto, self.rutaJuego+self.archivo, ))
        self.t.start()
        time.sleep(self.duracion)
         
        # Detengo la grabacion
        self.closeThread = True
         
        # Creo el archivo limpio
        self.convertirArchivo(self.rutaJuego, self.rutaJuegoFormato, self.archivo+".txt")
         
        # Crear la grafica con el archivo ya formateado
        self.crearGrafica(self.rutaJuegoFormato,self.rutaJuegoFormato, self.archivo+".txt")

    def presentarContenidoMatematico(self):
        print"Holos"
        
    def presentarCuestionarioEstres(self):
        nuevaVentana = CuestionarioEstres.CuestionarioEstres(
            name=self.datos, archivo=self.rutaCuestionarioEstres + self.archivo)
        self.children.append(nuevaVentana)

    def ejecutarCatMario(self):
        os.chdir('C:\\Users\\Gerardo Alan\\workspace\\Proyecto\\JuegoCatMario')
        os.system('"C:\\Users\\Gerardo Alan\\workspace\\Proyecto\\JuegoCatMario\\Cat Mario.exe"' )    

    def salirMenuUsuario(self):
        self.close()
        
    # Metodo que almacena los datos en un archivo y se detiene despues de la duracion
    def guardarDatos(self, puerto, nombre):
        global packet_log
        packet_log = []
        logging.basicConfig(level=logging.DEBUG)

        nombre = str(nombre)
        archi = open(nombre + ".txt", 'w')
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

        lineas = archivoLectura.readlines()
        
        for linea in lineas:
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

            poorSignal = linea[attentionPosicionComa + 14:]
            nuevaLinea += poorSignal
            poorSignalInt = int(poorSignal)

            if (valorDelta=="0" and valorTheta=="0" and valorLowAlpha=="0" and valorHighAlpha=="0" and valorLowBeta=="0" and valorHighBeta=="0" and valorLowGamma=="0" and valorMidGamma=="0" and valorMeditation=="0" and valorAttention=="0")or(poorSignalInt > 25) :
                pass
            else:
                archivoEscritura.write(nuevaLinea)

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

    def closeEvent(self, event):
        msg = QtGui.QMessageBox()
        msg.setWindowIcon(QtGui.QIcon('Icon/icon.jpg'))
        msg.setWindowTitle('Aviso')
        msg.setText(u'¿Estás seguro de salir?')
        msg.addButton(QtGui.QPushButton('Aceptar'), QtGui.QMessageBox.YesRole)
        msg.addButton(QtGui.QPushButton('Cancelar'), QtGui.QMessageBox.NoRole)

        result = msg.exec_()

        if result == 0:
            nuevaVentana = RegistroUsuario.RegistroUsuario()
            self.children.append(nuevaVentana)
            event.accept()
        elif result == 1:
            event.ignore()




