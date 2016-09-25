
#-*- coding:utf-8 -*-
import threading
# import sys
import os
from PyQt4 import QtGui
import ReproductorMultimedia
import CuestionarioEstres
import CuestionarioPuntuacion
# import ThinkGearProtocol
# import subprocess
# import logging
# import logging.handlers
import time
# import matplotlib.pyplot as plt
# import numpy as np
import RegistroUsuario
import GestorArchivo
from gevent.hub import sleep
import TestMatematico

class MenuUsuario(QtGui.QWidget):

    def __init__(self, name=None, archivo=None):
        super(MenuUsuario, self).__init__()
        self.gestorArchivo = GestorArchivo.GestorArchivo()
        self.btnWidth = 280
        self.btnHigh = 40
        self.widWidth = 350
        self.widHigh = 390
        self.duracion = 300
        self.children = []
        self.datos = name
        self.archivo = archivo
        # self.rutaVideoEstres = "/Video/videoEstres.wmv"
        self.rutaVideoEstres = "/Video/estres.wmv"
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
        
        self.rutaTestMatematico = "DatoEstimulo/TestMatematico/Muestra/"
        self.rutaTestMatematicoGrafica = "DatoEstimulo/TestMatematico/Grafica/"
        self.rutaTestMatematicoFormato = "DatoEstimulo/TestMatematico/Formato/"
        self.rutaTestMatematicoResultado = "Cuestionario/TestMatematico/"
        
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
        buttonCuestionarioPuntuacion = QtGui.QPushButton('Calificar Estimulos', self)
        buttonCuestionarioPuntuacion.clicked.connect(self.presentarCuestionarioPuntuacion)
        buttonCuestionarioPuntuacion.move(marginLeft, contTop)


        contTop += 52
        buttonSalir = QtGui.QPushButton(
            'Salir', self)
        buttonSalir.clicked.connect(
            self.salirMenuUsuario)
        buttonSalir.move(marginLeft+180, contTop)


        buttonContenidoMultimediaE.setMinimumSize(self.btnWidth, self.btnHigh)
        buttonJuegoEstresante.setMinimumSize(self.btnWidth, self.btnHigh)
        buttonTestMatematico.setMinimumSize(self.btnWidth, self.btnHigh)
        buttonContenidoMultimediaR.setMinimumSize(self.btnWidth, self.btnHigh)
        buttonCuestionario.setMinimumSize(self.btnWidth, self.btnHigh)
        buttonCuestionarioPuntuacion.setMinimumSize(self.btnWidth, self.btnHigh)
        buttonSalir.setMinimumSize(100, 30)

        self.setFixedSize(self.widWidth, self.widHigh)
        self.setWindowTitle('Menu de Usuario')
        self.setWindowIcon(QtGui.QIcon('Icon/icon.jpg'))
        self.show()

    def presentarContenidoMultimediaEstresor(self):
        nuevaVentana = ReproductorMultimedia.ReproductorMultimedia(
            name=self.datos, archivo=self.archivo, rutaVideo=self.rutaVideoEstres, carpeta=self.rutaEstres, carpetaDestino=self.rutaEstresFormato, carpetaImagen=self.rutaEstresGrafica,)
        self.children.append(nuevaVentana)

    def presentarContenidoMultimediaRelajante(self):
        nuevaVentana = ReproductorMultimedia.ReproductorMultimedia(
            name=self.datos, archivo=self.archivo, rutaVideo=self.rutaVideoRelajante, carpeta=self.rutaRelajacion, carpetaDestino=self.rutaRelajacionFormato, carpetaImagen=self.rutaRelajacionGrafica,)
        self.children.append(nuevaVentana)

    def grabarJuegoEstresante(self):
        actual = os.getcwd()
        self.juego = threading.Thread(target=self.ejecutarCatMario, args=())
        self.juego.start()
        sleep(1)
        os.chdir(actual)
        print os.getcwd()
        # Se crea el hilo y se ejecuta
        self.t = threading.Thread(target=self.gestorArchivo.guardarDatos, args=(self.rutaJuego, self.archivo))
        self.t.start()
            
        time.sleep(self.duracion)
        # Detengo la grabacion
        self.gestorArchivo.setCloseThread(True)
        time.sleep(1)
        # Creo el archivo limpio
        self.gestorArchivo.convertirArchivo(self.rutaJuego, self.rutaJuegoFormato, self.archivo+".txt")
        # Crear la grafica con el archivo ya formateado
        self.gestorArchivo.crearGrafica(self.rutaJuegoFormato,self.rutaJuegoGrafica, self.archivo)
        self.gestorArchivo.setCloseThread(False)

    def presentarContenidoMatematico(self):
        nuevaVentana = TestMatematico.TestMatematico(
            name=self.datos, archivo=self.rutaTestMatematicoResultado + self.archivo)
        self.children.append(nuevaVentana)
        
        # Se crea el hilo y se ejecuta
        self.test = threading.Thread(target=self.gestorArchivo.guardarDatos, args=(self.rutaTestMatematico, self.archivo))
        self.test.start()
        ##################################################################################
        #time.sleep(self.duracion)
        # Detengo la grabacion
        #self.gestorArchivo.setCloseThread(True)
        # Creo el archivo limpio
        #self.gestorArchivo.convertirArchivo(self.rutaTestMatematico, self.rutaTestMatematicoFormato, self.archivo+".txt")
        # Crear la grafica con el archivo ya formateado
        #self.gestorArchivo.crearGrafica(self.rutaTestMatematicoFormato,self.rutaTestMatematicoGrafica, self.archivo)
        #self.gestorArchivo.setCloseThread(False)
        
    def presentarCuestionarioEstres(self):
        nuevaVentana = CuestionarioEstres.CuestionarioEstres(
            name=self.datos, archivo=self.rutaCuestionarioEstres + self.archivo)
        self.children.append(nuevaVentana)
        
    def presentarCuestionarioPuntuacion(self):
        nuevaVentana = CuestionarioPuntuacion.CuestionarioPuntuacion(
            name=self.datos, archivo=self.rutaCuestionarioPuntuacion + self.archivo)
        self.children.append(nuevaVentana)

    def ejecutarCatMario(self):
        actual = os.getcwd()
        os.chdir(actual + '\\JuegoCatMario')
        os.system('"'+ actual + '\\JuegoCatMario\\Cat Mario.exe"')

    def salirMenuUsuario(self):
        self.close()
    
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




