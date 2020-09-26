# Reviews Counts for Non-US Regions (raw & normalized)
import pandas as pd
import numpy as np
import os

folder = 'non_us_reviews/'
files = os.listdir(folder)

master = pd.DataFrame()
for file in files:
    df = pd.read_csv(folder + file)
    cont_reg = df.Cont_Reg.iloc[0]
    df.date = pd.to_datetime(df.date)
    groupby_df = df.groupby('date').count().resample('W-Sun').sum().reset_index()
    groupby_df = groupby_df[groupby_df.date > '2019-05-31']
    groupby_df = groupby_df[['date', 'listing_id']]
    groupby_df.columns = ['Date', 'Reviews']
    if cont_reg == 'Asia':
        groupby_df = groupby_df[groupby_df.Date < '2020-06-16']  # Due to missing data in subsequent weeks
    norm_revs = (groupby_df.Reviews - groupby_df.Reviews.min()) / (groupby_df.Reviews.max()-groupby_df.Reviews.min())        
    groupby_df['Norm_Reviews'] = norm_revs  # Column w/ normalized weekly values for each cont_reg from 5/31/19 to the last date available
    groupby_df['Region'] = np.full(len(groupby_df), cont_reg)
    master = pd.concat([master, groupby_df])

clean = master[(master.Region != 'Central North America')]  # Removing Belize

clean.to_csv('non_us_norm_nonnorm_reviews_by_cont_reg.csv', index=False)