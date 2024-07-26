from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import ElementNotInteractableException
from chromedriver_py import binary_path  

import os
import sys
import pandas as pd
import time

options = Options()
options.page_load_strategy = 'normal'
options.add_argument("--start-maximized")

#options.add_argument("user-data-dir=Users/<username>/Library/Application Support/Google/Chrome/Default")
#prefs = {'download.default_directory' : '/Users/dvas22/Desktop/David/www/geography/downloads'}
options.add_argument("user-data-dir=/tmp/storedLoginInformation4")
prefs = {'download.prompt_for_download' : False}
options.add_experimental_option('prefs', prefs)

service = Service()

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


from geography.classes.UserClass import UserClass

#USER INFORMATION: User and Basin Information Setup (sSet this for yourself and the current basin)
external_user = False
basin_code = "cngo" #testing new search terms
master_user = "selena"

import getpass

password = getpass.getpass()

print("Password set!")

# when you run this, you will be asked to enter your password in the terminal below
# this password will be stored as the variable "password" until you close VSCode
# the script will then use that password variable in the login step




currentUser = UserClass(basin_code, master_user, external_user)
currentUser.getName()
paths = currentUser.getPath("excel")

#Base Paths 
user_name = paths["user_name"]
geography_folder = paths["geography_folder"]
download_folder_temp = paths["download_folder_temp"]
download_folder = paths["download_folder"]
status_file = paths["status_file"]

#and the search terms sheet
#df = pd.read_excel('TrackingSheet_basinterms.xlsx')
df = pd.read_excel('TrackingSheet_NEWbasinterms.xlsx') #to test the new basin search terms
#the sheet is in the same folder as this notebook, otherwise would need full file path
row = df[df['BCODE'] == basin_code.upper()]
search_term = row['Basin_Specific_Terms'].values[0]

def login_tufts_user(user_name):
    time.sleep(3)
    print("Logging in user with userName " + user_name)
    driver.get("https://login.ezproxy.library.tufts.edu/login?auth=tufts&url=http://www.nexisuni.com")
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR, ".btn-shib > .login").click()
    time.sleep(3)
    driver.find_element(By.ID, "username").send_keys(user_name)
    driver.find_element(By.ID, "password").send_keys(password) #this line used to say ...send_keys("")
    
    #And then have a
    time.sleep(5)
    #that would wait for the user to type in their password.

    try:
        driver.find_element(By.NAME, "_eventId_proceed").click()
        time.sleep(5)
    except NoSuchElementException:  
        print("Logged In _eventId_proceed")

    try:
        driver.find_element(By.ID, "trust-browser-button").click()
        time.sleep(5)
    except NoSuchElementException:  
        print("Logged In trust-browser-button")
    time.sleep(5)

    return driver

from classes.NoLinkClass import NoLinkClass

driver = login_tufts_user(user_name)
#working on tying in userclass
nlc = NoLinkClass(driver, search_term)

# the steps below assume we're already on nexis uni homepage.
# so the below line can be added in case we're not logging in
driver.get("https://advance-lexis-com.ezproxy.library.tufts.edu/bisacademicresearchhome?crid=d975d3e5-053d-44cc-85d9-4a1b2f583bea&pdmfid=1516831&pdisurlapi=true")

nlc = NoLinkClass(driver, search_term)
nlc.get_search_term()
nlc._init_search()
nlc._box_1()
nlc._box_2()
nlc._box_3()
nlc._box_4()
nlc.complete_search()