# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import os
import cv2
import numpy as np
import glob

# input parameters

input_directory = r'C:\Users\hamishg\OneDrive - Environment Canterbury\Documents\_Projects\git\Training\masking\input'
output_directory = r'C:\Users\hamishg\OneDrive - Environment Canterbury\Documents\_Projects\git\Training\masking\output'

files_to_mask = glob.glob(input_directory + '\*.jpg')

mask_file = 'hurunui_south_mask.png'

# masking function
def MaskingFunction(input_file, masking, outDir):

    # read image
    image = cv2.imread(input_file)
          
    # mask it - read mask normally, but divide by 255.0, so range is 0 to 1 as float
    mask = cv2.imread(masking) / 255.0
    
    # mask by multiplication, clip to range 0 to 255 and make integer
    result = (image * mask).clip(0, 255).astype(np.uint8)
         
    # save results
    file_name = os.path.basename(input_file)
    output_file = os.path.join(output_directory, file_name)
      
    cv2.imwrite(output_file, result)

# run for all images in directory
for inF in files_to_mask:
    MaskingFunction(inF, mask_file, output_directory)

