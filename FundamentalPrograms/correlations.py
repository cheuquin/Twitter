import numpy as np
import random
from pylab import *
from matplotlib import rc, rcParams
import matplotlib.pyplot as plt
import math
import sys
import json

#san diego 1455

N = 'Todo' #Puede ser 1, 2, 3, 4, Todo, Final

pathData = "Bitcoin" + str(N) + "/Data" + str(N) + ".csv"

precio = json.load(open('precio.json'))
#ti = 1231469665

#float(precio['values'][0]['x'])
# 1504014874 = 1 de Agosto de 2017 

#if N = 'Todo' , unpack = False
height, time, ntransaction, size, valueout, tax, TasaIO = np.loadtxt(pathData, delimiter = ',', unpack = True)

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

#dif = valueout - valuein

#n stands for 'new'

L = len(time)
ntime, ntrans, ntasa, nsize, nvalue = [], [], [], [], []
ntax, nfee, ndif, nvalueout = [], [], [], []
nTasaValue, nTasaTax, nPorcion, nValueSize = [], [], [],[]
nTasaIO = []

TasaValue = valueout/ntransaction
TasaTax = tax/ntransaction
#PorcionFee = (fee)*100/(valueout + fee)
ValueSize = valueout/size

indexSaved = []
fechaValida = []
valorValido = []
z = 0

for date in fecha:
	if np.where(time >= date )[0] !=[] :
#		if ((date < 1442275200) or (date > 1456099200)):
		indexSaved.append(np.where(time >= date )[0][0] )

	else:
		indexSaved.append(L-1)
	z = z + 1

#Posiciones 1220 a 1300 son nan, indexSaved en esas posiciones tienen el mismo valor.

IS = np.array(indexSaved)

with open("Bitcoin" + str(N) + "/index" + str(N) + ".csv", "w") as f:
	np.savetxt(f, IS.astype(int), fmt='%i', delimiter = ',')

#sys.exit()

time = (time)/(3600*24*365.25) + 1970 #Se resta el tiempo en que parte bitcoin y se pasa a anos

for i in range(len(fecha)):
	fecha[i] = (fecha[i] - precio['values'][0]['x'])/(3600*24*365.25)  + 2009.021

#n stands for new

devtrans, devsize, devtax, devVOut, devTValue, devTTax, devVSize, devTasaIO = [], [], [], [], [], [], [], []

fees = [0 for x in range(len(height))]

for j in range(0,len(height)):

	if j + 1 <= 210000: r = 50
	elif j+1 <= 420000: r = 25
	else: r = 12.5 

	fees[j] = tax[j] - r

nfees = []

for i in range(1,len(indexSaved) ):
	inicio = indexSaved[i-1]
	fin = indexSaved[i]

	n = float(fin - inicio)**(0.5)

	ntime.append(time[fin])
	ntrans.append(np.mean(ntransaction[inicio:fin])), devtrans.append( np.std( ntransaction[inicio:fin] )/n )
	nsize.append(np.mean(size[inicio:fin])), devsize.append( np.std( size[inicio:fin] )/n )
	ntax.append(np.mean(tax[inicio:fin])), devtax.append( np.std( tax[inicio:fin] )/n )
	nvalueout.append(np.mean(valueout[inicio:fin])), devVOut.append( np.std( valueout[inicio:fin] )/n )
	nTasaValue.append(np.mean(TasaValue[inicio:fin])), devTValue.append( np.std( TasaValue[inicio:fin] )/n )
	nTasaTax.append(np.mean(TasaTax[inicio:fin])), devTTax.append( np.std( TasaTax[inicio:fin] )/n )
	nValueSize.append(np.mean(ValueSize[inicio:fin])), devVSize.append( np.std( ValueSize[inicio:fin] )/n )
	nTasaIO.append(np.mean(TasaIO [inicio:fin]) ), devTasaIO.append( np.std( TasaIO[inicio:fin] )/n )
	nfees.apend(np.mean(fees[inicio:fin]))


fecha = fecha[1:]
valor = valor[1:]

# Arreglar ano, bitcoin parte el 1231469665 = 8 de Enero de 2009

####### Bitcoin Price ########
plt.plot(fecha,valor,  '-', color = 'black', linewidth = 1, label='Mean NumberTransactions per 3037 blocks in time')
plt.ticklabel_format(useOffset=False)
plt.ylabel('Bitcoin Price (USD)')
plt.xlabel('Year (yr)')
plt.savefig('Figures/Figures' + str(N) + '/BitcoinPrice.png')
plt.show()

####### Transactions ###########
#plt.errorbar(ntime,ntrans, yerr = devtrans,   color = 'black', linewidth = 2, fmt='-')
plt.plot(ntime,ntrans,  '-', color = 'black', linewidth = 1)
plt.ticklabel_format(useOffset=False)
plt.ylabel('Mean Number of Transaction per block')
plt.xlabel('Year (yr)')
plt.savefig('Figures/Figures' + str(N) + '/HistoTransaction.png')
plt.show()

Naumento = []
for i in range(1, len(ntrans)):
	Naumento.append((ntrans[i] - ntrans[i-1])*100/ntrans[i-1] )

plt.plot(ntime[1:L-1],Naumento,  '-', color = 'black', linewidth = 1, label='NumberTransactions per block in time')
plt.ticklabel_format(useOffset=False)
plt.ylabel('Growth of Number of Transaction per day')
plt.xlabel('Year (yr)')
plt.savefig('Figures/Figures' + str(N) + '/HistoTransactionGROWTH.png')
plt.show()

######### Value Bitcoin
#plt.errorbar(ntime,nvalueout, yerr = devVOut,   color = 'black', linewidth = 2, fmt='-')
plt.plot(ntime, nvalueout,  '-', color = 'black', linewidth = 1, label='NumberTransactions per block in time')
plt.ticklabel_format(useOffset=False)
plt.ylabel('Mean number of Bitcoin traded per block (BTC)')
plt.xlabel('Years from the begining of Bitcoin (yr)')
plt.savefig('Figures/Figures' + str(N) + '/HistoValue.png')
plt.show()

######### Transaction-Value Correlation
#plt.errorbar(ntime,nTasaValue, yerr = devTValue,   color = 'black', linewidth = 2, fmt='-')
plt.plot(ntime, nTasaValue,  '-', color = 'black', linewidth = 1, label='NumberTransactions per block in time')
plt.ticklabel_format(useOffset=False)
plt.ylabel('Mean number of Bitcoin traded by transaction (BTC)')
plt.xlabel('Year (yr)')
plt.savefig('Figures/Figures' + str(N) + '/HistoValueTransaction.png')
plt.show()

######### Size #########
#plt.errorbar(ntime,nsize, yerr = devsize,   color = 'black', linewidth = 2, fmt='-')
plt.plot(ntime, nsize,  '-', color = 'black', linewidth = 1, label='Size per block in time')
plt.ticklabel_format(useOffset=False)
plt.ylabel('Mean Size of Blocks (MB)')
plt.xlabel('Year (yr)')
plt.savefig('Figures/Figures' + str(N) + '/HistoSize.png')
plt.show()

######### Tax #########
#plt.errorbar(ntime,ntax, yerr = devtax,   color = 'black', linewidth = 2, fmt='-')
plt.plot(ntime,ntax,  '-', color = 'black', linewidth = 1, label='Size per block in time')
plt.ticklabel_format(useOffset=False)
plt.ylabel('Mean payment per block asigned to Miners (BTC)')
plt.xlabel('Year (yr)')
plt.savefig('Figures/Figures' + str(N) + '/HistoPayMiners.png')
plt.show()

######### Tax by number of transactions ###########
#plt.errorbar(ntime,nTasaTax, yerr = devTTax,   color = 'black', linewidth = 2, fmt='-')
plt.plot(ntime, nTasaTax,  '-', color = 'black', linewidth = 1, label='Value per block in time')
plt.ticklabel_format(useOffset=False)
plt.ylabel('Mean Payment per $N_{Transactions}$ asigned to miners (BTC/transactions)')
plt.xlabel('Year (yr)')
plt.savefig('Figures/Figures' + str(N) + '/HistoPaymentTransaction.png')
plt.show()


######### Correlation amount of Bitcoin Traded and Block Size ################
#plt.errorbar(ntime,nValueSize, yerr = devVSize,   color = 'black', linewidth = 2, fmt='-')
plt.plot(ntime,nValueSize,  '-', color = 'black', linewidth = 1, label='Value per block in time')
plt.ticklabel_format(useOffset=False)
plt.ylabel('Bitcoin traded as fuction of size of the block (BTC/size)')
plt.xlabel('Year (yr)')
plt.savefig('Figures/Figures' + str(N) + '/HistoValueSize.png')
plt.show()


####### Mean Ratio n_Outputs vs n_Inputs  per day ################
plt.plot(ntime,nTasaIO,  '-', color = 'black', linewidth = 1, label='Value per block in time')
plt.ticklabel_format(useOffset=False)
plt.ylabel('Mean Ratio $\\frac{N_{Out}}{N_{In}}$')
plt.xlabel('Year (yr)')
plt.savefig('Figures/Figures' + str(N) + '/HistoIO.png')
plt.show()

####### PosibleRelation ################
plt.plot(ntime, nfees, '-', color = 'black', linewidth = 1)
plt.ticklabel_format(useOffset=False)
plt.ylabel('Mean fees payed to Miners by block')
plt.xlabel('Time (yr)')
plt.savefig('Figures/Figures' + str(N) + '/Fees.png')
plt.show()



####### Correlations #####

C1 = np.corrcoef(ntrans, valor)
C1a = np.corrcoef(np.log10(ntrans ), valor)
C2 = np.corrcoef(nvalueout, valor)
C2a = np.corrcoef(np.log10(nvalueout), valor)
C3 = np.corrcoef(nTasaValue, valor)
C3a = np.corrcoef(np.log10(nTasaValue), valor)
C4 = np.corrcoef(nsize, valor)
C4a = np.corrcoef(np.log10(nsize), valor)
C5 = np.corrcoef(ntax, valor)
C5a = np.corrcoef(np.log10(ntax), valor)
C6 = np.corrcoef(nTasaTax, valor)
C6a = np.corrcoef(np.log10(nTasaTax), valor)
C7 = np.corrcoef(nValueSize, valor)
C7a = np.corrcoef(np.log10(nValueSize), valor)
C8 = np.corrcoef(Naumento, valor[0:len(valor)-1])
C8a = np.corrcoef(np.log10(Naumento), valor[0:len(valor)-1])
C9 = np.corrcoef(nTasaIO, valor)
C9a = np.corrcoef(np.log10(nTasaIO), valor)
C10 = np.corrcoef(nfees, valor)
C10a = np.corrcoef(np.log10(nfees), valor)

print C1, C1a
print C2, C2a
print C3, C3a
print C4, C4a
print C5, C5a
print C6, C6a
print C7, C7a
print C8, C8a

f = open('Correlations/correlations' + str(N) + '.txt', 'w')
g = open('Correlations/correlationsLog' + str(N) + '.txt', 'w')


R = 'Results: \n ' + str(C1) + '\n' + str(C2) + '\n' + str(C3) + '\n' + str(C4) + '\n' + str(C5) + '\n' + str(C6) + '\n' + str(C7) + '\n' + str(C9) + '\n' + str(C10)
f.write(R)
f.close()

S = 'Results: \n ' + str(C1a) + '\n' + str(C2a) + '\n' + str(C3a) + '\n' + str(C4a) + '\n' + str(C5a) + '\n' + str(C6a) + '\n' + str(C7a) + '\n' + str(C9a) + '\n' + str(C10a)
g.write(S)
g.close()


