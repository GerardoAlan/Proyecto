#-*- coding:utf-8 -*-

from math import atan2

class MagnitudFase():

    def __init__(self, arreglo=None):
        self.arreglo = arreglo
        self.arregloMagnitud = []
        self.arregloFase = []
        self.iniciar()
        
    def iniciar(self):
        
        arregloSize = len(self.arreglo)
        for i in range(0,arregloSize,2):
            self.real = float(self.arreglo[i])
            self.imaginario = float(self.arreglo[i+1])
            
            self.arregloMagnitud.append(pow(pow(self.real, 2) + pow(self.imaginario, 2), 0.5))
            self.arregloFase.append(atan2(self.imaginario, self.real))
            #magnitud = pow(pow(self.real, 2) + pow(self.imaginario, 2), 0.5)
            #fase = atan2(self.imaginario, self.real)
            #print "Real: " + str(self.real) + " Imaginario: " + str(self.imaginario) + " Magnitud: " + str(magnitud) + " Fase: " + str(fase)
        
    def obtenerMagnitud(self):
        return self.arregloMagnitud
    
    def obtenerFase(self):
        return self.arregloFase
    
    