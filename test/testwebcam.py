import cv2
WEBCAM_HEIGHT = 600
WEBCAM_WIDTH = 800

camera_port = 1
cap = cv2.VideoCapture(camera_port, cv2.CAP_DSHOW)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, WEBCAM_WIDTH)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, WEBCAM_HEIGHT)
# if cap.isOpened():
# 	print(f"Camera detected in port {camera_port}")
# else:
# 	print(f"No camera detected in port {camera_port}, exiting")
# 	exit()

# while True:
#     # Read a frame from the webcam
#     ret, frame = cap.read()

#     # Display the frame
#     frame = cv2.resize(frame, (WEBCAM_WIDTH, WEBCAM_HEIGHT))
#     cv2.imshow('Webcam Feed', frame)

#     # Break the loop when the 'q' key is pressed
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Release the webcam and close the window
# cap.release()
# cv2.destroyAllWindows()



i = 0
detector = cv2.QRCodeDetector()

while(True): 
	# Capture frame-by-frame 
	ret, frame = cap.read()

	# Gray scale operation
	# frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	data, one, _ = detector.detectAndDecode(frame)
	if data:
		print(i)
		i+=1
		print(data)

	# Display the resulting frame 
	cv2.imshow('frame', frame) 
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break 



# When everything done, release the capture 
cap.release() 
cv2.destroyAllWindows() 