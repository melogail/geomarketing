from config import web_driver_config
from selenium import webdriver
from models.QueriesDone import QueriesDone


class Scrap(object):
    def __init__(self, browser_type='chrome'):
        if browser_type == 'chrome':
            #driver_path = web_driver_config['chrome']['path']
            #self.driver = webdriver.Chrome(driver_path)
            pass



    def run(self, query):
        if self.__class__.__name__ == 'MassScrapping':
            print('MassScrapping code will run here')
        print(query)