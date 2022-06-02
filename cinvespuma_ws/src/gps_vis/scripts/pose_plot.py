import csv
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

path = '/home/sherlock/cinvespuma_ws/src/gps_vis/scripts/' 
#**************************************************************************************************
#**************************************************************************************************
#**************************************************************************************************
def gen_vec(file_csv):
	X = []
	Y = []
	T = []
	V = []
	with open(path+file_csv, 'r') as datafile:
		ploting = csv.reader(datafile, delimiter='	')
		for ROWS in ploting:
			T.append(float(ROWS[0]))
			X.append(float(ROWS[1]))
			Y.append(float(ROWS[2]))
			#V.append(float(ROWS[3]))
	"""
	U = []
	V = []
	for th in TH:
		U.append(np.cos(th)) #+np.pi/2.0
		V.append(np.sin(th)) #+np.pi/2.0
	"""
	return np.array(T),np.array(X),np.array(Y)
#**************************************************************************************************
#**************************************************************************************************
#**************************************************************************************************
file_gps_vis = 'prueba_pose_01.csv'
T,X,Y= gen_vec(file_gps_vis)
"""
fig = plt.figure(figsize=(4,4))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(X,Y,Z) # plot the point (2,3,4) on the figure
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
plt.show()
"""
#plt.quiver(X,Y,U,V, color = 'red', scale = 65, width=0.0015, headwidth = 2.0)
plt.plot(X,Y,marker='.')
plt.title('Pose 2D')
plt.xlabel('X')
plt.ylabel('Y')
plt.grid()
plt.show()

