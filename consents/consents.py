# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 14:08:22 2019

@author: HamishG
"""
import pandas as pd
from pdsql import mssql
import os

pd.options.display.max_columns = 10

#########################################
### Parameters

server = 'edwprod01'

crc_db = 'ConsentsReporting'

allo_summ_table = 'reporting.CrcAlloSiteSumm'

hydro_db = 'Hydro'

sites_table = 'ExternalSite'


catch_group = ['Waipara River']

#gwaz_group = ['Waipara']

active = ['Issued - Active', 'Issued - Inactive']

export_dir = r'C:\Users\HamishG\OneDrive - Environment Canterbury\Documents\_Projects\git\Training\Training\consents'

crc_allo_csv = 'crc_allo2.csv'

########################################
### Get data


crc_allo1 = mssql.rd_sql(server, crc_db, allo_summ_table)

crc_allo2 = crc_allo1[crc_allo1['ConsentStatus'].isin(active)]

sites1 = mssql.rd_sql(server, hydro_db, sites_table)

## Queries

sites2 = sites1[sites1['CatchmentGroupName'].isin(catch_group)] #| sites1['GwazName'].isin(gwaz_group)]

#crc_allo3 = crc_allo2[crc_allo2['ExtSiteID'].isin(sites2['ExtSiteID'])]

crc_allo3 = pd.merge(crc_allo2, sites2, on='ExtSiteID')

### Save data

file_path = os.path.join(export_dir, crc_allo_csv)
crc_allo3.to_csv(file_path, index=False)










































