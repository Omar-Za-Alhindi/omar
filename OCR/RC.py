import cv2
from OCR import Processing as pr
import numpy as np
import re
import math

# input test image output Coordinates list of the test image
# input path output list of column
def get_Column(image):
    c = []
    img = cv2.imread(image)
    dilation = pr.pro1(img)
    _, contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    im2 = img.copy()
    prev = 0
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if h>7:

            c.append((x, y, w, h))

        prev = y

    c.sort()
    return c

# input path  output list of rows
def get_Rows(image):
    img1 = cv2.imread(image)
    img1 = pr.resize(img1, 300, 300)
    dilation = pr.pro1(img1)
    # cv2.imshow('dilation' ,dilation)
    d = dilation.copy()
    _, contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    im2 = img1.copy()
    i = 0
    first = contours[0]
    prev = 0
    prevx = 0
    rows = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if y <= 290 and x and y != 0:
            if not rows:
                rows.append(y)

            if pr.RowThere(rows, y):
                print('row there')
            else:
                rows.append(y)

        i = i + 1

    new_rows = []
    sc = cv2.imread('OCR/new_image.jpg')
    for i in rows:
        i = i*len(sc)/len(img1)
        new_rows.append(int(i))
    new_rows.sort()

    for i in range(len(new_rows)):
        pr.CleanRows(new_rows,len(sc))
    new_rows.append(new_rows[-1] + 25)

    return new_rows

# matching for first row
def Tmatching(img, t):
    List = []
    img_rgb = cv2.imread(img)
    img_rgb = cv2.resize(img_rgb, (800, 800), interpolation=cv2.INTER_AREA)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    if t == 'K':
        template = cv2.imread('OCR/Template Matching/Katrangi_Test.jpg', 0)
    elif t == 'S':
        template = cv2.imread('OCR/Template Matching/Shami_Test.jpg', 0)

    w, h = template.shape[::-1]
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.4
    loc = np.where(res >= threshold)
    print(loc[0][0])
    if not loc[0][0]:
        print('dfdfdfdf')
        return
    roi = img_rgb[loc[0][0]:loc[0][0] + h, loc[1][0] + 3:loc[1][0] + w]
    crop_img = img_rgb[loc[0][0] - 5:img_rgb.shape[1], loc[1][0]:img_rgb.shape[0]]
    List.append((loc[1][0], loc[0][0], w, h))

    cv2.imwrite('OCR/test.jpg', roi)
    cv2.imwrite('OCR/new_image.jpg', crop_img)
    new_img = get_Column('OCR/test.jpg')

    new_x = pr.Avg(new_img[0][0], new_img[1][0])
    new_x = int(new_x)

    new_crop = img_rgb[loc[0][0]:img_rgb.shape[1], loc[1][0]:new_x]

    cv2.imwrite('OCR/rows_crop.jpg', new_crop)

