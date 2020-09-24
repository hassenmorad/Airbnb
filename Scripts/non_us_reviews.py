import pandas as pd
import numpy as np

file = pd.read_csv('Non_US_Cities.csv')

for cont_reg in file.Cont_Reg.unique():
    print(cont_reg)
    temp = file[file.Cont_Reg == cont_reg]
    master = pd.DataFrame()
    for i, row in temp.iterrows():
        print(row.City)
        df = pd.read_csv(row['Reviews Link'])
        df['City'] = np.full(len(df), row.City)
        df['Country'] = np.full(len(df), row.Country)
        df['Continent'] = np.full(len(df), row.Continent)
        df['Region'] = np.full(len(df), row.Region)
        df['Cont_Reg'] = np.full(len(df), cont_reg)
        master = pd.concat([master, df])
    master.to_csv('non_us_reviews_' + cont_reg + '.csv', index=False)