# -*- coding: utf-8 -*-

import cv2
import numpy as np
from matplotlib import pyplot as plt


def nothing(x):
    pass


# 创建一副黑色图像
img = cv2.imread('./lena.jpg')
#缩放
img=cv2. resize(img, None,fx=2,fy=2,interpolation=cv2. INTER_CUBIC)


# 设置滑动条组件
cv2.namedWindow('image')
cv2.createTrackbar('minVal', 'image', 0, 255, nothing)
cv2.createTrackbar('maxVal', 'image', 0, 255, nothing)


while (1):

    key=cv2. waitKey(5)
    if key==27:
        break
    minVal = cv2.getTrackbarPos('minVal','image')
    maxVal = cv2.getTrackbarPos('maxVal','image')
    edges = cv2.Canny(img, minVal, maxVal)
    cv2.imshow('image', edges)

# 销毁窗口
cv2.destroyAllWindows()