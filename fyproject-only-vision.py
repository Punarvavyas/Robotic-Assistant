'''
FINAL YEAR PROJECT
...
'''


import time
import cv2
import numpy as np
##import bluetooth
##from bluetooth.btcommon import BluetoothError
import time
##import keyboard
##import getpass
import random

##
##class DeviceConnector:
##    TARGET_NAME = "device_name"
##    TARGET_ADDRESS = None
##    SOCKET = None
##
##    def __init__(self):
##        pass
##
##    def getConnectionInstance(self):
##        self.deviceDiscovery()
##        if(DeviceConnector.TARGET_ADDRESS is not None):
##            print('Device found!')
##            self.connect_bluetooth_addr()
##            return DeviceConnector.SOCKET
##        else:
##            print('Could not find target bluetooth device nearby')
##
##    def deviceDiscovery(self):
##        try:
##            nearby_devices = bluetooth.discover_devices(lookup_names = True, duration=5)
##            print(nearby_devices)
##            while nearby_devices.__len__() == 0 and tries < 3:
##                print('hi')
##                nearby_devices = bluetooth.discover_devices(lookup_names = True, duration=5)
##                tries += 1
##                time.sleep (200.0 / 1000.0)
##                print ('couldnt connect! trying again...')
##            for bdaddr, name in nearby_devices:
##                #print('hello')
##                if bdaddr and name == DeviceConnector.TARGET_NAME:
##                    print('great')
##                    DeviceConnector.TARGET_ADDRESS = bdaddr
##                    DeviceConnector.TARGET_NAME = name
##        except BluetoothError as e:
##            print ('bluetooth is off')
##
##    def connect_bluetooth_addr(self):
##        for i in range(1,5):
##            time.sleep(1)
##            sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
##            try:
##                sock.connect((DeviceConnector.TARGET_ADDRESS, 1))
##                sock.setblocking(False)
##                DeviceConnector.SOCKET = sock
##                return
##            except BluetoothError as e:
##                print('Could not connect to the device')
##        return None
##
##d=DeviceConnector
##d.TARGET_NAME="ROBOCON_4"
##d.deviceDiscovery(d)
##d.connect_bluetooth_addr(d)
##s=d.SOCKET
##time.sleep(1)
##


camera = cv2.VideoCapture('http://192.168.43.67:8080/video')


##for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):	
##	image = frame.array
##	roi = image[200:250, 0:639]
##	Blackline= cv2.inRange(roi, (0,0,0), (50,50,50))
##	kernel = np.ones((3,3), np.uint8)
##	Blackline = cv2.erode(Blackline, kernel, iterations=5)
##	Blackline = cv2.dilate(Blackline, kernel, iterations=9)	
##	img,contours, hierarchy = cv2.findContours(Blackline.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)	
##	if len(contours) > 0 :
##	   x,y,w,h = cv2.boundingRect(contours[0])	   
##	   cv2.line(image, (x+(w/2), 200), (x+(w/2), 250),(255,0,0),3)
##	cv2.imshow("orginal with line", image)	
##	rawCapture.truncate(0)	
##	key = cv2.waitKey(1) & 0xFF	
##	if key == ord("q"):
##		break

##while 1:
##    ret, image = camera.read()
##    roi = image[200:250, 0:639]
##    Blackline= cv2.inRange(roi, (0,0,0), (50,50,50))
##    kernel = np.ones((3,3), np.uint8)
##    Blackline = cv2.erode(Blackline, kernel, iterations=5)
##    Blackline = cv2.dilate(Blackline, kernel, iterations=9)	
##    contours, hierarchy = cv2.findContours(Blackline.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)	
##    if len(contours) > 0 :
##        x,y,w,h = cv2.boundingRect(contours[0])	   
##        cv2.line(image, (x+(w//2), 200), (x+(w//2), 250),(255,0,0),3)
##    cv2.imshow("orginal with line", image)
##    k = cv2.waitKey(30) & 0xFF
##    if k == 27:
##        break

##while 1:
##    ret,image = camera.read()
##    roi = image[120:200, 0:479]
##    Blackline = cv2.inRange(roi, (0,0,0), (60,60,60))	
##    kernel = np.ones((3,3), np.uint8)
##    Blackline = cv2.erode(Blackline, kernel, iterations=5)
##    Blackline = cv2.dilate(Blackline, kernel, iterations=9)	
##    contours_blk, hierarchy_blk = cv2.findContours(Blackline.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
##	
##    if len(contours_blk) > 0:	 
##        blackbox = cv2.minAreaRect(contours_blk[0])
##        (x_min, y_min), (w_min, h_min), ang = blackbox
##        if ang < -45 :
##            ang = 90 + ang
##        if w_min < h_min and ang > 0:	  
##            ang = (90-ang)*-1
##        if w_min > h_min and ang < 0:
##            ang = 90 + ang	  
##    setpoint = 320
##    error = int(x_min - setpoint) 
##    ang = int(ang)	 
##    box = cv2.boxPoints(blackbox)
##    box = np.int0(box)
##    cv2.drawContours(roi,[box],0,(0,0,255),3)	 
##    cv2.putText(roi,str(ang),(10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
##    cv2.putText(roi,str(error),(10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
##    cv2.line(roi, (int(x_min),200 ), (int(x_min),250 ), (255,0,0),3)
####    data=ang+'b'+error+'b'
####    s.send(data)
##    cv2.imshow("orginal with line", image)	
####    rawCapture.truncate(0)	
##    key = cv2.waitKey(1) & 0xFF	
##    if key == ord("q"):
##        break
junction_area_threshold = 28000 #verify

if True:
        while(1):
                ret,image=camera.read()
                Blackline = cv2.inRange(image, (0,0,0), (75,75,75))	
                kernel = np.ones((3,3), np.uint8)
                Blackline = cv2.erode(Blackline, kernel, iterations=5)
                Blackline = cv2.dilate(Blackline, kernel, iterations=9)	
                contours_blk, hierarchy_blk = cv2.findContours(Blackline.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

##                mask = np.zeros(image.shape, np.uint8)
                cv2.drawContours(image, contours_blk, -1, (0,255,0), 2)
                ind=0
                for c in contours_blk:
                        # compute the center of the contour
                        M = cv2.moments(c)
                        cX = int(M["m10"] / M["m00"])
                        cY = int(M["m01"] / M["m00"])
                 
                        # draw the contour and center of the shape on the image
                        cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
                        cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1)
                        ind+=1
                        cv2.putText(image, "can" + str(cv2.contourArea(c)), (cX - 20, cY - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

	
                contours_blk_len = len(contours_blk)
                if contours_blk_len > 0 :
                 if contours_blk_len == 1:
                  blackbox = cv2.minAreaRect(contours_blk[0])
                 else:
                   canditates=[]
                   off_bottom = 0	   
                   for con_num in range(contours_blk_len):		
                        blackbox = cv2.minAreaRect(contours_blk[con_num])
                        (x_min, y_min), (w_min, h_min), ang = blackbox		
                        box = cv2.boxPoints(blackbox)
                        (x_box,y_box) = box[0]
                        if y_box > 358 :		 
                         off_bottom += 1
                        canditates.append((y_box,con_num,x_min,y_min))		
                   canditates = sorted(canditates)
                   if off_bottom > 1:	    
                        canditates_off_bottom=[]
                        for con_num in range ((contours_blk_len - off_bottom), contours_blk_len):
                           (y_highest,con_highest,x_min, y_min) = canditates[con_num]		
                           total_distance = (abs(x_min - x_last)**2 + abs(y_min - y_last)**2)**0.5
                           canditates_off_bottom.append((total_distance,con_highest))
                        canditates_off_bottom = sorted(canditates_off_bottom)         
                        (total_distance,con_highest) = canditates_off_bottom[0]         
                        blackbox = cv2.minAreaRect(contours_blk[con_highest])
                        ###
                        if cv2.contourArea(contours_blk[con_highest]) > junction_area_threshold:
                                 cv2.putText(image,"junction" ,(10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                   else:		
                        (y_highest,con_highest,x_min, y_min) = canditates[contours_blk_len-1]		
                        blackbox = cv2.minAreaRect(contours_blk[con_highest])
                         #My Code---
                        if cv2.contourArea(contours_blk[con_highest]) > junction_area_threshold:
                                cv2.putText(image,"junction" ,(10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                         

                #My Code---
##                 if cv2.contourArea(contours_blk[con_highest]) > junction_area_threshold:
##                         cv2.putText(image,"junction" ,(10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                 (x_min, y_min), (w_min, h_min), ang = blackbox
                 x_last = x_min
                 y_last = y_min
                 if ang < -45 :
                  ang = 90 + ang
                 if w_min < h_min and ang > 0:	  
                  ang = (90-ang)*-1
                 if w_min > h_min and ang < 0:
                  ang = 90 + ang	  
                 setpoint = 240
                 error = int(x_min - setpoint) 
                 ang = int(ang)	 
                 box = cv2.boxPoints(blackbox)
                 box = np.int0(box)
                 cv2.drawContours(image,[box],0,(0,0,255),3)	 
                 cv2.putText(image,str(ang),(10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                 cv2.putText(image,str(error),(10, 320), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                 cv2.line(image, (int(x_min),200 ), (int(x_min),250 ), (255,0,0),3)
                 
                        
                cv2.imshow("orginal with line", image)	
                key = cv2.waitKey(1) & 0xFF	
                if key == ord("q"):
                        cv2.destroyAllWindows()
                        break


	

