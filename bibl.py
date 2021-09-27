import sys
import numpy as np
import cv2
import math
from PIL import Image

def getBoxes(contours_list, min_area):
    boxes = []
    for contour in contours_list:
        rect = cv2.minAreaRect(contour)  # пытаемся вписать прямоугольник
        box = cv2.boxPoints(rect)  # ищем четыре вершины у прямоугольника
        box = np.int0(box)  # округляем координаты
        area = cv2.contourArea(box)  # вычисляем площадь, занимаемую прямоугольником
        if (area > min_area):
            boxes.append(box)
    return boxes


# Вычисляем угол поворота прямоугольника
def calcAngle(box):
    # Находим центр фигуры
    center = (
        (int((box[0][0] + box[1][0] + box[2][0] + box[3][0]) / 4)),
        (int((box[0][1] + box[1][1] + box[2][1] + box[3][1]) / 4))
    )

    # Находим две стороны прямоугольника: вертикальную и горизонтальную
    edge1 = np.int0((box[1][0] - box[0][0], box[1][1] - box[0][1]))
    edge2 = np.int0((box[2][0] - box[1][0], box[2][1] - box[1][1]))

    # Определяем наиболее длинную сторону прямоугольника
    if cv2.norm(edge2) > cv2.norm(edge1):
        usedEdge = edge2
    else:
        usedEdge = edge1

    # Определем горизонтальную сторону
    reference = (1, 0)

    # Вычисляем угол между самой длинной стороной прямоугольника и горизонтом
    angle = 180.0 / math.pi * math.acos(
        (reference[0] * usedEdge[0] + reference[1] * usedEdge[1]) / (cv2.norm(reference) * cv2.norm(usedEdge)))

    return center, angle


# Рисуем на изображении прямоугольники, центр и угол наклона
def drawBoxesAngle(img, box, center, angle):
    img_out = img.copy()

    # Рисуем прямоугольник
    cv2.drawContours(img_out, [box], 0, (255, 0, 0), 2)

    # Рисуем круг в центре прямоугольника
    cv2.circle(img_out, center, 3, (10, 200, 10), 5)

    # Выводим величину угла наклона
    cv2.putText(img_out, "%d" % int(angle), (center[0] + 10, center[1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)

    return img_out

def box(image):
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(img_gray, 150, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE)
    image_copy = image.copy()
    boxes = hierarchy[0:3]#getBoxes(hierarchy[0:3], 10)
    print(hierarchy[0])
    print(contours[0])
    cv2.drawContours(image=image_copy, contours=contours, contourIdx=-1, color=(255, 0, 0), thickness=5, lineType=cv2.LINE_AA, hierarchy=hierarchy,	maxLevel = 1)
    # for box in boxes:
    #     center = calcAngle(box)
    #     print(box)
    return image_copy