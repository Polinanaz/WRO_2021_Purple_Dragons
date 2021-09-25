import cv2
import tensorflow as tf
import matplotlib.pyplot as plt
import cv2
import numpy as np
import os
import time
import sys
#Подключаем режим мультипроцессорности для более быстрой работы алгоритма
cv2.setUseOptimized(True) #активируем режим оптимизации

frame = cv2.VideoCapture(1)
sss = cv2.ximgproc.segmentation.createSelectiveSearchSegmentation()

while True:
        status, image = frame.read()
    
        cv2.imshow("TV show", image)
        # Передаем алгоритму картинку
        sss.setBaseImage(image)
        # Выбираем медленный, но более точный метод (по умолчанию работает метод Fast)
        sss.switchToSelectiveSearchQuality()
        # Запускаем selective search segmentation на переданном изображении
        rects = sss.process() #результат вернётся в виде прямоугольников внутри которых предположительно находятся объекты
        numShowRects = 10 #кол-во region proposals (прямоугольников, описывающих объект)
        imOut = image.copy() #создаем копию исходной картинки

        for i, rect in enumerate(rects): #проходим по каждому прямоугольнику
            if (i < numShowRects): #пока не наберётся заданное кол-во прямоугольников
                x, y, w, h = rect      # x,y - координаты точки вершины; w, h - шаги от вершины вправо, вниз
                cv2.rectangle(imOut, (x, y), (x+w, y+h), (0, 255, 0), 1, cv2.LINE_AA) #метод нарисует на изображении прямоугольник по указанным параметрам
            else: #если кол-во прямоугольников превысит заданное
                break #то останавливаемся

        cv2.imshow("TV show", image)

        k = cv2.waitKey(30)
        if k == 27:
            break

frame.release()
cv2.destroyAllWindows()