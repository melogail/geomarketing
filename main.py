from bootstrap import *
import pandas as pd
import re
from models.Cids import Cids

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

# Building queries list
for index, row in df.iterrows():
    for type in types:
        # Building search query
        rerun_query = True
        query = {}
        query['query'] = f'{type} in {row["quism"]}, {row["governorate"]}'.strip()
        query['query'] = re.sub(' +', ' ', query['query'])
        query['type'] = type
        # Remove any extra spaces in the query
        queries.append(query)


# Main section
# Prompting user for scrapping type
print('{:*^50}'.format('*'))
print('{:*^50}'.format(' Welcome to Google Maps Scrapping Tool '))
print('{:*^50}'.format('*'))
print('')
print('What type of scraping you would like to perform?')
print('{:=^50}'.format('Please choose from the following types'))
print('')
print('{:<3} {}'.format('[1]', 'Mass Scrapping'))
print('{:<3} {}'.format('[2]', 'Landmark Details Scrapping'))
scraping_type = input('Your choice: ')

# Choose main scraping type
while scraping_type != '1' and scraping_type != '2':
    print("\nPleas select right choice!")
    scraping_type = input('Your choice: ')

# choose sub-scraping type if exist
if scraping_type == '1':
    # Run mass scraping
    mass_scrapping(queries)
elif scraping_type == '2':
    print('\nWhat kind of landmark data you would like to scrap?')
    print('{:=^50}'.format('Please choose from the following types'))
    print('')
    print('{:<3} {}'.format('[1]', 'All my landmarks saved in my database'))
    print('{:<3} {}'.format('[2]', 'Single landmark from my choice'))
    landmark_scrap = input('Your choice: ')

    # validate choice
    while scraping_type != '1' and scraping_type != '2':
        print("\nPleas select right choice!")
        scraping_type = input('Your choice: ')

    if landmark_scrap == '1':
        for cid in Cids.where({'type': 'Nutritionist'}).get():
            details_scraping(cid[1])

    elif landmark_scrap == '2':
        print('Sorry, This option is not functioning yet!!')
        print('Program terminated...')
        exit()
