# -*- coding: utf-8 -*-
"""
Created on Fri Mar 12 09:52:07 2021

@author: HamishG
"""

import os
import pandas as pd
from pdsql import mssql
from allotools import AlloUsage
from datetime import datetime

pd.options.display.max_columns = 10


############################################
### Parameters

server = 'edwprod01'
database = 'hydro'
sites_table = 'ExternalSite'

catch_group = ['Hurunui River']
summ_col = 'SwazName'

crc_filter = {'use_type': ['stockwater', 'irrigation']}

datasets = ['allo', 'metered_allo', 'restr_allo', 'metered_restr_allo', 'usage']

freq = 'A-JUN'

from_date = '2012-07-01'
to_date = '2020-06-30'

py_path = os.path.realpath(os.path.dirname(__file__))

plot_dir = 'plots'
export2 = 'total_swaz_allo_usage_2019-03-25.csv'
export3 = 'total_swaz_allo_usage_pivot_2019-03-25.csv'

now1 = str(datetime.now().date())

plot_path = os.path.join(py_path, plot_dir)

if not os.path.exists(plot_path):
    os.makedirs(plot_path)

############################################
### Extract data

# sites1 = mssql.rd_sql(server, database, sites_table, ['ExtSiteID', 'SwazGroupName', summ_col], where_in={'SwazGroupName': catch_group})

site_filter = {'SwazName': ['Lower Hurunui', 'Hurunui Headwaters','Middle Hurunui']}
# site_filter = {'SwazName': ['Hurunui Headwaters']}

a1 = AlloUsage(from_date, to_date, site_filter=site_filter)

a1.allo = a1.allo.reset_index()
a1.allo = a1.allo.loc[~a1.allo.crc.isin(['CRC181083', 'CRC181084'])]
a1.allo.set_index(['crc', 'take_type', 'allo_block'], inplace=True)

combo_ts = a1.get_ts(datasets, freq, ['SwazName', 'use_type', 'date'], irr_season=True)
a1_allo = a1.allo

combo_ts.to_csv(os.path.join(py_path, export2))
a1_allo.to_csv(os.path.join(py_path, export3))

#########################################
### Plotting

### Grouped
## Lumped
a1.plot_group('A-JUN', group='SwazGroupName', export_path=plot_path, irr_season=True)

## broken up
a1.plot_group('A-JUN', group='SwazName', export_path=plot_path, irr_season=True)

### Stacked
## lumped
a1.plot_stacked('A-JUN', group='SwazGroupName', export_path=plot_path, irr_season=True)

## broken up
a1.plot_stacked('A-JUN', group='SwazName', export_path=plot_path, irr_season=True)