
#-*- coding:utf-8 -*-

import sys
import MenuUsuario
from PyQt4 import QtGui


class RegistroUsuario(QtGui.QWidget):

    def __init__(self):
        super(RegistroUsuario, self).__init__()
        self.children = []
        self.iptNombre = QtGui.QLineEdit(self)
        self.iptApaterno = QtGui.QLineEdit(self)
        self.iptAmaterno = QtGui.QLineEdit(self)
        self.iptCorreoE = QtGui.QLineEdit(self)
        #self.iptSexo = QtGui.QLineEdit(self)
        #self.iptEdad = QtGui.QLineEdit(self)
        #self.iptSemestre = QtGui.QLineEdit(self)
        self.tamCombo = 80
        self.initUI()

    def initUI(self):
        tamHorizontal = 350
        tamVertical = 320
        self.setFixedSize(tamHorizontal, tamVertical)
        self.setWindowTitle('Registra Usuario')
        self.setWindowIcon(QtGui.QIcon('Icon/icon.jpg'))

        marginLeftLbl = 25
        contTopLbl = 25
        marginLeftIpt = 105
        sizeIpt = 200

        itemComboSexo = ["Masculino", "Femenino"]
        itemComboEdad = ['17','18','19','20','21','22','23','24','25','26','27','28','29','30']
        itemComboSemestre = ['1', '2', '3', '4', '5', '6', '7', '8']

        # Nombre
        lblNombre = QtGui.QLabel('Nombre:', self)
        lblNombre.move(marginLeftLbl, contTopLbl)
        self.iptNombre.setMinimumWidth(sizeIpt)
        self.iptNombre.move(marginLeftLbl + marginLeftIpt, contTopLbl)
        contTopLbl += 35

        # Apellido Paterno
        lblApaterno = QtGui.QLabel('Apellido Paterno:', self)
        lblApaterno.move(marginLeftLbl, contTopLbl)
        self.iptApaterno.setMinimumWidth(sizeIpt)
        self.iptApaterno.move(marginLeftLbl + marginLeftIpt, contTopLbl)
        contTopLbl += 35

        # Apellido Materno
        lblAmaterno = QtGui.QLabel('Apellido Materno:', self)
        lblAmaterno.move(marginLeftLbl, contTopLbl)
        self.iptAmaterno.setMinimumWidth(sizeIpt)
        self.iptAmaterno.move(marginLeftLbl + marginLeftIpt, contTopLbl)
        contTopLbl += 35

        # e-mail
        lblCorreoE = QtGui.QLabel(u'Correo electrónico:', self)
        lblCorreoE.move(marginLeftLbl, contTopLbl)
        self.iptCorreoE.setMinimumWidth(sizeIpt)
        self.iptCorreoE.move(marginLeftLbl + marginLeftIpt, contTopLbl)
        contTopLbl += 35

        # Sexo
        lblSexo = QtGui.QLabel(u'Sexo:', self)
        lblSexo.move(marginLeftLbl, contTopLbl)
        self.comboSexo = QtGui.QComboBox(self)
        self.comboSexo.addItems(itemComboSexo)
        self.comboSexo.setMinimumWidth(self.tamCombo)
        self.comboSexo.move(marginLeftLbl + marginLeftIpt + 119, contTopLbl)
        contTopLbl += 35

        # Edad
        lblEdad = QtGui.QLabel(u'Edad:', self)
        lblEdad.move(marginLeftLbl, contTopLbl)
        self.comboEdad = QtGui.QComboBox(self)
        self.comboEdad.addItems(itemComboEdad)
        self.comboEdad.setMinimumWidth(self.tamCombo)
        self.comboEdad.move(marginLeftLbl + marginLeftIpt + 119, contTopLbl)
        contTopLbl += 35

        # Semestre
        lblSemestre = QtGui.QLabel(u'Semestre:', self)
        lblSemestre.move(marginLeftLbl, contTopLbl)
        self.comboSemestre = QtGui.QComboBox(self)
        self.comboSemestre.addItems(itemComboSemestre)
        self.comboSemestre.setMinimumWidth(self.tamCombo)
        self.comboSemestre.move(marginLeftLbl + marginLeftIpt + 119, contTopLbl)
        contTopLbl += 35

        # Boton Aceptar
        btnAceptar = QtGui.QPushButton('Ingresar', self)
        btnAceptar.clicked.connect(self.ingresarUsuario)
        tamHorizontalBtn = 100
        tamVerticalBtn = 30
        btnAceptar.setMinimumSize(tamHorizontalBtn, tamVerticalBtn)
        btnAceptar.move(tamHorizontal - tamHorizontalBtn -
                        19, tamVertical - tamVerticalBtn - 18)

        self.show()

    def ingresarUsuario(self):
        nombre = str((self.iptNombre.text()).toAscii())
        aPaterno = str((self.iptApaterno.text()).toAscii())
        aMaterno = str((self.iptAmaterno.text()).toAscii())
        correoE = str((self.iptCorreoE.text()).toAscii())
        edad = str(self.comboEdad.currentText())
        sexo = str(self.comboSexo.currentText())
        semestre = str(self.comboSemestre.currentText())

        datos = nombre + " " + aPaterno + " " + aMaterno + \
            " " + correoE + " " + sexo + " " + edad + " " + semestre
        archivo = nombre + "_" + aPaterno + "_" + aMaterno
        nuevaVentana = MenuUsuario.MenuUsuario(name=datos, archivo=archivo)
        self.children.append(nuevaVentana)
        self.close()

    def keyPressEvent(self, event):
        if event.key() == 16777220:
            self.ingresarUsuario()

def main():
    app = QtGui.QApplication(sys.argv)
    main_window = RegistroUsuario()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
