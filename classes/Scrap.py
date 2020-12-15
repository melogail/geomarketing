from config import web_driver_config
from selenium import webdriver


class Scrap(object):
    def __init__(self, browser_type='chrome'):
        if browser_type == 'chrome':
            driver_path = web_driver_config['chrome']['path']
            self.driver = webdriver.Chrome(driver_path)

    def run_query(self, query=False):
        pass
