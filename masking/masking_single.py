# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import cv2
import numpy as np

# parameters
file_to_mask = 'input.jpg'
mask_image = 'mask.jpg'
masked_file = 'output.jpg'

# read image
image = cv2.imread(file_to_mask)

# mask it - read mask normally, but divide by 255.0, so range is 0 to 1 as float
mask = cv2.imread(mask_image) / 255.0

# mask by multiplication, clip to range 0 to 255 and make integer
result = (image * mask).clip(0, 255).astype(np.uint8)

#view input, mask, output
cv2.imshow('image', image)
cv2.imshow('mask', mask)
cv2.imshow('masked image', result)
cv2.waitKey(0)
cv2.destroyAllWindows()

# save results
cv2.imwrite(masked_file, result)




