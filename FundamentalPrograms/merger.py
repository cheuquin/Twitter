import numpy as np
import random
from pylab import *
from matplotlib import rc, rcParams
import matplotlib.pyplot as plt
import math
import ast
import sys


data1 = np.loadtxt("Bitcoin1/Data" + '1.csv', delimiter = ',')
data2 = np.loadtxt("Bitcoin2/Data" + '2.csv', delimiter = ',')
data3 = np.loadtxt("Bitcoin3/Data" + '3.csv', delimiter = ',')
data4 = np.loadtxt("Bitcoin4/Data" + '4.csv', delimiter = ',')

#ldat = len(data3[0])
#Tipos3 = np.loadtxt("Bitcoin3/Types3.csv", delimiter = ',')

ldat = len(data3[0])
data = [[] for x in range(ldat)]

for column in range(ldat):
#	data[column] = np.concatenate( (Types3.T[column], Types3p2.T[column]) )
	data[column] = np.concatenate( (data1.T[column], data2.T[column], data3.T[column], data4.T[column]) )

data = np.array(data).T

print len(data[0])

with open("BitcoinTodo/DataTodo.csv", "w") as f:
	np.savetxt(f,data, delimiter = ',')

sys.exit()
