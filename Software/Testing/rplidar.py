import os
import math
from adafruit_rplidar import RPLidar

#setup lidar
PORT_NAME = '/dev/ttyUSB0'
lidar = RPLidar(None, PORT_NAME)

max_distance = 0;

#pylint: disable=redefined-outer-name,global-statement
def process_data(data):
    global max_distance
    #lcd.fill((0,0,0))
    for angle in range(360):
        distance = data[angle]
        if distance > 0:                  # ignore initially ungathered data points
            max_distance = max([min([5000, distance]), max_distance])
            radians = angle * math.pi / 180.0
            x = distance * math.cos(radians)
            y = distance * math.sin(radians)
            point = (160 + int(x / max_distance * 119), 120 + int(y / max_distance * 119))
            #print("point: " + str(point))
 
 
scan_data = [0]*360
 
try:
    print(lidar.info)
    for scan in lidar.iter_scans():
        for (_, angle, distance) in scan:
            scan_data[min([359, math.floor(angle)])] = distance
        process_data(scan_data)
        print("scan: " +str(scan_data))
 
except KeyboardInterrupt:
    print('Stoping.')
lidar.stop()
lidar.disconnect()
