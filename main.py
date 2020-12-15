import time
import datetime
import pandas as pd
import re

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# import models
from models.Cids import Cids
from models.QueriesDone import QueriesDone
from models.Shiakha import Shiakha
from models.Quism import Quism
from models.Governorate import Governorate

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
for index, row in df.iterrows():
    for type in types:
        # Building search query
        rerun_query = True
        query = f'{type} in {row["quism"]}, {row["governorate"]}'.strip()
        # Remove any extra spaces in the query
        query = re.sub(' +', ' ', query)

        # Check if the query already done before
        # which is saved inside queries_done table
        for search_query in QueriesDone.all():
            if query in search_query[1]:
                print(f'This query already done on: {search_query[2]}')
                rerun_query = False
        # Skip query from rerun again
        if not rerun_query:
            continue

        print('{:=^50}'.format(" Start of Query "), "\n")
        # Saving start time
        start_time = datetime.datetime.now()
        s = start_time.strftime('%H:%M:%S')
        print(f'{query}, Query Start on: {s}')

        driver_path = '.\chromedriver.exe'
        driver = webdriver.Chrome(driver_path)

        print("Navigating to Google Maps!")

        # Open Google Search and enter the query
        driver.get('https://www.google.com/')
        search = driver.find_element_by_name('q')
        search.send_keys(query)
        search.send_keys(Keys.RETURN)

        try:
            # Find the view all button
            view_all_btn = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//span[@class='wUrVib']"))
            )
            view_all_btn.click()

            try:
                cids = []

                for i in range(100):
                    # Get all the elements which has 'data-cid' attributes
                    data_cid_elements = WebDriverWait(driver, 10).until(
                        EC.visibility_of_all_elements_located((By.XPATH, "//a[@data-cid]"))
                    )
                    # Save cids in array
                    for cid in data_cid_elements:
                        cids.append([cid.get_attribute('data-cid'), type])

                    # move to next page
                    time.sleep(3)
                    try:
                        next_btn = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.ID, "pnnext"))
                        )
                        next_btn.click()
                    except:
                        print('No more pages to load')
                        break
            except:
                print("Query Failed!")
                print("Cannot find 'a[data-cid]' elements!")
                QueriesDone.insert([[query, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 0]])
                driver.quit()
                continue
        except:
            print("Query Failed!")
            print("Unable to Find 'View all' button!")
            QueriesDone.insert([[query, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 0]])
            driver.quit()
            continue

        # storing cids
        if len(cids) > 0:
            # Closing the opened query page
            driver.quit()

            print(f'Number of results: {len(cids)}')

            # Saving CIDs in database
            print(f'Saving CIDs to database')
            Cids.insert(cids)
            print(f'Data successfully saved')

            # Saving query in database
            QueriesDone.insert([[query, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 1]])

            # printing query time duration
            end_time = datetime.datetime.now()
            s = end_time.strftime('%H:%M:%S')
            print(f'{query}, Query End on: {s}')
            print(f'Query Duration: {end_time - start_time}')
            print("=".format({''}))
            print('{:=^50}'.format(" End of Query "), '\n')
