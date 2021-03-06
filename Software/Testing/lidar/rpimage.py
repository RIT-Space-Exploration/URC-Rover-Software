"""
Consume LIDAR measurement file and create an image for display.

Adafruit invests time and resources providing this open source code.
Please support Adafruit and open source hardware by purchasing
products from Adafruit!

Written by Dave Astels for Adafruit Industries
Copyright (c) 2019 Adafruit Industries
Licensed under the MIT license.

All text above must be included in any redistribution.
"""

import os
from math import cos, sin, pi, floor
#import pygame
from adafruit_rplidar import RPLidar
import numpy as np
import cv2
import time

# Set up pygame and the display
#os.putenv('SDL_FBDEV', '/dev/fb1')
#pygame.init()
#lcd = pygame.display.set_mode((320,240))
#pygame.mouse.set_visible(False)
#lcd.fill((0,0,0))
#pygame.display.update()

# Setup the RPLidar
PORT_NAME = '/dev/ttyUSB0'
lidar = RPLidar(None, PORT_NAME)

# used to scale data to fit on the screen
max_distance = 0

def set_image_at_point(image, x, y):
    if (0 < x < 240 and 0 < y < 240):
        image[x , y] = [255, 255, 255]
    else:
        print("out of image bounds x:" + str(x) + " y:" + str(y))

#pylint: disable=redefined-outer-name,global-statement
def process_data(data):
    global max_distance
    #lcd.fill((0,0,0))

    image = cv2.imread('lidar_empty.png')
    height, width, depth = image.shape

    for angle in range(360):
        distance = data[angle]
        if distance > 0:                  # ignore initially ungathered data points
            max_distance = max([min([5000, distance]), max_distance])
            radians = angle * pi / 180.0
            x = distance * cos(radians)
            y = distance * sin(radians)
            point = (160 + int(x / max_distance * 119), 120 + int(y / max_distance * 119))
            set_image_at_point(image, (160 + int(x / max_distance * 119)), (120 + int(y / max_distance * 119)))

    cv2.imwrite('lidar_full.png', image)

#lcd.set_at(point, pygame.Color(255, 255, 255))
#pygame.display.update()

scan_data = [0]*360

try:
    print(lidar.info)
    for scan in lidar.iter_scans():
        for (_, angle, distance) in scan:
            scan_data[min([359, floor(angle)])] = distance
        process_data(scan_data)
        print("waiting...")
        time.sleep(10)
except KeyboardInterrupt:
    print('Stoping.')
lidar.stop()
lidar.disconnect()

