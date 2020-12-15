# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 13:46:28 2020

@author: HamishG
"""

import os
import glob
import pandas as pd
import numpy as np
import shutil

pd.options.display.max_columns = 100

# Root dir where raw imagery are saved
rawdir = r'C:\Temp\Hurunui Hapua photo archive\Hurunui2'

# Desintation directory where imagery subset will be copied to
resultdir = r'C:\TEMP\Hurunui Hapua photo archive\Output\Hurunui2'

# Get all files in the raw directory
all_files = glob.glob(os.path.join(rawdir, '*.jpg'))
totalFiles = len(all_files)

# Create new list to store file names
file_list = []

# Loop over each file and put it in an organised DataFrame structure splitting file name

for f in all_files:
    fname = os.path.basename(f)
    f_split = fname.split('_')
    h = f_split[2].split('.')[0]
    f_split[1] = f_split[1]+' '+ h
    
    file_list.append(f_split)
  
file_list2 = pd.DataFrame(file_list)

# Format DataFrame
file_list2['DateTime'] = pd.to_datetime(file_list2[1], format='%y-%m-%d %H-%M-%S-%f')
file_list3 = file_list2.drop(1,axis=1)

# Add target date/time column - hour target in this example
file_list3['DateTime_out'] = pd.to_datetime(file_list3['DateTime'].dt.date) + pd.Timedelta(hours=12)

# Image date/time difference from target date/time column
file_list3['diff'] = np.abs((file_list3['DateTime_out'] - file_list3['DateTime']) / pd.Timedelta(hours=1))

# Filter all image attributes, outputting closest image to target time
file_list3['Date']= file_list3['DateTime'].dt.date
test = file_list3[['Date', 'diff']].groupby('Date').min().reset_index()

# Recreate image file name in prep for image subset copy
new_test = pd.merge(test, file_list3, how='left', on=['Date', 'diff'])
new_test['fname'] = new_test[0] + '_' + pd.to_datetime(new_test['Date']).dt.strftime('%y-%m-%d') + '_' + new_test[2]

# Drop columns not required
flist = new_test.copy()
flist.drop(['Date', 'diff', 0, 2, 'DateTime_out'],axis=1,inplace=True)

# Copy the files from the raw directory to the result directory
for index, value in flist.iterrows():
    shutil.copy(os.path.join(rawdir, value['fname']), os.path.join(resultdir, value['fname']))

### Export function for validation
# export_dir = r'C:\Temp\Hurunui Hapua photo archive'
# list_csv = 'list6.csv'
# file_export = flist
# file_path = os.path.join(export_dir, list_csv)
# file_export.to_csv(file_path, index=False)
