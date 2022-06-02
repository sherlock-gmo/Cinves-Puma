import sys
import numpy as np
import scipy.linalg
# Frec. de muestreo de la senal de control(Hz)
f = 29.7 #(for_seg_images)  #29.7#16.6/SEG #29.7/BIN
# Periodo de muestreo de la senal de control (s)
h = 1/f
# Velocidad de avance del auto (m/s)
v = 0.3 #****
# Separacion de los ejes (m)
L = 0.137
# Distancia entre las llantas traseras y la base de la homografia (m)
Lh = 0.31
# Matrices del modelo cinematico usado
A = np.matrix ([[1,v*h], [0,1]])
B = (v*h/L)*np.matrix([[Lh+v*h/2], [1]])
C = np.matrix([[1,0], [0,1]])
# Matrices de ponderacion propuestas
Q = 0.014*np.matrix([[1,0],[0,1]]) # dir. prop. a Ke
R = 20.0	# inv. prop. a Ke
print("-------------------------------------------")
print('v',v)
print('R',R)
print('Q',Q)
print("-------------------------------------------")
P = np.matrix(scipy.linalg.solve_discrete_are(A,B,Q,R))
print("-------------------------------------------")
print('Ganancias del Optimal Controller Ke Kth')
K = np.matrix(scipy.linalg.inv(B.T*P*B+R)*(B.T*P*A))
print('K',K)
print("-------------------------------------------")
