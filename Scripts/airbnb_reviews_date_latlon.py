# Linking US Airbnb Reviews w/ Lat/Lon Coords

import pandas as pd

reviews = pd.read_csv('airbnb_reviews_us_cities.csv')
listings = pd.read_csv('airbnb_id_latlon.csv')

comb = pd.merge(listings, reviews, on='listing_id', how='right')

# 2019-2020 Data
recent = comb[comb.date > '2019-03-31']
recent.to_csv('airbnb_reviews_date_latlon_1920.csv', index=False)

# Removing City & State cols to ease conversion to .shp
drop_loc = comb.drop(['City','State'], axis=1)
drop_loc.to_csv('airbnb_reviews_date_latlon.csv', index=False)