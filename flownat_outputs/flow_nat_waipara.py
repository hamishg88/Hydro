# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 09:25:41 2019

@author: michaelek
"""
import os
import numpy as np
from flownat import FlowNat
import pandas as pd

pd.options.display.max_columns = 10

from_date = '1968-07-01'
to_date = '2020-06-30'
rec_data_code = 'Primary'
output_path = r'C:\Users\hamishg\OneDrive - Environment Canterbury\Documents\_Projects\git\flownat\marble_point'
input_sites1 = ['64602']

# Up to 1996-06-30, there was a max of ~9 m3/s taken from the river.
# After that it increases to over 20 m3/s until 2013, then it goes quite high.


def tsreg(ts, freq=None, interp=False):
    """
    Function to regularize a time series object (pandas).
    The first three indeces must be regular for freq=None!!!

    ts -- pandas time series dataframe.\n
    freq -- Either specify the known frequency of the data or use None and
    determine the frequency from the first three indices.\n
    interp -- Should linear interpolation be applied on all missing data?
    """

    if freq is None:
        freq = pd.infer_freq(ts.index[:3])
    ts1 = ts.resample(freq).mean()
    if interp:
        ts1 = ts1.interpolate('time')

    return ts1


def malf7d(x, w_month='JUN', max_missing=90, malf_min=0.9, intervals=[10, 20, 30, 40], return_alfs=False, num_years=False, export_path=None, export_name_malf='malf.csv', export_name_alf='alf.csv', export_name_mis='alf_missing_data.csv'):
    """
    Function to create a 7 day mean annual low flow estimate from flow time
    series.

    Parameters
    ----------
    x : DataFrame or Series
        Pandas DataFrame or Series with a daily DateTimeIndex.
    w_month : str
        The month to start the water year in three upper case letters.
    max_missing : int
        The allowed missing data in a year for the alf7d calc.
    malf_min : float
        The minimum ratio of ALF data years to total years to calculate the MALF.
    intervals : list of int
        The intervals to calculate MALF over.
    return_alf : bool
        Should the ALFs and the number of missing days per year be returned in addition to the MALF?
    export_path : str
        The base path for the export files that will be saved.

    Returns
    -------
    DataFrame(s)
        When return_alfs is False, then the output is only a dataframe of the MALFs by intervals. When return_alfs is True, then the output will include the MALFs, the annual ALFs, the number of missing days per year, the number of days (out of 20) that have data surrounding the minimum flow value for that year, and the dates of the minimum flow per year.
    """

    mon_day_dict = {'JUN': 182, 'JAN': 1, 'FEB': 32, 'MAR': 61, 'APR': 92, 'MAY': 122, 'JUL': 153, 'AUG': 214, 'SEP': 245, 'OCT': 275, 'NOV': 306, 'DEC': 336}

    def malf_fun(df, intervals):

        malfs = []
        last_yr = df[-1:].index[0]
        for i in intervals:
            first_yr = last_yr - pd.DateOffset(years=i)
            df10 = df[first_yr:]
            mis10 = np.floor(i * malf_min) <= df10.count()
            if mis10:
                malfs.extend([round(np.mean(df10), 3)])
            else:
                malfs.extend([np.nan])
        malfs.extend([round(np.mean(df), 3)])

        return malfs

    #    def day_june(df, dayofyear=182):
    #        day1 = df.dt.dayofyear
    #        over1 = day1 >= dayofyear
    #        under1 = day1 < dayofyear
    #        day2 = day1.copy()
    #        day2.loc[over1] = day1.loc[over1] - dayofyear
    #        day2.loc[under1] = 365 - dayofyear + day1.loc[under1]
    #        return(day2)

    ### Make sure the object is a data frame and regular
    df_temp = tsreg(pd.DataFrame(x))
    df = df_temp.dropna(axis=1, how='all')
    df.columns = df.columns.astype(int)

    ### Rolling mean
    df2 = df.rolling(7, center=True).mean()

    ## count the number of days with data
    df2_nans = df2.rolling(20, center=True).count()

    ### Calc and filter ALFs
    n_days_yr = df2.fillna(0).resample('A-' + w_month).count()
    day_filter = n_days_yr.iloc[:, 0] >= 275
    n_days_yr2 = n_days_yr[day_filter]
    df3_res = df2.resample('A-' + w_month)
    df4 = df3_res.min()[day_filter]
    df_count1 = df3_res.count()[day_filter]
    df_missing = n_days_yr2 - df_count1
    df4[df_missing > max_missing] = np.nan
    df_count2 = df4.count()

    ### Find the minimum in each water year
    min_date = df2.resample('A-' + w_month).agg(['idxmin'])
    min_date.columns = min_date.columns.droplevel(1)
    min_day = min_date.apply(lambda x: x.dt.dayofyear)
    mon_day = mon_day_dict[w_month]

    ## Determine if there are missing values near the min flow value
    n_days_min = min_date.copy()
    for i in df2_nans:
        index1 = min_date.loc[min_date[i].notnull(), i]
        val1 = df2_nans.loc[index1, i].resample('A-' + w_month).min()
        val1.name = i
        n_days_min.loc[:, i] = val1

    mis_min_bool = any(n_days_min < 13)

    if mis_min_bool:
        print(
        'Warning 1 - Some sites have significant amounts of missing values near the ALF! Check the DataFrame output for further info.')

    ## determine the number of min days per year within a month of the water year break point
    count_min_day = min_day.apply(lambda x: (x > (mon_day - 30)) & (x < (mon_day + 30))).sum()
    ratio_min_day = (count_min_day / df_count2).round(2)
    ratio_min_day_bool = ratio_min_day >= 0.25

    if any(ratio_min_day_bool):
        sites_prob = ratio_min_day[ratio_min_day_bool].index.tolist()
        print('Warning 2 - Site(s) ' + str(
            sites_prob) + ' have a significant amount of ALFs that fall at the end/beginning of the water year.')

    #    mean_date = min_date.apply(day_june, dayofyear=mon_day_dict[w_month]).mean()

    ## MALF calc
    malf = df4.apply(lambda x: pd.Series(malf_fun(x, intervals)), axis=0).transpose()
    malf_col_names = ["MALF7D " + str(i) + " yrs" for i in intervals]
    malf_col_names.extend(["MALF7D all yrs"])
    malf.columns = malf_col_names
    if num_years:
        malf['Avg_num_days'] = np.nan
        for i in malf.index:
            val = float(malf.ix[i, 4])
            t1 = df[i][df[i] <= val]
            t2 = round(t1.resample('A-' + w_month).count().mean(), 1)
            malf.loc[i, 'Avg_num_days'] = t2

    ## Export data and return dataframes
    if return_alfs:
        if isinstance(export_path, str):
            malf.to_csv(path.join(export_path, export_name_malf))
            df4.round(3).to_csv(path.join(export_path, export_name_alf))
            df_missing.to_csv(path.join(export_path, export_name_mis))

        return ([malf, df4.round(3), df_missing, n_days_min, min_date])
    else:
        if isinstance(export_path, str):
            malf.to_csv(path.join(export_path, export_name_malf))

        return malf


########################################
### flow nat


f1 = FlowNat(from_date, to_date, input_sites=input_sites1, output_path=output_path)

#f1 = FlowNat(from_date, to_date, input_sites=input_sites1)

#up1 = f1.upstream_takes()

nat_flow = f1.naturalisation()

for s in input_sites1:
    nat_flow1 = f1.plot(s)

#nat_flow = self.naturalisation()
flow_rec = nat_flow['Flow'].rename(columns={64602: '64602'})
malf_rec = malf7d(flow_rec)

flow_nat = nat_flow['NatFlow'].rename(columns={64602: '64602'})
malf_nat = malf7d(flow_nat)

## Output

site = '64602'

allo1 = f1.allo_wap[f1.allo_wap.ExtSiteID == site]

use1 = f1.usage_rate[f1.usage_rate.Wap.isin(allo1.Wap.unique())]

waps = f1.waps_gdf[f1.waps_gdf.Wap.isin(allo1.Wap.unique()) & (f1.waps_gdf.ExtSiteID == site)]

allo1.to_csv(os.path.join(output_path, 'above_marblepoint_allo_2020-18-12.csv'), index=False)
use1.to_csv(os.path.join(output_path, 'above_marblepoint_usage_2020-18-12.csv'), index=False)
waps.to_file(os.path.join(output_path, 'above_marblepoint_waps_2020-18-12.shp'))

nat_flow.to_csv(os.path.join(output_path, 'above_marblepoint_flownat_2020-18-12.csv'))

malf_rec.to_csv(os.path.join(output_path, 'above_marblepoint_rec_flow_malf_2020-18-12.csv'))
malf_nat.to_csv(os.path.join(output_path, 'above_marblepoint_nat_flow_malf_2020-18-12.csv'))








































