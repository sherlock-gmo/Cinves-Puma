import numpy as np
import cv2

i = 0
cap = cv2.VideoCapture(0)
if not cap.isOpened():
	print("No se puede abrir la camara")
	exit()
while True:
	ret, frame = cap.read()
	# Se detiene si no recibe video
	if not ret:
		print("No se recibe video")
		break
	# Se detiene si se presiona 'q'
	if cv2.waitKey(1) == ord('q'):
		  break

	cv2.imwrite('video_onboard_'+str(i)+'.png',frame)
	i = i+1


# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
