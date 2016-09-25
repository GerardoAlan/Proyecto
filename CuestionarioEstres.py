
#-*- coding:utf-8 -*-

# import sys
from PyQt4 import QtGui, QtCore


class CuestionarioEstres(QtGui.QWidget):

    def __init__(self, name=None, archivo=None):
        super(CuestionarioEstres, self).__init__()
        self.children = []
        self.datos = name
        self.archivo = archivo
        self.initUI()

    def definirMedida(self):
        self.tamCombo = 40
        self.respuesta = []

    def cargarArreglo(self):
        self.pregunta = [u"1. Preparar un examen inmediato:", u"2. Efectuar un examen oral:", u"3. Efectuar un examen escrito:", u"4. Esperar los resultados de un examen:", u"5. Suspender un examen:", u"6. Ser preguntado en clase:", u"7. Preparar un trabajo individualmente:", u"8. Preparar un trabajo en grupo:",
                         u"9. Preguntar una duda a un profesor en clase (en público):", u"10. Preguntar una duda a un profesor fuera de clase\n      (en privado):", u"11. Hablar con un profesor sobre tus problemas académicos \n      (en privado, desacuerdos sobre resultados de exámenes\n      demanda de orientación):", u"12. Participar en un seminario (discusión de temas en grupos\n      reducidos):", u"13. Efectuar actividades de prácticas:", u"14. Exponer un tema en clase:", u"15. Discutir problemas académicos con compañeros (en\n      asambleas o reuniones):", u"16. Entrar o salir del aula cuando la clase ya ha empezado:", u"17. Excesiva cantidad de materia para estudio:", u"18. Falta de tiempo para estudiar:"]

        self.respuestaCombo = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        self.ultimaSemanaCombo = ['SI', 'NO']

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

        #Container Widget
        self.widget = QtGui.QWidget()
        # Layout of Container Widget
        layout = QtGui.QVBoxLayout(self)

        # Preguntas del cuestionario
        for pregunta in self.pregunta:

            labelPregunta = QtGui.QLabel(pregunta)

            comboRespuesta = QtGui.QComboBox()
            comboRespuesta.addItems(self.respuestaCombo)
            comboRespuesta.setMaximumWidth(self.tamCombo)

            comboRespuestaUltimaSemana = QtGui.QComboBox(self)
            comboRespuestaUltimaSemana.addItems(self.ultimaSemanaCombo)
            comboRespuestaUltimaSemana.setMaximumWidth(self.tamCombo)

            self.respuesta.append(comboRespuesta)
            self.respuesta.append(comboRespuestaUltimaSemana)

            hbox = QtGui.QHBoxLayout()
            hbox.addWidget(labelPregunta)
            hbox.addWidget(comboRespuesta)
            hbox.addWidget(comboRespuestaUltimaSemana)

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
        self.setFixedSize(470, 530)
        self.setWindowTitle('Cuestionario')
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
            for respuesta in range(0, len(self.respuesta) - 1, 2):
                datos += str((self.respuesta[respuesta]).currentText()) + "," + str(
                    (self.respuesta[respuesta + 1]).currentText()) + "\n"

            file = open(self.archivo + ".txt", 'w')
            file.write(datos)
            file.close()
            self.close()

    def keyPressEvent(self, event):
    	if event.key() == 16777220:
    		self.ingresarRespuestas()

