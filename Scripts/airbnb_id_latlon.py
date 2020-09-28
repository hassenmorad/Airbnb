# Extracting Lat/Lon Coords For US Airbnb Listings w/ Reviews
import pandas as pd

states = pd.read_csv('50 States FIPS.txt', sep='\t')
tables = pd.read_html('http://insideairbnb.com/get-the-data.html')

cities = {}
counter = 0
for table in tables:
    city = table['Country/City'].iloc[0]
    cities[counter] = city
    counter += 1

us = [4,14,16,21,22,23,26,35,39,42,55,57,58,60,63,65,70,73,74,75,76,77,78,80,94,101]

master = pd.DataFrame()
for city_id in us:
    city = cities[city_id].replace(' ','-').replace(',','').replace('.','')
    date = str(pd.to_datetime(tables[city_id]['Date Compiled'].iloc[0]))[:10]
    for state in list(states.Abbrev.unique()) + ['DC']:
        try:
            df = pd.read_csv('http://data.insideairbnb.com/united-states/' + state.lower() + '/' + city.lower() + '/' + date + '/visualisations/listings.csv')
            df = df[['id', 'latitude', 'longitude']]
            break
        except:
            continue
    print(city, state, date)
    master = pd.concat([master, df])

master.columns = ['listing_id', 'latitude', 'longitude']

master.to_csv('airbnb_id_latlon.csv', index=False)