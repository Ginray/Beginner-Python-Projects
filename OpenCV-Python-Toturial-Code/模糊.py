# -*- coding: utf-8 -*-
import cv2
import numpy as np
from matplotlib import pyplot as plt


'''
平均
'''
img=cv2. imread( 'lena.jpg' )
#（5,5） 卷积核
blur = cv2. blur(img,( 5, 5))
plt. subplot( 121),plt. imshow(img),plt. title( 'Original' )
plt. xticks([]), plt. yticks([])
plt. subplot( 122),plt. imshow(blur),plt. title( 'Blurred' )
plt. xticks([]), plt. yticks([])
plt. show()


'''
高斯模糊
'''

#（5,5） 卷积核
blur = cv2. GaussianBlur(img,(5,5),0)
plt. subplot( 121),plt. imshow(img),plt. title( 'Original' )
plt. xticks([]), plt. yticks([])
plt. subplot( 122),plt. imshow(blur),plt. title( 'Blurred' )
plt. xticks([]), plt. yticks([])
plt. show()

'''
中值模糊
'''
blur = cv2.medianBlur(img,5)
plt. subplot( 121),plt. imshow(img),plt. title( 'Original' )
plt. xticks([]), plt. yticks([])
plt. subplot( 122),plt. imshow(blur),plt. title( 'Blurred' )
plt. xticks([]), plt. yticks([])
plt. show()