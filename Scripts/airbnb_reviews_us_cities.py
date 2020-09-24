# Airbnb reviews data for major US cities (source: http://insideairbnb.com/get-the-data.html)
import pandas as pd
import numpy as np

# US state abbreviations (will reference below)
states = pd.read_csv('50 States FIPS.txt', sep='\t')

# All data tables available on site
tables = pd.read_html('http://insideairbnb.com/get-the-data.html')

# 
cities = {}
counter = 0
for table in tables:
    city = table['Country/City'].iloc[0]
    cities[counter] = city
    counter += 1

# US cities
us = [4,14,16,21,22,23,26,35,39,42,55,57,58,60,63,65,70,73,74,75,76,77,78,80,94,101]

# 
master = pd.DataFrame()
for city_id in us:
    city = cities[city_id].replace(' ','-').replace(',','').replace('.','')
    date = str(pd.to_datetime(tables[city_id]['Date Compiled'].iloc[0]))[:10]
    for state in list(states.Abbrev.unique()) + ['DC']:
        try:
            df = pd.read_csv('http://data.insideairbnb.com/united-states/' + state.lower() + '/' + city.lower() + '/' + date + '/visualisations/reviews.csv')
            df['City'] = np.full(len(df), city.replace('-', ' '))
            df['State'] = np.full(len(df), state)
            break
        except:
            continue
    master = pd.concat([master, df])

master.City = master.City.apply(lambda x:x.title().replace('-', ' '))
master.State = master.State.apply(lambda x:x.upper())

master.to_csv('airbnb_reviews_us_cities.csv', index=False)