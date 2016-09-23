
#-*- coding:utf-8 -*-

import threading
import time
import os
import sys
from PyQt4 import QtGui, QtCore
from PyQt4.phonon import Phonon
import scipy as sp
import matplotlib.pyplot as plt
# import ThinkGearProtocol
# import logging
# import logging.handlers
import numpy as np
import GestorArchivo



class ReproductorMultimedia(QtGui.QWidget):

    def __init__(self, name=None, archivo=None, rutaVideo=None, carpeta=None, carpetaDestino=None, carpetaImagen=None):
        super(ReproductorMultimedia, self).__init__()
        self.gestorArchivo = GestorArchivo.GestorArchivo()
        rutaAbs = os.path.abspath(os.path.curdir)
        self.rutaVideo = rutaAbs + rutaVideo
        self.carpeta = carpeta
        self.carpetaDestino = carpetaDestino
        self.carpetaImagen = carpetaImagen

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
            self.media.setCurrentSource(Phonon.MediaSource(self.rutaVideo))
            # Se crea el hilo y se ejecuta
            self.gestorArchivo = GestorArchivo.GestorArchivo()
            self.t = threading.Thread(target=self.gestorArchivo.guardarDatos, args=(self.nombreArchivo, self.datos, ))
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
            self.gestorArchivo.convertirArchivo(self.carpeta, self.carpetaDestino, self.nombreArchivo+".txt")
            # Crear la grafica con el archivo ya formateado
            self.gestorArchivo.crearGrafica(self.carpetaDestino, self.carpetaImagen, self.nombreArchivo+".txt")

            self.close()
            
            if newstate == Phonon.ErrorState:
                source = self.media.currentSource().fileName()
                print('ERROR: could not play:', source.toLocal8Bit().data())
                print('  %s' % self.media.errorString().toLocal8Bit().data())


