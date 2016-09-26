
#-*- coding:utf-8 -*-

import sys
from PyQt4 import QtGui, QtCore


class CuestionarioPuntuacion(QtGui.QWidget):

    def __init__(self, name=None, archivo=None):
        super(CuestionarioPuntuacion, self).__init__()
        self.children = []
        self.datos = name
        self.archivo = archivo
        self.initUI()

    def definirMedida(self):
        self.tamCombo = 40
        self.respuesta = []

    def cargarArreglo(self):
        self.pregunta = [u"1. ¿El video estresor logró su objetivo?:", 
                         u"2. ¿El juego te estresó?:", 
                         u"3. ¿El test matemático logró estresarte?:", 
                         u"4. ¿El video relajante logró su cometido?:"]
        
        self.mejorEstimulo = u"5. ¿Cuál fue el mejor estímulo?:"

        self.resp = ['SI', 'NO']
        self.opcionEstimulo = ['Video estresor', 'Juego', u'Test matemático', 'Video relajante']

    def initUI(self):
        # Medidas de los combos y margen
        self.definirMedida()

        # Contenido de los combos
        self.cargarArreglo()

        # Instrucciones
        instr = u" Marca SI cuando el estímulo logro su cometido, de lo contrario marca NO" + "\n"

        labelInstruccion = QtGui.QLabel(instr)

        #Container Widget
        self.widget = QtGui.QWidget()
        # Layout of Container Widget
        layout = QtGui.QVBoxLayout(self)

        # Preguntas del cuestionario
        for pregunta in self.pregunta:

            labelPregunta = QtGui.QLabel(pregunta)

            comboRespuesta = QtGui.QComboBox()
            comboRespuesta.addItems(self.resp)
            comboRespuesta.setMaximumWidth(self.tamCombo)

            self.respuesta.append(comboRespuesta)

            hbox = QtGui.QHBoxLayout()
            hbox.addWidget(labelPregunta)
            hbox.addWidget(comboRespuesta)
            
            layout.addLayout(hbox)
        
        # Para seleccionar el mejor estimulo
        labelMejorEstimulo = QtGui.QLabel(self.mejorEstimulo)
        comboMejorEstimulo = QtGui.QComboBox()
        comboMejorEstimulo.addItems(self.opcionEstimulo)
        comboMejorEstimulo.setMaximumWidth(100)
        self.respuestaMejorEstimulo = []
        self.respuestaMejorEstimulo.append(comboMejorEstimulo)
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(labelMejorEstimulo)
        hbox.addWidget(comboMejorEstimulo)
        layout.addLayout(hbox)
        
        self.widget.setLayout(layout)
        # Scroll Area Properties
        scroll = QtGui.QScrollArea()
        scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.widget)

        btnWidget = QtGui.QWidget()
        layoutBtn = QtGui.QVBoxLayout(self)
        btnEnviar = QtGui.QPushButton('Enviar', self)
        btnEnviar.clicked.connect(self.ingresarRespuestas)
        btnEnviar.setMinimumSize(130, 35)
        hBtnBox = QtGui.QHBoxLayout()
        hBtnBox.addStretch(1)
        hBtnBox.addWidget(btnEnviar)
        layoutBtn.addLayout(hBtnBox)
        btnWidget.setLayout(layoutBtn)

        # Scroll Area Layer add
        vLayout = QtGui.QVBoxLayout(self)
        vLayout.addWidget(labelInstruccion)
        vLayout.addWidget(scroll)
        vLayout.addWidget(btnWidget)
        self.setLayout(vLayout)

        # Creando la ventana
        self.setFixedSize(380, 400)
        self.setWindowTitle(u'Cuestionario Puntuación')
        self.setWindowIcon(QtGui.QIcon('Icon/icon.jpg'))
        self.show()

    def ingresarRespuestas(self):

        msg = QtGui.QMessageBox()
        msg.setWindowIcon(QtGui.QIcon('Icon/icon.jpg'))
        msg.setWindowTitle('Guardar Cuestionario')
        msg.setText(u'¿Has terminado?')
        msg.addButton(QtGui.QPushButton('Aceptar'), QtGui.QMessageBox.YesRole)
        msg.addButton(QtGui.QPushButton('Cancelar'), QtGui.QMessageBox.NoRole)

        result = msg.exec_()

        if result == 0:
            datos = ""
            for respuesta in range(0, len(self.respuesta)):
                datos += str((self.respuesta[respuesta]).currentText()) + "\n"

            datos += str((self.respuestaMejorEstimulo[0]).currentText()) 

            file = open(self.archivo + ".txt", 'w')
            file.write(datos)
            file.close()
            self.close()

    def keyPressEvent(self, event):
    	if event.key() == 16777220:
    		self.ingresarRespuestas()

