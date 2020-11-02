# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import cv2
import numpy as np

# read image
img = cv2.imread('test.jpg')

#mask it - method 1:
# read mask as grayscale in range 0 to 255
# mask1 = cv2.imread('test_mask.jpg',0)
# result1 = img.copy()
# result1[mask1 == 0] = 0
# result1[mask1 != 0] = img[mask1 != 0]

# mask it - method 2:
# read mask normally, but divide by 255.0, so range is 0 to 1 as float
mask2 = cv2.imread('test_mask.jpg') / 255.0
# mask by multiplication, clip to range 0 to 255 and make integer
result2 = (img * mask2).clip(0, 255).astype(np.uint8)

cv2.imshow('image', img)
# cv2.imshow('mask1', mask1)
# cv2.imshow('masked image1', result1)
cv2.imshow('masked image2', result2)
cv2.waitKey(0)
cv2.destroyAllWindows()

# save results
# cv2.imwrite('test_masked1.jpg', result1)
cv2.imwrite('test_masked2.jpg', result2)
