# -*- coding: utf-8 -*-

import pandas as pd
import os, glob, shutil


# Year/Month/Camera

# Root dir where raw imagery are saved
rawdir = r'C:\TEMP\masking\output'

# Desintation directory where images will be organised in Year/Month/Camera folders
resultdir = r'C:\TEMP\masking\test'

# Get all files in the raw directory
all_files = glob.glob(os.path.join(rawdir, '*.jpg'))
totalFiles = len(all_files)

# Loop over each file and put it in an organised folder structure
i=0
for f in all_files:
    i+=1
    
    fname = os.path.basename(f)
    f_split = fname.split('_')
    
    cam = f_split[0]
    dstring = f_split[1]
    d = pd.to_datetime(dstring, format='%y-%m-%d')
    y = str(d.year)
    m = '{:02}'.format(d.month)
        
    # Check if result directory exists and if not, then create it
    outDir = os.path.join(resultdir, y, m, cam)
    if not os.path.exists(outDir):
        os.makedirs(outDir)
        
    # Move the files from the raw directory to the organised folder structure
    shutil.move(f, os.path.join(outDir, fname))
    print('Processed %s of %s images' %(i, totalFiles))
    
        

    
    