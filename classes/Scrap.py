import time
import datetime
import re
from config import web_driver_config
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from models.QueriesDone import QueriesDone
from models.Landmark import Landmark
from models.Cids import Cids

# TODO:: Fix running scrap class on every call without checking performed queries
class Scrap(object):

    # driver object
    driver = None

    # Browser type
    browser_type = 'chrome'

    def __init__(self, browser_type='chrome'):
        #TODO:: Set how to choose browser type
        pass

    def launch_driver(self):
        if self.browser_type == 'chrome':
            driver_path = web_driver_config['chrome']['path']
            driver_options = webdriver.ChromeOptions()
            driver_options.add_argument("--lang=en_UK")
            driver_options.add_argument('disable-infobars')
            caps = DesiredCapabilities().CHROME
            caps["pageLoadStrategy"] = "eager"  #  complete
            return webdriver.Chrome(driver_path, chrome_options=driver_options, desired_capabilities=caps)

    def run(self, query):

        self.driver = self.launch_driver()
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
        # check query type
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
                # storing cids
                if len(cids) > 0:
                    # Closing the opened query page
                    # self.driver.quit()

                    print(f'Number of results: {len(cids)}')

                    # Saving CIDs in database
                    print(f'Saving CIDs to database')
                    Cids.insert(cids)
                    print(f'Data successfully saved')

                    # Saving query in database
                    QueriesDone.insert(
                        [[query['query'], datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 1, 'cid']])

                    # printing query time duration
                    end_time = datetime.datetime.now()
                    s = end_time.strftime('%H:%M:%S')
                    print(f'{query["query"]}, Query End on: {s}')
                    print(f'Query Duration: {end_time - start_time}')
                    print("=".format({''}))
                    print('{:=^50}'.format(" End of Query "), '\n')
                else:
                    print('No CIDs saved!!')
            except:
                print("Query Failed!")
                print("Cannot find 'a[data-cid]' elements!")
                QueriesDone.insert([[query['query'], datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 0, 'cid']])
                # self.driver.quit()
        except:
            print("Query Failed!")
            print("Unable to Find 'View all' button!")
            QueriesDone.insert([[query['query'], datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 0, 'cid']])
            # self.driver.quit()

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
        print(f'Getting CID: {query} details, Query Start on: {s}')
        print("Navigating to Google Maps!")
        
        self.driver.get(f'https://www.google.com/maps?cid={query}')
        
        try:
            # Set data variable
            landmark_details = []
            # Get current URL to extract coordinates
            time.sleep(3)
            flag = False

            # Get landmark coordinates
            while flag == False:
                url = self.driver.current_url
                try:
                    lat = re.search(r'(?<=!3d)(.*?)(?=!4d)', url).group(0)
                    lng = re.search(r'(?<=!4d)(.*?)$', url).group(0)
                    flag = True
                except Exception as e:
                    print('Trying to get landmark coordinates!')
                    time.sleep(2)

            try:
                # Get landmark image
                image_container = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_all_elements_located(
                        (By.XPATH, '//button[contains(@class, "section-hero-header-image-hero")]'))
                )
                for el in image_container:
                    try:
                        image = el.find_element_by_tag_name('img').get_attribute('src')
                    except Exception as e:
                        image = None
            except Exception as e:
                print("cannot find image container")

            try:
                # Get landmark title
                title_container = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//h1[contains(@class, "section-hero-header-title-title")]'))
                )
                name = title_container.find_element_by_tag_name('span').text
            except Exception as e:
                print("Cannot find landmark name")
                exit()

            try:
                # Get landmark sub-title
                sub_title_container = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//h2[contains(@class, "section-hero-header-title-subtitle")]'))
                )
                sub_name = sub_title_container.find_element_by_tag_name('span').text
            except Exception as e:
                sub_name = None

            try:
                # Get landmark reviews and user total reviews
                reviews_container = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//div[@class="section-rating"]'))
                )
                reviews = reviews_container.find_element_by_xpath('//span[@class="section-star-display"]').text
                user_total_reviews = reviews_container.find_element_by_xpath(
                    '//button[@jsaction="pane.rating.moreReviews"]').text
                user_total_reviews = re.search(r'\d+', user_total_reviews).group(0)
            except Exception as e:
                reviews = None
                user_total_reviews = None

            try:
                # Get landmark type
                type_container = reviews_container.find_element_by_xpath('//span[@class="section-rating-term"]')
                type = type_container.find_element_by_xpath('//button[@jsaction="pane.rating.category"]').text
            except:
                type = None

            try:
                # Getting landmark data
                info_data = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located(
                        (By.XPATH, '//button[@data-item-id]'))
                )

                # Landmark data variables
                address_en = None
                address_ar = None
                website = None
                phone_number = None
                plus_code = None

                # sleep time for assuring that rest of HTML is rendered
                time.sleep(2)
                for data in info_data:
                    if data.get_attribute('data-item-id') == 'address' and address_en is None:
                        value = data.find_element_by_xpath('.//div[contains(@class, "__primary-text")]')
                        address_en = value.text

                    elif data.get_attribute('data-item-id') == 'laddress' and address_ar is None:
                        value = data.find_element_by_xpath('.//div[contains(@class, "__primary-text")]')
                        address_ar = value.text

                    elif data.get_attribute('data-item-id') == 'authority' and website is None:
                        value = data.find_element_by_xpath('.//div[contains(@class, "__primary-text")]')
                        website = value.text

                    elif 'phone:' in data.get_attribute('data-item-id') and phone_number is None:
                        value = data.find_element_by_xpath('.//div[contains(@class, "__primary-text")]')
                        phone_number = value.text

                    elif data.get_attribute('data-item-id') == 'oloc' and plus_code is None:
                        value = data.find_element_by_xpath('.//div[contains(@class, "__primary-text")]')
                        plus_code = value.text

            except Exception as e:
                print("Cannot find landmark information!" + str(e))

            # Saving data to the database
            landmark_details.append(
                [query, name, sub_name, lat, lng, reviews, user_total_reviews, type, address_en, address_ar, plus_code,
                 phone_number, website, image])
            Landmark.insert(landmark_details)
            QueriesDone.insert([[query, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 1, 'landmark_details']])
            self.driver.quit()

        except Exception as e:
            print('Error occurred while running this query!' + str(e))
            QueriesDone.insert([[query, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 0, 'landmark_details']])
            self.driver.quit()