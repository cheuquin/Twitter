import numpy as np
import random
from pylab import *
from matplotlib import rc, rcParams
import matplotlib.pyplot as plt
import math
import sys
import json

N = 'Todo' #Puede ser 1, 2, 3, 4, 'Todo', 'Final'

pathData = "Bitcoin" + str(N) + "/Types" + str(N) + ".csv"
pathDataTime = "Bitcoin" + str(N) + "/Data" + str(N) + ".csv"

#[u'pubkeyhash', u'pubkey', u'scripthash', u'multisig', u'nonstandard', u'nulldata']


T1, T2, T3, T4, T5, T6 = np.loadtxt(pathData, delimiter = ',', unpack = True)
#T1, T2, T3, T4, T5, T6, T7, T8 = np.loadtxt(pathData, delimiter = ',', unpack = True)
IndexSaved = np.loadtxt("Bitcoin" + str(N) + "/index" + str(N) + ".csv", delimiter = ',').astype(int)
#height, time = np.loadtxt(pathDataTime, delimiter = ',', usecols=(0, 1), unpack = True)
height, time = np.loadtxt(pathDataTime, delimiter = ',', unpack = True, usecols = (0,1))

precio = json.load(open('precio.json'))

inicio, fin = 0, 0
ti = time[0]
tf = time[len(time)-1]

for i in range( len(precio['values'])):
	if ((precio['values'][i]['x'] >= ti) and (inicio == 0) ):
		inicio = i-1
		if fin != 0: break

	if  ((precio['values'][i]['x'] >=tf) and (fin == 0)):
		fin = i
		if inicio != 0: break


fecha, valor = [], []

for i in range(fin - inicio):
	fecha.append(precio['values'][inicio + i]['x'])
	valor.append(precio['values'][inicio + i]['y'])

for i in range(len(fecha)):
	fecha[i] = (fecha[i])/(3600*24*365.25)  + 1970

fecha = fecha[1:]
valor = valor[1:]

nT1, nT2, nT3, nT4, nT5, nT6 = [], [], [], [], [], []
#nT7, nT8 = [], []

for i in range(1,len(IndexSaved) ):
	inicio = IndexSaved[i-1]
	fin = IndexSaved[i]
	nT1.append(np.log10(np.sum(T1[inicio:fin]) + 1) )
	nT2.append(np.log10(np.sum(T2[inicio:fin]) + 1) )
	nT3.append(np.log10(np.sum(T3[inicio:fin]) + 1) )
	nT4.append(np.log10(np.sum(T4[inicio:fin]) + 1) )
	nT5.append(np.log10(np.sum(T5[inicio:fin]) + 1) )
	nT6.append(np.log10(np.sum(T6[inicio:fin]) + 1) )
#	nT7.append(np.log10(np.sum(T7[inicio:fin]) + 1) )
#	nT8.append(np.log10(np.sum(T8[inicio:fin]) + 1) )

#[u'pubkeyhash', u'pubkey', u'scripthash', u'multisig', u'nonstandard', u'nulldata']


plt.plot(fecha,nT1,  '-', color = 'black', linewidth = 1, label = 'pubkeyhash') #poner label por tipo
plt.plot(fecha,nT2,  '-', color = 'red', linewidth = 1, label = 'pubkey')
plt.plot(fecha,nT3,  '-', color = 'blue', linewidth = 1, label = 'scripthash')
plt.plot(fecha,nT4,  '-', color = 'yellow', linewidth = 1, label = 'multisig')
plt.plot(fecha,nT5,  '-', color = 'orange', linewidth = 1, label = 'nonstandard')
plt.plot(fecha,nT6,  '-', color = 'green', linewidth = 1, label = 'nulldata')

#plt.plot(fecha,nT7,  '-', color = 'pink', linewidth = 1, label = 'nulldata')
#plt.plot(fecha,nT8,  '-', color = 'brown', linewidth = 1, label = 'nulldata')

plt.ticklabel_format(useOffset=False)
plt.ylabel('Number of Transactions')
plt.xlabel('Year (yr)')
plt.savefig('Figures/Figures' + str(N) + '/NTransactionPerType.png')
plt.show()





