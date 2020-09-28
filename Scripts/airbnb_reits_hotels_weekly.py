
import pandas as pd

hotel_df = pd.read_csv('HLT_weekly.txt')[['Date', 'Close']]
marriot = pd.read_csv('MAR_weekly.txt')[['Date', 'Close']]
hotel_df = hotel_df.merge(marriot, on='Date')
hotel_df.columns = ['Date', 'Hilton', 'Marriott']
hotel_df.Date = pd.to_datetime(hotel_df.Date).astype(str)

reits = ['aple_weekly', 'hst_weekly', 'peb_weekly', 'pk_weekly', 'rhp_weekly', 'xhr_weekly']

reit_df = pd.read_csv(reits[0] + '.txt')[['Date', 'Close']]
for reit in reits[1:]:
    df = pd.read_csv(reit + '.txt')[['Date', 'Close']]
    reit_df = reit_df.merge(df, on='Date')
    
reit_df.columns = ['Date', 'APLE', 'HST', 'PEB', 'PK', 'RHP', 'XHR']

reit_df.Date = pd.to_datetime(reit_df.Date).astype(str)

# 
sp = pd.read_csv('sp500_weekly.txt')
sp = sp[['Date', 'Close']]
sp.columns = ['Date', 'S&P 500']
sp.Date = pd.to_datetime(sp.Date).astype(str)

stocks = sp.merge(reit_df, on='Date').merge(hotel_df, on='Date')

# Calculating Weekly Airbnb Reviews
rev = pd.read_csv('airbnb_reviews_us_cities.csv')
rev.date = pd.to_datetime(rev.date)

week_rev = rev.groupby('date').count().resample('W-Sun').sum().reset_index()
week_rev = week_rev[['date', 'listing_id']]
week_rev.columns = ['Date', 'Airbnb Reviews']

week_rev = week_rev[(week_rev.Date > '2018-09-14') & (week_rev.Date < '2020-08-03')]
week_rev.Date = week_rev.Date.astype(str)

#
comb = pd.merge(stocks, week_rev, on='Date', how='outer').sort_values('Date')

comb_melt = pd.melt(comb, id_vars='Date')

no_date = comb.drop('Date', axis=1)

normalized_df = (no_date-no_date.min())/(no_date.max()-no_date.min())
normalized_df['Date'] = comb.Date.values

normalized_df = pd.melt(normalized_df, id_vars='Date')
normalized_df.columns = ['Date', 'Variable', 'Normalized Value']
normalized_df['Raw Value'] = comb_melt.value.values

normalized_df.to_csv('airbnb_reits_hotels_weekly.csv', index=False)