#!/usr/bin/env python
import rospy
import time
import cv2
import numpy as np

cap = cv2.VideoCapture(1)
cap.set(3,1280)	# Resolution y
cap.set(4,720)	# Resolution x
cap.set(cv2.CAP_PROP_FPS,30)	# FPS

H = np.array([[ 2.34695419e-01, -1.32684008e-01, -6.51538676e+01], [ 3.44425305e-03,  2.11796937e-01, -5.43928720e+00], [-4.85568704e-05, -1.12204468e-03,  1.00000000e+00]])
K = np.array([[625.70905563,0.0,714.99743504],[0.0,623.30278949,397.75606526],[0.0,0.0,1.0]])
dist_coef = np.array([[-3.34720632e-01,1.18125580e-01,4.17257777e-04,-1.61458599e-04,-1.85794482e-02]])
lower = np.array([40,100,100])
upper = np.array([65,255,255])
path = '/home/sherlock/cinvespuma_ws/src/gps_vis/scripts/'

#**********************************************************************************
#**********************************************************************************
#**********************************************************************************
def video_cap():
	# Procesamiento de la imagen
	_,imagen0 = cap.read()	
	h,w = imagen0.shape[:2]
	f = 1.19
	w = int(w*f)
	h = int(h*f)
	mapx,mapy = cv2.initUndistortRectifyMap(K,dist_coef,None,None,(w,h),5)
	imagenF = cv2.remap(imagen0,mapx,mapy,cv2.INTER_LINEAR)
	imagenF = cv2.warpPerspective(imagenF, H, (300,300),borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0)) 
	imagenF = cv2.inRange(cv2.cvtColor(imagenF,cv2.COLOR_BGR2HSV),lower,upper)
	imagenF = cv2.medianBlur(imagenF,3)
	
	# Calculo de la posicion
	M = cv2.moments(imagenF)
	#print(M["m00"])
	if (M["m00"]>=17000):
		cX = int(M["m10"] / M["m00"])
		cY = int(M["m01"] / M["m00"])
		t = time.time()
		# Guarda los datos
		f = open(path+'prueba_pose02.csv','a+')
		f.write("%5.2f	%5.2f	%5.2f\n" %(t, cX, cY))
		f.close()
	

 	#Visualizacion
	cv2.imshow('homografia',imagenF)	
	cv2.moveWindow("homografia", 400,20)
	cv2.waitKey(1)

#**********************************************************************************
#**********************************************************************************
#**********************************************************************************
if __name__ == '__main__':
    try:
			print "*** Nodo inicializado, GPS_vis ***"
			rospy.init_node('gps_vis', anonymous=True)	
			while not rospy.is_shutdown():	
				video_cap()
    except rospy.ROSInterruptException:
        pass
