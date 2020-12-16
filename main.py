from bootstrap import *
import pandas as pd
import re

# Reading data csv file
df = pd.read_csv('clear_data_gathering.csv', sep=',')

# Type to search for
types = ['GYM',
         'Fruit and Vegetable Store',
         'Grocery Store',
         'Nutritionist',
         'Organic Food Store',
         'Physical therapy clinic',
         'Physician',
         'Restaurant',
         'Shopping Mall',
         'store',
         'Supermarket',
         'Vitamin & Supplements Store',
         'ATM',
         'BANK']

# Starting program and looping through dataframe rows
queries = []
for index, row in df.iterrows():
    for type in types:
        # Building search query
        rerun_query = True
        query = f'{type} in {row["quism"]}, {row["governorate"]}'.strip()
        # Remove any extra spaces in the query
        query = re.sub(' +', ' ', query)
        queries.append(query)

# Run mass scraping
mass_scrapping(queries)
