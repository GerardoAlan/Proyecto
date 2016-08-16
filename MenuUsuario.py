
#-*- coding:utf-8 -*-

import sys
import os
from PyQt4 import QtGui
import ReproductorMultimedia
import Cuestionario


class MenuUsuario(QtGui.QWidget):

    def __init__(self, name=None, archivo=None):
        super(MenuUsuario, self).__init__()
        self.btnWidth = 235
        self.btnHigh = 40
        self.widWidth = 300
        self.widHigh = 200
        self.children = []
        self.datos = name
        self.archivo = archivo
        self.rutaEstres = "/Videos/videoEstres.wmv"
        self.rutaRelajante = "/Videos/videoRelajacion.wmv"
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
        buttonContenidoMultimediaR = QtGui.QPushButton(
            'Presentar Contenido Relajante', self)
        buttonContenidoMultimediaR.clicked.connect(
            self.presentarContenidoMultimediaRelajante)
        buttonContenidoMultimediaR.move(marginLeft, contTop)

        contTop += 52
        buttonCuestionario = QtGui.QPushButton('Realizar Cuestionario', self)
        buttonCuestionario.clicked.connect(self.presentarCuestionario)
        buttonCuestionario.move(marginLeft, contTop)

        buttonContenidoMultimediaE.setMinimumSize(self.btnWidth, self.btnHigh)
        buttonContenidoMultimediaR.setMinimumSize(self.btnWidth, self.btnHigh)
        buttonCuestionario.setMinimumSize(self.btnWidth, self.btnHigh)

        self.setFixedSize(self.widWidth, self.widHigh)
        self.setWindowTitle('Menu de Usuario')
        self.setWindowIcon(QtGui.QIcon('Icon/icon.jpg'))
        self.show()

    def presentarContenidoMultimediaEstresor(self):
        nuevaVentana = ReproductorMultimedia.ReproductorMultimedia(
            name=self.datos, archivo=self.archivo + "Estres", ruta=self.rutaEstres)
        self.children.append(nuevaVentana)

    def presentarContenidoMultimediaRelajante(self):
        nuevaVentana = ReproductorMultimedia.ReproductorMultimedia(
            name=self.datos, archivo=self.archivo + "Relajante", ruta=self.rutaRelajante)
        self.children.append(nuevaVentana)

    def presentarCuestionario(self):
        nuevaVentana = Cuestionario.Cuestionario(
            name=self.datos, archivo="Cuestionarios/" + self.archivo)
        self.children.append(nuevaVentana)

    def closeEvent(self, event):
        msg = QtGui.QMessageBox()
        msg.setWindowIcon(QtGui.QIcon('Icon/icon.jpg'))
        msg.setWindowTitle('Aviso')
        msg.setText(u'¿Estás seguro de salir?')
        msg.addButton(QtGui.QPushButton('Aceptar'), QtGui.QMessageBox.YesRole)
        msg.addButton(QtGui.QPushButton('Cancelar'), QtGui.QMessageBox.NoRole)

        result = msg.exec_()

        if result == 0:
            event.accept()
        elif result == 1:
            event.ignore()


