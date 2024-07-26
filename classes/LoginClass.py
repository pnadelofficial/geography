from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import ElementNotInteractableException
from webdriver_manager.chrome import ChromeDriverManager

from chromedriver_py import binary_path  

import os
import sys
import pandas as pd
import time
import getpass

'''
#ideally if the section starting line 41 is good we don't need all this

options = Options()
options.page_load_strategy = 'normal'
options.add_argument("--start-maximized")

#options.add_argument("user-data-dir=Users/<username>/Library/Application Support/Google/Chrome/Default")
#prefs = {'download.default_directory' : '/Users/dvas22/Desktop/David/www/geography/downloads'}
options.add_argument("user-data-dir=/tmp/storedLoginInformation10")

prefs = {'download.prompt_for_download' : False}
options.add_experimental_option('prefs', prefs)

service = Service()

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)



#and then example usage
if __name__ == "__main__":
    from Setup import WebDriverManager  # Assuming you save the class in Setup.py

    manager = WebDriverManager()
    driver = manager.start_driver()
'''

class WebDriverManager:
    def __init__(self):
        self.driver = None
        self.setup_options()
        self.setup_service()

    def setup_options(self):
        self.options = ChromeOptions()
        self.options.page_load_strategy = 'normal'
        self.options.add_argument("--start-maximized")
        self.options.add_argument("user-data-dir=/tmp/storedLoginInformation2")        
        prefs = {'download.prompt_for_download': False}
        self.options.add_experimental_option('prefs', prefs)

    def setup_service(self):
        self.service = Service(ChromeDriverManager().install())

    def reset(self):
        self.number += 1 # self.number = self.number + 1
        self.temp_foldername = "storedLoginInformation" + str(self.number)
        # and then somewhere else the following ???
        '''
        # should these two replace line 61?
        #self.temp_foldername = "storedLoginInformation" + str(self.number)
        #self.options.add_argument(self.temp_foldername)
        # at some point I need to refer to reset() method right?
        '''
    
    def start_driver(self):
        if not self.driver:
            self.driver = webdriver.Chrome(service=self.service, options=self.options)
        return self.driver

    def stop_driver(self):
        if self.driver:
            self.driver.quit()
            self.driver = None

class PasswordManager:
    def __init__(self):
        # Initialize the password attribute to None
        self.password = None

    def get_password(self):
        # Check if the password is already set
        if self.password is None:
            # Prompt for the password and store it
            self.password = getpass.getpass()
        # Return the stored password
        return self.password

'''
# Create an instance of PasswordManager
pm = PasswordManager()
if pm.password is None:
    password = pm.get_password()
    print("Password set!")
else: pass
'''

#is this right? will it ask again?

class Login:
    def __init__(self, user_name, password, driver_manager= WebDriverManager, timeout=20, url=None):
        self.driver_manager = driver_manager
        self.driver = driver_manager.start_driver()
        self.user_name = user_name
        self.password = password
        self.url = url
        self.timeout = timeout

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

    def _init_login(self):
        print("Logging in user with userName " + self.user_name)
        loggedin_home = "https://login.ezproxy.library.tufts.edu/login?auth=tufts&url=http://www.nexisuni.com"
        self.driver.get(self.url or loggedin_home)
        self._click_from_css(".btn-shib > .login")
        #driver.find_element(By.ID, "username").send_keys(self.user_name)
        self._send_keys_from_css("#username", self.user_name)  # Using ID selector
        #driver.find_element(By.ID, "password").send_keys(password)
        self._send_keys_from_css("#password", self.password)   # Using ID selector
        #driver.find_element(By.NAME, "_eventId_proceed").click()
        self._click_from_css("#login > button")
        print("entered Tufts username and password")

        #in case update chrome page comes up
        time.sleep(3)
        update_chrome_substring = "https://api-58712eef.duosecurity.com/frame/frameless/v4/auth?sid=frameless-"
        if update_chrome_substring in self.driver.current_url:
            self._click_from_css("body > div > div > div > div.display-flex.flex-direction-column.flex-value-one.size-padding-left-large.size-padding-right-large > div > button")
            print("skipped update chrome page")
        else:
            pass
    
        #DUO to try to automate
        # in case we're allowed to use an IT bypass code
        #bypass_code = 123456789 # replace with the bypass code
        time.sleep(3)
        duo_page_substring = "https://api-58712eef.duosecurity.com/frame/v4/auth/prompt?sid=frameless-"
        if duo_page_substring in self.driver.current_url:
            print('DUO push code on screen OR wait for call')
            time.sleep(10)
        else: pass
        
        if duo_page_substring in self.driver.current_url:
            other_options_selector = "#auth-view-wrapper > div:nth-child(2) > div.row.display-flex.other-options-link.align-flex-justify-content-center.size-margin-bottom-large.size-margin-top-small"
            self._click_from_css(other_options_selector)
            DUO_phone_call = 'body > div > div > div.card.card--white-label.uses-white-label-border-color.display-flex.flex-direction-column > div > div.all-auth-methods.display-flex.flex-value-one > ul > li:nth-child(2) > a > span.method-select-chevron > svg'
            self._click_from_css(DUO_phone_call)
            print('DUO calling')
            time.sleep(10)
        else: pass

        #if DUO fails (sometimes won't call phone), try again
        #if duo_page_substring in self.driver.current_url:
            #time.sleep(2)
            # can do other options again and find selector for code again
            # and another time.sleep()


        #in case trust browser page comes up
        time.sleep(3)
        trust_browser_substring = "https://api-58712eef.duosecurity.com/frame/v4/auth/prompt?sid=frameless-"
        if trust_browser_substring in self.driver.current_url :
            self._click_from_css("#trust-browser-button")
            print("skipped trust browser page")
            
        else:
            pass

# plop into main
'''
from classes.LoginClass import WebDriverManager, Login, PasswordManager

if __name__ == "__main__":  
    
    # will ask for and set password
    pm = PasswordManager()
    if pm.password is None:
        password = pm.get_password()
        print("Password set!")
    else: pass
    
    # will open chrome
    manager = WebDriverManager()
    driver = manager.start_driver()
    options = manager.setup_options()

    # will log in (tufts)
    login = Login(user_name=user_name, password=password, driver_manager=manager, url=None)
    login._init_login()

'''

