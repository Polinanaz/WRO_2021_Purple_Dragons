import cv2
import tensorflow as tf
import matplotlib.pyplot as plt
import cv2
import numpy as np
import os
import time
import sys
from PIL import Image
import bibl 

# def rect(img):
#     r=True
#     x=0
#     y=0
#     while r and((y<img.shape[0])or(x<img.shape[1])):
#         if x<img.shape[1]:
#             x+=1
#         else:
#             x=0
#             y+=1
#         print(img[y][x][0])
#         if (img[y][x][0]==0) and ((img[y][x][1]==255) and ((img[y][x][2]==0))):
#             r=False
#             fc=[x,y]
    
#     r=True
#     x=img.shape[1]-1
#     y=img.shape[0]-1
#     while r and((y>0)or(x>0)):
#         if x>1:
#             x-=1
#         else:
#             x=img.shape[1]
#             y-=1
#         if (img[y][x][0]==0) and ((img[y][x][1]==255) and ((img[y][x][2]==0)))and (y!=-1)and (x!=-1):
#             r=False
#             sc=[x,y]
#     return fc,sc



frame = cv2.VideoCapture(0)

while True:
        status, image = frame.read()
        cv2.cvtColor(image, getattr(cv2,'COLOR_BGR2' + 'RGB'))
        x=image.shape[1]
        y=image.shape[0]
        # s=x//20//2
        # cv2.line(image, (x//2-s, 0), (x//2-s, y), (0, 0, 255), 5)
        # cv2.line(image, (x//2+s, 0), (x//2+s, y), (0, 0, 255), 5)
        
        # cv2.line(image, (x//2-3*s, 0), (x//2-3*s, y), (0, 0, 255), 5)
        # cv2.line(image, (x//2+3*s, 0), (x//2+3*s, y), (0, 0, 255), 5)

        # a= y//3

        # cv2.line(image, (x//2-3*s, a), (x//2+3*s, a), (0, 0, 255), 5)
        # cv2.line(image, (x//2-3*s, a*2), (x//2+3*s, a*2), (0, 0, 255), 5)
        
        # x_= 1000
        # y_=670
        # cv2.line(image, (x_, 0), (x_, y), (100, 100, 255), 5)
        # cv2.line(image, (x_-10, y_), (x_+10, y_), (255, 100, 255), 5)

        data = np.array(image)
        # print(data[x_][y_])
        r1, g1, b1 = 242, 242, 242 # Original value
        red, green, blue = data[:,:,0], data[:,:,1], data[:,:,2]
        mask = (red >= r1) & (green >= g1) & (blue >= b1)
        car = (red >= 155) & (green <=155) & (blue <= 155)
        # black= (red >= 180) & (red <= 240) & (green <=210) & (green >=150) & (blue <= 210) & (blue >= 150) 

        data[:,:,:3][car] = [0, 255, 0]
        image = data

        data = np.array(image)
        data[:,:,:3][mask] = [0, 0, 255]
        image = data

        # data = np.array(image)
        # data[:,:,:3][black] = [255, 0, 0]
        # image = data
        # a=[rect(image)]
        # cv2.rectangle(image, (a[0][0],a[0][1]), (a[1][2],a[][3]), (0, 255, 255), 10)
        cv2.imshow("Autopilot", image)
        k = cv2.waitKey(30)
        if k == 27:
            break

frame.release()
cv2.destroyAllWindows()