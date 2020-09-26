import pandas as pd
import numpy as np

file = pd.read_csv('Non_US_Cities.csv')

for country in file.Country.unique():
    print(country)
    temp = file[file.Country == country]
    master = pd.DataFrame()
    for i, row in temp.iterrows():
        print(row.City)
        df = pd.read_csv(row['Reviews Link'])
        df['City'] = np.full(len(df), row.City)
        df['Country'] = np.full(len(df), row.Country)
        df['Continent'] = np.full(len(df), row.Continent)
        df['Region'] = np.full(len(df), row.Region)
        master = pd.concat([master, df])
    master.to_csv('non_us_reviews_' + country + '.csv', index=False)