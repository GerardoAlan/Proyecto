#-*- coding:utf-8 -*-

import numpy as np

class TransformadaRapidaFourier():
	def __init__(self, arreglo=None):
		self.arreglo = arreglo
		self.transformada = []
		self.ejeReal = []
		self.ejeImaginario = []
		self.iniciar()

	def iniciar(self):
		self.transformada = np.fft.fft(self.arreglo)
		for elemento in self.transformada:
			self.ejeReal.append(elemento.real)
			self.ejeImaginario.append(elemento.imag)

	def obtenerTransformada(self):
		return self.transformada

	def obtenerEjeReal(self):
		return self.ejeReal

	def obtenerEjeImaginario(self):
		return self.ejeImaginario
