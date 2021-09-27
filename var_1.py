import cv2
import tensorflow as tf
import matplotlib.pyplot as plt
import cv2
import numpy as np
import os
import time
import sys
from PIL import Image


frame = cv2.VideoCapture(0)

while True:
        status, image = frame.read()
        x=image.shape[1]
        y=image.shape[0]
        s=x//20//2
        cv2.line(image, (x//2-s, 0), (x//2-s, y), (0, 0, 255), 5)
        cv2.line(image, (x//2+s, 0), (x//2+s, y), (0, 0, 255), 5)
        
        cv2.line(image, (x//2-3*s, 0), (x//2-3*s, y), (0, 0, 255), 5)
        cv2.line(image, (x//2+3*s, 0), (x//2+3*s, y), (0, 0, 255), 5)

        a= y//3

        cv2.line(image, (x//2-3*s, a), (x//2+3*s, a), (0, 0, 255), 5)
        cv2.line(image, (x//2-3*s, a*2), (x//2+3*s, a*2), (0, 0, 255), 5)

        data = np.array(image)   # "data" is a height x width x 4 numpy array
        red, green, blue = data.T # Temporarily unpack the bands for readability
        
        # Replace white with red... (leaves alpha values alone...)
        a=230
        white_areas = (red >= a) & (blue >= a) & (green >= a)
        img = np.zeros([y,x,3],dtype=np.uint8)
        img.fill(255)
        for i in data:
            if i[0]>=a :
                img[data.index(i)]==[0, 255,0]
        #data[..., :-1][white_areas.T] = (0, 255) # Transpose back needed

        cv2.imshow("Autopilot", img)

        k = cv2.waitKey(30)
        if k == 27:
            break

frame.release()
cv2.destroyAllWindows()