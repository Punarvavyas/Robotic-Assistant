'''
FINAL YEAR PROJECT
...
'''


import time
import cv2
import numpy as np
import bluetooth
from bluetooth.btcommon import BluetoothError
import time
import keyboard
import getpass
import random
import time
import socket
import threading


map1 = '''MCA MAP
        F1  F2  F3  F4      F5
        |       |      |        |        |
        6----7----8-----9----10
'''

routes =[]
turns = []
def findroute(par,src,dest):
    for i in src.dirs:
##        print(src.nodeid,i,par)
        if i==0 or i==par:
            continue
        if i == dest.nodeid:
##            print(i)
            routes.append(i)
##            turns.append
            return 1
        r = findroute(src.nodeid,nodes[i],dest)
        if r==1:
##            print(i)
            routes.append(i)
            return 1
    return 0

class Junc:
    def __init__(self,nodeid,dirs ):
        self.dirs = dirs
        self.nodeid = nodeid

nodes = []
nodes.append(0)
nodes.append(Junc(1,[0,0,0,6]))
nodes.append(Junc(2,[0,0,0,7]))
nodes.append(Junc(3,[0,0,0,8]))
nodes.append(Junc(4,[0,0,0,9]))
nodes.append(Junc(5,[0,0,0,10]))
nodes.append(Junc(6,[7,1,0,0]))
nodes.append(Junc(7,[8,2,6,0]))
nodes.append(Junc(8,[9,3,7,0]))
nodes.append(Junc(9,[10,4,8,0]))
nodes.append(Junc(10,[0,5,9,0]))


news = [['r','n','l','u'],['n','l','u','r'],['u','r','n','l'],['l','u','r','n']]
print(map1)


s= socket.socket()

def serverthread():
    host = '0.0.0.0'
    port = 12345
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.bind((host,port))
        s.listen(1)
        pdata=''
        while True:
            try:
                c,addr = s.accept()
                databytes = c.recv(1024)
                data = str(databytes)
                print(data)
                if pdata!= data:
                    i1 = data.find('&')
                    i2 = data.find('id')
                    a=int(data[i1-1])
                    b=int(data[i2-2])
                    dire='s'
                    pdata =data
                    findroute(0,nodes[a],nodes[b])
                    routes.append(a)
                    routes.reverse()
                    print(routes)
                    for i in range(len(routes)-1):
                        ctr = 0
                        for j in nodes[routes[i]].dirs:
                            if j == routes[i+1]:
                                if dire == 'n':
                                    turns.append(news[0][ctr])
                                elif dire == 'e':
                                    turns.append(news[1][ctr])
                                elif dire == 'w':
                                    turns.append(news[2][ctr])
                                elif dire == 's':
                                    turns.append(news[3][ctr])
                                if ctr == 0:
                                    dire = 'e'
                                elif ctr == 1:
                                    dire = 'n'
                                elif ctr == 2:
                                    dire = 'w'
                                elif ctr == 3:
                                    dire = 's'
                    ##            turns.append(ctr)
                                break
                            ctr += 1
                    print(turns)
				
            finally:
                c.close()

    finally:
        s.close()
##

t1 = threading.Thread(target=serverthread,name='t1')
t1.start()

class DeviceConnector:
    TARGET_NAME = "device_name"
    TARGET_ADDRESS = None
    SOCKET = None

    def __init__(self):
        pass

    def getConnectionInstance(self):
        self.deviceDiscovery()
        if(DeviceConnector.TARGET_ADDRESS is not None):
            print('Device found!')
            self.connect_bluetooth_addr()
            return DeviceConnector.SOCKET
        else:
            print('Could not find target bluetooth device nearby')

    def deviceDiscovery(self):
        try:
            nearby_devices = bluetooth.discover_devices(lookup_names = True, duration=5)
            print(nearby_devices)
            while nearby_devices.__len__() == 0 and tries < 3:
                print('hi')
                nearby_devices = bluetooth.discover_devices(lookup_names = True, duration=5)
                tries += 1
                time.sleep (200.0 / 1000.0)
                print ('couldnt connect! trying again...')
            for bdaddr, name in nearby_devices:
                #print('hello')
                if bdaddr and name == DeviceConnector.TARGET_NAME:
                    print('great')
                    DeviceConnector.TARGET_ADDRESS = bdaddr
                    DeviceConnector.TARGET_NAME = name
        except BluetoothError as e:
            print ('bluetooth is off')

    def connect_bluetooth_addr(self):
        for i in range(1,5):
            time.sleep(1)
            sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            try:
                sock.connect((DeviceConnector.TARGET_ADDRESS, 1))
                sock.setblocking(False)
                DeviceConnector.SOCKET = sock
                return
            except BluetoothError as e:
                print('Could not connect to the device')
        return None

d=DeviceConnector
d.TARGET_NAME="ROBOCON_9"
d.deviceDiscovery(d)
d.connect_bluetooth_addr(d)
s=d.SOCKET
time.sleep(1)
kp=1
flag_jnc=0
jnc=0
jnc_cnt=0


camera = cv2.VideoCapture('http://192.168.43.123:8080/video')
junction_area_threshold = 25000 #verify
north=1
south=0
west=0
east=0
path_cnt=-1
prev_path_cnt=-1
if True:
        while(1):
                jnc=0
                ret,image=camera.read()
                Blackline = cv2.inRange(image, (0,0,0),(80,80,80))	
                kernel = np.ones((3,3), np.uint8)
                Blackline = cv2.erode(Blackline, kernel, iterations=5)
                Blackline = cv2.dilate(Blackline, kernel, iterations=9)	
                _,contours_blk, hierarchy_blk = cv2.findContours(Blackline.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

##                mask = np.zeros(image.shape, np.uint8)
                cv2.drawContours(image, contours_blk, -1, (0,255,0), 2)
                ind=0
                contours_blk_len = len(contours_blk)
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
                  if cv2.contourArea(contours_blk[0]) > junction_area_threshold:
                      cv2.putText(image,"junction" ,(10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                      if flag_jnc==0:
                          time.sleep(0.5)
                          jnc=1
                          path_cnt++;
                          flag_jnc=1
                          
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
                        
                        if cv2.contourArea(contours_blk[con_highest]) > junction_area_threshold:
                                 cv2.putText(image,"junction" ,(10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                                 if flag_jnc==0:
                                    time.sleep(0.5)
                                    jnc=1
                                    flag_jnc=1
                   else:		
                        (y_highest,con_highest,x_min, y_min) = canditates[contours_blk_len-1]		
                        blackbox = cv2.minAreaRect(contours_blk[con_highest])
                         #My Code---
                        if cv2.contourArea(contours_blk[con_highest]) > junction_area_threshold:
                                cv2.putText(image,"junction" ,(10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                                #cv2.putText(image,"12" ,(15, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                                if flag_jnc==0:
                                    time.sleep(0.5)
                                    jnc=1
                                    flag_jnc=1
                                    
                                 

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

                 motor_left=500+(kp*error)
                 motor_right=500-(kp*error)

                        
                cv2.imshow("orginal with line", image)	
                key = cv2.waitKey(1) & 0xFF	
                if key == ord("q"):
                        cv2.destroyAllWindows()
                        break
                elif key == ord("n"):
                    jnc = 2
                    flag_jnc=0
                elif key == ord("l"):
                    if north==1:
                        west=1
                        north=0
                        south=0
                        east=0
                        jnc = 6
                    elif west==1:
                        south=1
                        north=0
                        west=0
                        east=0
                        jnc=6
                    elif south==1:
                        east=1
                        north=0
                        south=0
                        west=0
                        jnc=6
                    elif east==1:
                        north=1
                        west=0
                        south=0
                        east=0
                        jnc=6
                    
                    
                elif key == ord("r"):
                    if north==1:
                        east=1
                        north=0
                        south=0
                        west=0
                        jnc = 7
                    elif west==1:
                        north=1
                        west=0
                        south=0
                        east=0
                        jnc=7
                    elif south==1:
                        west=1
                        north=0
                        south=0
                        east=0
                        jnc=7
                    elif east==1:
                        south=1
                        north=0
                        west=0
                        east=0
                        jnc=7
                    
                    jnc = 4

                elif key == ord("u"):
                    jnc = 5
                data=str(int(motor_left))+'b'+str(jnc)+'f'+str(int(motor_right))+'e'
                s.send(data)
                '''
                if jnc==4:
                    time.sleep(3)
                '''


'''
while 1:
    ret,image = camera.read()
    roi = image[120:200, 0:479]
    Blackline = cv2.inRange(roi, (0,0,0), (60,60,60))	
    kernel = np.ones((3,3), np.uint8)
    Blackline = cv2.erode(Blackline, kernel, iterations=5)
    Blackline = cv2.dilate(Blackline, kernel, iterations=9)	
    _,contours_blk, hierarchy_blk = cv2.findContours(Blackline.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	
    if len(contours_blk) > 0:	 
        blackbox = cv2.minAreaRect(contours_blk[0])
        (x_min, y_min), (w_min, h_min), ang = blackbox
        if ang < -45 :
            ang = 90 + ang
        if w_min < h_min and ang > 0:	  
            ang = (90-ang)*-1
        if w_min > h_min and ang < 0:
            ang = 90 + ang	  
    setpoint = 320
    error = int(x_min - setpoint) 
    ang = int(ang)	 
    box = cv2.boxPoints(blackbox)
    box = np.int0(box)
    cv2.drawContours(roi,[box],0,(0,0,255),3)	 
    cv2.putText(roi,str(ang),(10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(roi,str(error),(10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.line(roi, (int(x_min),200 ), (int(x_min),250 ), (255,0,0),3)
    data=str(ang)+'b'+str(error)+'e'
    s.send(data)
    cv2.imshow("orginal with line", image)	
##    rawCapture.truncate(0)	
    key = cv2.waitKey(1) & 0xFF	
    if key == ord("q"):
        break

'''
