
# -*- coding:utf-8 -*-
from PyQt4 import QtGui, QtCore
import threading
import time

class TestMatematico(QtGui.QWidget):

    def __init__(self, carpeta=None, rutaFormato=None, rutaGrafica=None, name=None, archivo=None):
        super(TestMatematico, self).__init__()
        self.children = []
        self.rutaTestMatematico = carpeta
        self.rutaTestMatematicoFormato = rutaFormato
        self.rutaTestMatematicoGrafica = rutaGrafica
        self.datos = name
        self.archivo = archivo
        self.initUI()

    def definirMedida(self):
        self.tamCombo = 80
        self.respuesta = []

    def cargarArreglo(self):
        self.pregunta = [u"1. Sigue la serie: 27, 19, 34, 26, 41, 33, ?", 
                         u"2. Continúa la secuencia: 16, 2, 32, 2, 64, 2, ?", 
                         u"3. Sigue la secuencia: 3, 30, 6, 30, 9, 90, ?", 
                         u"4. Sigue la secuencia: 3, 6, 9, 12, 15, 18, 21, ?", 
                         u"5. Sigue la secuencia: 6, 6, 10, 5, 14, 4, ?", 
                         u"6. ¿Qué número sigue la secuencia?: 25, 50, 100, 200, 400, ?", 
                         u"7. Sigue la secuencia: 3, 7, 21, 147, 3087, ?", 
                         u"8. Encuentra el número que sigue la secuencia: 25, 10, 15, 5, 10, ?",
                         u"9. Indica qué par de números siguen la serie: 7, 3, 6, 3, 5, 3, ?, ?", 
                         u"10. Qué número sigue la secuencia: 4, 3, 3, 2, 2, ?", 
                         u"11. Continúa la secuencia: 7, 21, 84 ,420, 2520, ?", 
                         u"12. Continúa la secuencia: 120, 240, 720, 2880, ?", 
                         u"13. Sigue la serie: 18, 36, 11, 22, 17, 34, 9, ?", 
                         u"14. Continúa la secuencia: 14, 15, 28, 30, 56, ?", 
                         u"15. Sigue la serie: 24, 34, 44, 54, 64, ?", 
                         u"16. ¿Qué número continúa la serie?: 9, 17, 8, 14, 7, 11, 6, 8, ?", 
                         u"17. Encuentra el número que sigue la secuencia: 2, 6, 12, 36, 72,\n      216, ?", 
                         u"18. Sigue la secuencia: 42, 14, 35, 21, 28, 28, ?",
                         u"19. Indica qué par de números siguen la serie: 52, 53, 55, 58, 62,\n      67, ? ,?",
                         u"20. Sigue la serie: (2-4-1), (4-12-4), (?-?-?), (8-40-40)",
                         u"21. Encuentra el número que sigue la secuencia: 18, 32, 60, 116,\n      228, ?",
                         u"22. ¿Qué número continúa la serie: 6, 3, 8, 4, 10, 5, 12, 6, 14, ?",
                         u"23. Sigue la secuencia: 3, 21, 147, 1029, ?",
                         u"24. En la siguiente serie hay un número equivocado que no \n      corresponde con la serie. Señala el número que debería\n      ir en su lugar: 5, 10, 12, 24, 26, 28, 54, 108, 110",
                         u"25. Completa la serie: 4, 8, 11, 7, 14, ?, ?, 26, 29, ?"]

        self.respuestaCombo = [[" ","48","52","24","66"],
                               [" ","128","172","254","196"],
                               [" ","120","100","12","110"],
                               [" ","24","25","27","26"],
                               [" ","18","3","13","16"],
                               [" ","600","700","800","1600"],
                               [" ","453789","354796","673459","534679"],
                               [" ","5","15","0","20"],
                               [" ","3,3", "3,4", "4,3", "1,2"],
                               [" ","4","1","3","2"],
                               [" ","8820","10080","17640","5040"],
                               [" ","5760","11520","8640","14400"],
                               [" ","15","18","27","36"],
                               [" ","60","66","58","86"],
                               [" ","74","72","70","71"],
                               [" ","10","9","12","5"],
                               [" ","432","420","288","252"],
                               [" ","14","19","21","22"],
                               [" ","72,79","71,79","73,80","72,75"],
                               [" ","(8-24-12)","(6-24-12)","(6-20-12)","(8-24-10)"],
                               [" ","452","456","624","312"],
                               [" ","16","8","6","7"],
                               [" ","6300","5200","1703","7203"],
                               [" ","6","48","52","105"],
                               [" ","10,14,24", "10,20,33", "17,13,25", "18,14,25"]]

    def initUI(self):
        # Medidas de los combos y margen
        self.definirMedida()

        # Contenido de los combos
        self.cargarArreglo()

        # Instrucciones
        instr = u"    Los siguientes  puntos describen  actividades o  situaciones que se  presentan en la vida" + "\n"
        instr += u"    académica y que  pueden ser  estresantes para  los estudiantes (es decir,  que provocan" + "\n"
        instr += u"    tensión o malestar excesivo en el individuo)." + "\n\n"
        instr += u"    En cada punto, elige la opción (de 1 a 9) que mejor indique en que medida es estresante" + "\n"
        instr += u"    para  ti. A continuación indica SI te has  encontrado o  NO en esta  situación durante las" + "\n"
        instr += u"    últimas 4 semanas."

        labelInstruccion = QtGui.QLabel(instr)

        # Container Widget
        self.widget = QtGui.QWidget()
        # Layout of Container Widget
        layout = QtGui.QVBoxLayout(self)

        # Preguntas del cuestionario
        contadorRespuesta = 0
        for pregunta in self.pregunta:

            labelPregunta = QtGui.QLabel(pregunta)

            comboRespuesta = QtGui.QComboBox()
            comboRespuesta.addItems(self.respuestaCombo[contadorRespuesta])
            print contadorRespuesta, self.respuestaCombo[contadorRespuesta]
            contadorRespuesta += 1
            comboRespuesta.setMaximumWidth(self.tamCombo)
            self.respuesta.append(comboRespuesta)
            
            hbox = QtGui.QHBoxLayout()
            hbox.addWidget(labelPregunta)
            hbox.addWidget(comboRespuesta)
            
            hboxSpace = QtGui.QHBoxLayout()
            hboxSpace.addWidget(QtGui.QLabel(" "))

            layout.addLayout(hbox)
            layout.addLayout(hboxSpace)

        self.widget.setLayout(layout)
        # Scroll Area Properties
        scroll = QtGui.QScrollArea()
        scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.widget)

        btnWidget = QtGui.QWidget()
        layoutBtn = QtGui.QVBoxLayout(self)
        #btnEnviar = QtGui.QPushButton('Enviar', self)
        #btnEnviar.clicked.connect(self.ingresarRespuestas)
        #btnEnviar.setMinimumSize(130, 35)
        hBtnBox = QtGui.QHBoxLayout()
        hBtnBox.addStretch(1)
        #hBtnBox.addWidget(btnEnviar)
        layoutBtn.addLayout(hBtnBox)
        btnWidget.setLayout(layoutBtn)

        # Scroll Area Layer add
        vLayout = QtGui.QVBoxLayout(self)
        vLayout.addWidget(labelInstruccion)
        vLayout.addWidget(scroll)
        vLayout.addWidget(btnWidget)
        self.setLayout(vLayout)

        # Creando la ventana
        self.setFixedSize(470, 530)
        self.setWindowTitle('Test Matematico')
        self.setWindowIcon(QtGui.QIcon('Icon/icon.jpg'))
        self.show()
        
    def detenerTest(self):
        datos = ""
        print len(self.respuesta)
        for respuesta in range(0, len(self.respuesta)):
            datos += str((self.respuesta[respuesta]).currentText()) + "\n"

        file = open(self.archivo + ".txt", 'w')
        file.write(datos)
        file.close()
        self.close()
