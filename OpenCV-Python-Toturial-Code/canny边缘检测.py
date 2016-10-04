# -*- coding: utf-8 -*-
import cv2
import numpy as np
from matplotlib import pyplot as plt



img=cv2. imread( 'lena.jpg' )
'''
第一个参数 输入图像
第二个参数 minVal
第三个参数 maxVal
第四个参数 设定梯度大小的方程 默认Edge _Gradient ( G ) = | Gx*Gx | + | Gy*Gy |
'''
edges = cv2. Canny(img, 100, 200)
'''
subplot(x,y,z)表示x行 y列 第z个数（从上往下 ，从左往右）
'''


plt. subplot( 1,2,1)
plt. imshow(img,cmap = 'gray' )
plt. title( 'Original Image' )


plt. subplot( 1,2,2)
plt. imshow(edges,cmap = 'gray' )
plt. title( 'Edge Image' )
plt. show()
