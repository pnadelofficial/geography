from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class NoLinkClass:
    def __init__(self, driver: webdriver, timeout=20, url=None):
        self.driver = driver
        self.url = url
        self.timeout = timeout

        # search keys
        self.box_1_keys = '*water* OR river* OR lake OR dam OR stream OR tributary OR diversion OR irrigation OR pollution OR water quality OR flood! OR drought! OR channel OR canal OR hydroelect! OR reservoir OR groundwater OR aquifer OR drought OR recharge OR "water table" OR "bore hole"'

    def _click_from_css(self, css_selector):
        element = WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
        )
        element.click()
    
    def _send_keys_from_css(self, css_selector, keys):
        element = WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
        )
        element.send_keys(keys)

    def _init_search(self):
        if self.url:
            self.driver.get(self.url)
        self._click_from_css(".advanced-search") # click advanced search
        self._click_from_css(".menu-node:nth-child(2)") # click to search in News
        self.driver.execute_script("window.scrollTo(0,102)")

    def _box_1(self):
        self._send_keys_from_css(".searchterm-input-box:nth-child(1)", self.box_1_keys) 
        self._click_from_css(".search-input-row-outline > .dropdown:nth-child(3) > .icon")
        self._click_from_css(".expanded .dropdown-option:nth-child(7) > .option-text")
    
    def box_2(self):
        pass
