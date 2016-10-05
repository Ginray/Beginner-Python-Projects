#-*- coding: utf-8 -*-
import cv2
import numpy as np
from matplotlib import pyplot as plt
img_rgb = cv2. imread( 'cat.jpg' )
img_gray = cv2. cvtColor(img_rgb, cv2. COLOR_BGR2GRAY)
template = cv2. imread( 'cat.jpg' , 0)
'''
[::-1]是把原有的字符串倒过来 详见 ‘切片’
'''
w, h = template. shape[:: - 1]
res = cv2. matchTemplate(img_gray,template,cv2. TM_CCOEFF_NORMED)
threshold = 0.8
#umpy.where(condition[, x, y])
#Return elements, either from x or y, depending on condition.
#If only condition is given, return condition.nonzero().
loc = np. where( res >= threshold)
for pt in zip( *loc[:: - 1]):
    cv2. rectangle(img_rgb, pt, (pt[ 0] + w, pt[ 1] + h), ( 0, 0, 255), 2)
cv2.imshow('res',img_rgb)
cv2.waitKey(0)