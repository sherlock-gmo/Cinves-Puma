import numpy as np
import cv2
import glob

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((7*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:7].T.reshape(-1,2)
#objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)
#print(objp)
# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.
images = glob.glob('*.png')
images.sort()

for fname in images:
	img = cv2.imread(fname)
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	# Find the chess board corners
	ret, corners = cv2.findChessboardCorners(gray, (7,7),None)
	# If found, add object points, image points (after refining them)
	if ret == True:
		print(fname)
		objpoints.append(objp)
		corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
		imgpoints.append(corners2)
		# Draw and display the corners
		img = cv2.drawChessboardCorners(img, (7,7), corners2,ret)
		cv2.imshow('img',img)
		cv2.waitKey(200)
cv2.destroyAllWindows()
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)
print('camera matrix \n',mtx)
print('Coeff. Dist. \n',dist)

# undistort
img_ex = cv2.imread('26.png')
dst = cv2.undistort(img_ex, mtx, dist, None, None)
cv2.imwrite('calibresult.jpg',dst)

