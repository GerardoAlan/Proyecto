#-*- coding:utf-8 -*-

from math import atan2

class MagnitudFase(object):

    def __init__(self, arreglo=None):
        self.arreglo = arreglo
        self.arregloMagnitud = []
        self.arregloFase = []
        self.iniciar()
        
    def iniciar(self):
        #print "Arreglo: " + str(self.arreglo)
        
        arregloSize = len(self.arreglo)    
        for i in range(0,arregloSize,2):
            self.real = self.arreglo[i]
            self.imaginario = self.arreglo[i+1]
            
            self.arregloMagnitud.append(pow(pow(self.real, 2) + pow(self.imaginario, 2), 0.5))
            self.arregloFase.append(atan2(self.imaginario, self.real))
            #magnitud = pow(pow(self.real, 2) + pow(self.imaginario, 2), 0.5)
            #fase = atan2(self.imaginario, self.real)
            #print "Real: " + str(self.real) + " Imaginario: " + str(self.imaginario) + " Magnitud: " + str(magnitud) + " Fase: " + str(fase)
        
    def obtenerMagnitud(self):
        return self.arregloMagnitud
    
    def obtenerFase(self):
        return self.arregloFase
    
        
x = [1,-1,2,1,3,-1,4,1,1,2]
mf = MagnitudFase(x)
print mf.obtenerMagnitud()
print mf.obtenerFase()