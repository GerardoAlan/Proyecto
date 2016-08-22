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
    
        
x = [2895619.49722,5512314.88691,972175.874285,992180.162218,147936.025896,127221.751186,70480.911805,43553.6303947,360158.212539,149046.031754,260626.672003,107456.546279,140477.36186,70089.9293876,134124.038473,81637.5946518,-629.167923139,-688.713026933,-81.9627287239,-403.681893567]
mf = MagnitudFase(x)
print "Arreglo de entrada: " + str(x)
print "Magnitud: " + str(mf.obtenerMagnitud())
print "Fase: " + str(mf.obtenerFase())