import numpy as np
import cv2
import glob
import matplotlib.image as mpimg
from matplotlib import pyplot as plt
from numpy.linalg import inv

imagen0 = cv2.imread('image_02.png',1) # Origen (Imagen del suelo)
#**************************************************
#**************************************************
#**************************************************
K = np.array([[625.70905563,0.0,714.99743504],[0.0,623.30278949,397.75606526],[0.0, 0.0, 1.0]])
dist_coef = np.array([[-3.34720632e-01,1.18125580e-01,4.17257777e-04,-1.61458599e-04,-1.85794482e-02]])
h,w = imagen0.shape[:2]
f = 1.19
w = int(w*f)
h = int(h*f)
mapx,mapy = cv2.initUndistortRectifyMap(K,dist_coef,None,None,(w,h),5)
imagenK = cv2.remap(imagen0,mapx,mapy,cv2.INTER_LINEAR)
cv2.imwrite('Undist_02.png',imagenK)
#**************************************************
#**************************************************

# Se definen 4 puntos en la imagen de origen. Las unidades son px.
p1_1 = [467,61]
p1_2 = [1375,45]	
p1_3 = [1040,490]
p1_4 = [631,503]
P1 = np.concatenate(([[p1_1],[p1_2],[p1_3],[p1_4]]),axis=0)
# Se seleccionan 4 puntos en la imagen de destino, se escriben en cm y se usa como referencial 
# al vector de traslacion T. Este se varia segun convenga a la imagen de salida; 
T = [40,10]
p2_1 = np.add([0.0,0.0],T)
p2_2 = np.add([245,0.0],T)			
p2_3 = np.add([245,245],T) 
p2_4 = np.add([0.0,245],T)
P2 = np.array([p2_1,p2_2,p2_3,p2_4])
H, mask = cv2.findHomography(P1, P2, cv2.RANSAC,5.0) 
#**************************************************
#**************************************************
#**************************************************
print "****************"
print "Matriz de Homografia"
print H # Matriz de homografia
#Obtenemos la imagen con correccion de pespectiva
imagenH = cv2.warpPerspective(imagenK, H, (300,300),borderMode=cv2.BORDER_CONSTANT, borderValue=(125, 125, 125)) 		
cv2.imwrite('Homography.png',imagenH)
imagenH = cv2.cvtColor(imagenH, cv2.COLOR_BGR2RGB)	
plt.imshow(imagenH, 'gray'), plt.show()
