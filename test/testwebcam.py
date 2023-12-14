import cv2

camera_port = 1
cap = cv2.VideoCapture(camera_port, cv2.CAP_DSHOW)
if cap.isOpened():
   print(f"Camera detected in port {camera_port}")
else:
   print(f"No camera detected in port {camera_port}, exiting")
   exit()

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