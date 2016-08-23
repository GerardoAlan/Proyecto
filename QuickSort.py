
# -*- coding: utf-8 -*-

class QuickSort():
	
	def __init__(self,arreglo=None):
		self.iniciarQS(arreglo)
		
	def partirArreglo(self, arreglo,p,q):
		x = arreglo[p]
		i = p
		for w in xrange(i+1,q):
			if arreglo[w] <= x:
				i = i + 1
				cambiaW = arreglo[i]
				arreglo[i] = arreglo[w]
				arreglo[w] = cambiaW
		cambiaP = arreglo[i]
		arreglo[i] = arreglo[p]
		arreglo[p] = cambiaP
		return i
	
	def qsr(self, arreglo,p,q):
		if p < q:
			r = self.partirArreglo(arreglo,p,q)
			self.qsr(arreglo,p,r)
			self.qsr(arreglo,r+1,q)
	
	def iniciarQS(self, arreglo):
		self.qsr(arreglo,0,len(arreglo))

'''
arreglo = [[-1,2],[-55,4],[0,3],[-1.223,23434],[34343,4],[23,3]]
print "Antes del ordenamiento: ",arreglo
QS = QuickSort(arreglo=arreglo)
print "Despues del ordenamiento: ",arreglo
'''
		