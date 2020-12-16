import time
import datetime
import re
from config import web_driver_config
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from models.QueriesDone import QueriesDone
from models.Cids import Cids


class Scrap(object):
    def __init__(self, browser_type='chrome'):
        if browser_type == 'chrome':
            driver_path = web_driver_config['chrome']['path']
            self.driver = webdriver.Chrome(driver_path)

    def run(self, query):
        # Check the type of scraping running
        # MassScraping Class
        if self.__class__.__name__ == 'MassScraping':
            self.mass_scrap(query)

        elif self.__class__.__name__ == 'DetailsScraping':
            self.details_scrap(query)

    def mass_scrap(self, query):
        """
        Mass scraping code
        :param query:
        :return:
        """
        #check query type
        print('{:=^50}'.format(" Start of Query "), "\n")
        # Saving start time
        start_time = datetime.datetime.now()
        s = start_time.strftime('%H:%M:%S')
        print(f'{query["query"]}, Query Start on: {s}')
        print("Navigating to Google Maps!")

        # Open Google Search and enter the query
        self.driver.get('https://www.google.com/')
        search = self.driver.find_element_by_name('q')
        search.send_keys(query['query'])
        search.send_keys(Keys.RETURN)

        try:
            # Find the view all button
            view_all_btn = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//span[@class='wUrVib']"))
            )
            view_all_btn.click()

            try:
                cids = []
                for i in range(100):
                    # Get all the elements which has 'data-cid' attributes
                    data_cid_elements = WebDriverWait(self.driver, 10).until(
                        EC.visibility_of_all_elements_located((By.XPATH, "//a[@data-cid]"))
                    )
                    # Save cids in array
                    for cid in data_cid_elements:
                        cids.append([cid.get_attribute('data-cid'), query['type']])

                    # move to next page
                    time.sleep(3)
                    try:
                        next_btn = WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located((By.ID, "pnnext"))
                        )
                        next_btn.click()
                    except:
                        print('No more pages to load')
                        break
            except:
                print("Query Failed!")
                print("Cannot find 'a[data-cid]' elements!")
                QueriesDone.insert([[query['query'], datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 0]])
                self.driver.quit()
        except:
            print("Query Failed!")
            print("Unable to Find 'View all' button!")
            QueriesDone.insert([[query['query'], datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 0]])
            self.driver.quit()

        # storing cids
        if len(cids) > 0:
            # Closing the opened query page
            #self.driver.quit()

            print(f'Number of results: {len(cids)}')

            # Saving CIDs in database
            print(f'Saving CIDs to database')
            Cids.insert(cids)
            print(f'Data successfully saved')

            # Saving query in database
            QueriesDone.insert([[query['query'], datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 1]])

            # printing query time duration
            end_time = datetime.datetime.now()
            s = end_time.strftime('%H:%M:%S')
            print(f'{query["query"]}, Query End on: {s}')
            print(f'Query Duration: {end_time - start_time}')
            print("=".format({''}))
            print('{:=^50}'.format(" End of Query "), '\n')
        else:
            print('No CIDs saved!!')

    def details_scrap(self, query):
        """
        Details scraping code
        :param query:
        :return:
        """
        print('{:=^50}'.format(" Start of Query "), "\n")
        # Saving start time
        start_time = datetime.datetime.now()
        s = start_time.strftime('%H:%M:%S')
        print(f'{query}, Query Start on: {s}')
        print("Navigating to Google Maps!")

        # Open Google Search and enter the query
        self.driver.get(f'https://www.google.com/maps?cid={query}')

        # Set data variable
        data = []
        # Get current URL to extract coordinates
        time.sleep(3)
        url = self.driver.current_url
        lng = ''