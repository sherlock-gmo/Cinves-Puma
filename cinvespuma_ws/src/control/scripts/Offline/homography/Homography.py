import numpy as np
import cv2
import glob
import matplotlib.image as mpimg
from matplotlib import pyplot as plt
from numpy.linalg import inv

imagen0 = cv2.imread('image___1.png',1) # Origen (Imagen del suelo)
#**************************************************
#**************************************************
#**************************************************
K = np.array([[367.41555751, 0.0, 317.19250783],[0.0, 367.33752184, 239.178539],[0.0, 0.0, 1.0]])
dist_coef = np.array([[-0.321731, 0.11867863, -0.00120927, -0.00076853, -0.02279705]])
h,w = imagen0.shape[:2]
f = 1.19
w = int(w*f)
h = int(h*f)
mapx,mapy = cv2.initUndistortRectifyMap(K,dist_coef,None,None,(w,h),5)
imagenK = cv2.remap(imagen0,mapx,mapy,cv2.INTER_LINEAR)
cv2.imwrite('Undist.png',imagenK)

#**************************************************
#**************************************************
#**************************************************
# Se definen 4 puntos en la imagen de origen. Las unidades son px.
p1_1 = [275,362]
p1_2 = [466,360]	
p1_3 = [692,464]
p1_4 = [21,473]
P1 = np.concatenate(([[p1_1],[p1_2],[p1_3],[p1_4]]),axis=0)
# Se seleccionan 4 puntos en la imagen de destino, se escriben en cm y se usa como referencial 
# al vector de traslacion T. Este se varia segun convenga a la imagen de salida; 
T = [75,224]
p2_1 = np.add([0.0,0.0],T)
p2_2 = np.add([47.0,0.0],T)			
p2_3 = np.add([47.0,65.5],T) 
p2_4 = np.add([0.0,65.5],T)
P2 = np.array([p2_1,p2_2,p2_3,p2_4])
H, mask = cv2.findHomography(P1, P2, cv2.RANSAC,5.0) 
#**************************************************
#**************************************************
#**************************************************
print "****************"
print "Matriz de Homografia"
print H # Matriz de homografia
#Obtenemos la imagen con correccion de pespectiva
imagenH = cv2.warpPerspective(imagenK, H, (200,300),borderMode=cv2.BORDER_CONSTANT, borderValue=(125, 125, 125)) 		
cv2.imwrite('Homography.png',imagenH)
imagenH = cv2.cvtColor(imagenH, cv2.COLOR_BGR2RGB)	
plt.imshow(imagenH, 'gray'), plt.show()

