import cv2
import math
import numpy as np
from PIL import Image
import pytesseract

# resize image to x ,y shape
def resize(img , x , y):
    re = cv2.resize(img, (x, y), interpolation=cv2.INTER_AREA)
    return re

# filters for contours
def pro(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hue, saturation, value = cv2.split(hsv)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    topHat = cv2.morphologyEx(value, cv2.MORPH_TOPHAT, kernel)
    blackHat = cv2.morphologyEx(value, cv2.MORPH_BLACKHAT, kernel)
    add = cv2.add(value, topHat)
    subtract = cv2.subtract(add, blackHat)
    blur = cv2.GaussianBlur(subtract, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 19, 9)
    return thresh

# filters for contours
def pro1(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 3))
    dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)
    return dilation

# Crop left part
def cropLeft(img):
    height = img.shape[0]
    width = img.shape[1]

    crop_img = img[0:height, 0:int(width / 3)]
    return crop_img

def crop(img , pointTop, pointDown):
    x = 0
    y = 0
    cropi = img[pointDown+4:800 , 0:800]
    cv2.rectangle(img , (0 , pointTop-6) , (800,pointDown+4) , (0,0,255),2)
    # cv2.imshow("crop",cropi)
    # cp = img[pointDown - 6: pointTop + 4, 0:800]
    # cv2.imshow("cp",cp)
    # cv2.imshow("",img)
    # cv2.waitKey(0)

def dpi(image , x , y):
    img = Image.open(image)
    img.save(image, dpi=(x, y))

def Ifthere(x,list):
    for i in list:
        if math.fabs(i[1] - x)<=15:
            return True

x = 0
y = 0
def row(image , list ):
    x = list[0][0]
    y = list[0][1]
    for i in list:
        crop = image[x:i[0] , y:i[1]]
        x = i[0]
        y = i[1]
        # cv2.imshow("",crop)
        # cv2.waitKey(0)

def Avg(x1, x2):
    sum = x1 + x2
    avg = sum / 2
    return avg

def RowThere(l, y):
        for i in l:
            if math.fabs(i - y) <= 3:
                return True


def CleanRows(l,x):
    first = l[0]
    q4 = x/4
    x = x - q4
    for i in l[1:]:
        if math.fabs(first - i) >= 70 and i >x:
            index = l.index(i)
            l.pop(index)

        first = i
