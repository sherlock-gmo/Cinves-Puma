#! /usr/bin/env python
import cv2
import rospy
import numpy as np
from std_msgs.msg import Int16, Int32
#from sensor_msgs.msg import Image
from sensor_msgs.msg import CompressedImage
from cv_bridge import CvBridge


bridge = CvBridge()

# V. globales de la vision
FT = 0
l = 30 # Tamano de la recta con que se modela el camino
x_ref = 100
x1 = 100
x2 = 100
x1_h = 100

# V. globales del control
u = 90
v = 0 

H = np.array([[-3.55770877e-02, -3.09583830e-01, 1.11862212e+02], [-9.45637806e-03, -9.80994015e-01, 3.27881049e+02], [-2.89072815e-05, -3.10845748e-03, 1.0]]) 
K = np.array([[367.41555751, 0.0, 317.19250783], [0.0, 367.33752184, 239.178539], [0.0, 0.0, 1.0]]) 
dist_coef = np.array([[-0.321731  ,  0.11867863, -0.00120927, -0.00076853, -0.02279705]])
# Crea la mascara del color segmentado (rosa)
lower1 = np.array([150,50,100])
upper1 = np.array([179,255,255])
lower2 = np.array([0,50,100])
upper2 = np.array([10,255,255])

#*************************************************************************************************************
#*************************************************************************************************************
#*************************************************************************************************************
#									UNDIST_K
def undist_k(imagenN):
	h,w = imagenN.shape[:2]
	f = 1.19
	h = int(h*f)
	w = int(w*f)
	mapx,mapy = cv2.initUndistortRectifyMap(K,dist_coef,None,None,(w,h),5)
	imagenK = cv2.remap(imagenN,mapx,mapy,cv2.INTER_LINEAR)
	return imagenK
#*************************************************************************************************************
#*************************************************************************************************************
#*************************************************************************************************************
#  		               TIP
def tip(imagenN):
	imagenH = cv2.warpPerspective(imagenN, H, (200,300),borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0)) 
	return imagenH
#*************************************************************************************************************
#*************************************************************************************************************
#*************************************************************************************************************
def roi_zone(x):
	assert (x>=0) and (x<=199), 'x out of limits'
	if (x>139) and (x<=199):
		y = int(round(-1.3*x+479.7))
	if (x>=89) and (x<=139):
		y = 299
	if (x>=0) and (x<89):
		y = int(round(0.9326*x+215.9986))
	return y
#*************************************************************************************************************
#*************************************************************************************************************
#*************************************************************************************************************
def vec_create(x,stride):
	j = 0
	xv = []
	for i in range(0,2*stride+1):
		if ((-1)**i==-1): j = j+1
		xv.append(x+j*(-1)**i)
	return xv
#*************************************************************************************************************
#*************************************************************************************************************
#*************************************************************************************************************
def line_detector(imagen0,x1,l,side):
	# Busca x1r
	K = True
	stride = 5
	y1 = roi_zone(x1)
	x1v = vec_create(x1,stride)
	while (K==True):
		if (y1+6>299): m = 299-y1
		else: m = stride
		for j in range(y1+m,y1-stride,-1):
			for i in x1v:
				if imagen0[j][i]==255:
					x1 = i
					y1 = j
					K = False
					break
			x1v = vec_create(x1,stride)
			if (K==False): break
		if (K==True): # Insiste en la busqueda
			x1 = x1-1*side
			y1 = roi_zone(x1)

	# Busca x2 a una altura de l cm o menos
	x2 = x1
	y2 = roi_zone(x2)
	x2v = vec_create(x2,stride)
	for j in range(y1-1,y1-l,-1):
		for i in x2v:
			if imagen0[j][i]==255:
				x2 = i
				y2 = j
				K = False
				break
		x2v = vec_create(x2,stride)			
	return x1,y1,x2,y2
#*************************************************************************************************************
#*************************************************************************************************************
#*************************************************************************************************************
#							CONTROL DEL STEERING
def callback_V(data0):
	global u, FT
	global x1, x2, x1_h

	#____________________________Procesamiento de la imagen	
	#imagen0 = bridge.imgmsg_to_cv2(data0, "bgr8") 	# Imagen cv2
	imagen0 = np.fromstring(data0.data, np.uint8)
	imagen0 = cv2.imdecode(imagen0, cv2.IMREAD_COLOR)

	imagen0 = undist_k(imagen0)			# Rectifica la distorcion radial y tangencial
	imagen0 = tip(imagen0)					# Aplica la transformacion de homografia
	imagenF1 = cv2.inRange(cv2.cvtColor(imagen0,cv2.COLOR_BGR2HSV),lower1,upper1)
	imagenF2 = cv2.inRange(cv2.cvtColor(imagen0,cv2.COLOR_BGR2HSV),lower2,upper2)
	imagenF = np.add(imagenF1,imagenF2)
	imagenF = cv2.medianBlur(imagenF,3)			
	y1 = 0
	y2 = 0
	#________________________________________Busca la linea
	if (FT<=10):
		x1 = 130 
		FT = FT+1
	else: x1 = x1_h
	side = 1 # Linea derecha
	x1,y1,x2,y2 = line_detector(imagenF,x1,l,side)
	x1_h = x1

	#________________________________________Ley de Control	
	e_y = x1-x_ref
	e_th = np.arctan2(x2-x1,l) #En radianes 
	ky = 0.25 #1.0
	kth = 0.02#5.0
	u = 90+np.arctan(ky*e_y+kth*e_th)*(180.0/np.pi) #En grados
	print('steering ',u)

 	#Visualizacion
	#namedWindow("homografia");
	imagenS = cv2.cvtColor(imagenF,cv2.COLOR_GRAY2BGR)
	imagenS = cv2.circle(imagenS,(x1,y1),3,(0, 0, 255),-1)
	imagenS = cv2.circle(imagenS,(x2,y2),3,(0, 0, 255),-1)
	#imagenS = cv2.line(imagenS, (x1,y1), (x2,y2), (0, 0, 255), 2) 
	cv2.imshow('homografia',imagenS)	
	cv2.moveWindow("homografia", 400,20)
	cv2.waitKey(1)	
	
	#Vpub.publish(v) 
	Spub.publish(u)
	
#*************************************************************************************************************
#*************************************************************************************************************
#*************************************************************************************************************
#																PRINCIPAL
if __name__ == '__main__':
	print("Nodo inicializado: optimal_driver_01.py")
	rospy.init_node('optimal_driver_01',anonymous=True)												
	Vpub = rospy.Publisher('/actuators/speed',Int32,queue_size=15)				 
	Spub = rospy.Publisher('/actuators/steering',Int16,queue_size=15)
	rospy.Subscriber("/sensors/camera/image/compressed",CompressedImage,callback_V)	 						
	rospy.spin()
#*************************************************************************************************************
#*************************************************************************************************************
#*************************************************************************************************************
