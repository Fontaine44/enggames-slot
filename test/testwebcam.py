import cv2
from pyzbar.pyzbar import decode, ZBarSymbol

# cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
# print("init")

# while True:
#     # Capture frame-by-frame 
#     ret, frame = cap.read()

#     # # Our operations on the frame come here 
#     # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     barcode = decode(frame, [ZBarSymbol.QRCODE])
#     if barcode:
#         print(barcode[0].data)
#         print(barcode[0].type)
#         break



# # reading the input using the camera 
# result, image = cam.read() 
  
# if result:  
  
#     # saving image in local storage 
#     cv2.imwrite("test.png", image)








# cam = cv2.VideoCapture(0)
# # cam.set(28, 25) 
# # result, image = cam.read()
# # cv2.imwrite("bar.png", image)
# # print("reading")

# while True:
#     _, img = cam.read()
#     barcode = decode(img, [ZBarSymbol.CODE39])
#     if barcode:
#         a = barcode[0].data
#         break

# print(a)




cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
i = 0
detector = cv2.QRCodeDetector()

while(True): 
    # Capture frame-by-frame 
    ret, frame = cap.read()

    # Our operations on the frame come here 
    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # retval, frame = cv2.threshold(frame, 140, 255, cv2.THRESH_BINARY)

    barcode = decode(frame)
    if barcode:
        print(i)
        i+=1
        print(barcode[0].data)
        print(barcode[0].type)

    data, one, _ = detector.detectAndDecode(frame)
    if data:
        print(data)

    # Display the resulting frame 
    cv2.imshow('frame', frame) 
    if cv2.waitKey(1) & 0xFF == ord('q'): 
      break 

# When everything done, release the capture 
cap.release() 
cv2.destroyAllWindows() 