# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 09:42:35 2020

@author: HamishG
"""

import pandas as pd
from pdsql import mssql
import os

pd.options.display.max_columns = 10

#########################################
### Parameters

server = 'edwprod01'

crc_db = 'Hydro'

wus_table = 'dbo.TSDataNumericDaily'

site1= ['H37/0025']
        
export_dir = r'C:\Users\HamishG\OneDrive - Environment Canterbury\Documents\_Projects\git\Training\Training\WUS_export'

crc_wus_csv = 'crc_wus_H37_0025.csv'

########################################
## Get data

crc_wus1 = mssql.rd_sql(server, crc_db, wus_table, where_in={'ExtSiteID': site1})

#crc_wus2 = crc_wus1[crc_wus1['ExtSiteID'].isin(site1)]


#######################################
### Save data

file_path = os.path.join(export_dir, crc_wus_csv)
crc_wus2.to_csv(file_path, index=False)