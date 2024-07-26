from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import pandas as pd
import time
import getpass

from classes.UserClass import UserClass

#USER INFORMATION: User and Basin Information Setup (Set this for yourself and the current basin)
external_user = False
basin_code = "cngo"
master_user = "selena"

currentUser = UserClass(basin_code, master_user, external_user)
currentUser.getName()
paths = currentUser.getPath("excel")

#Base Paths 
user_name = paths["user_name"]
geography_folder = paths["geography_folder"]
download_folder_temp = paths["download_folder_temp"]
download_folder = paths["download_folder"]
status_file = paths["status_file"]
#might try to put these into userclass, no?

#add time.sleep()s between cells where needed in .py
time.sleep(5)

from classes.LoginClass import WebDriverManager, Login, PasswordManager

if __name__ == "__main__":  
    pm = PasswordManager()
    if pm.password is None:
        password = pm.get_password()
        print("Password set!")
    else: pass
    
    manager = WebDriverManager()
    driver = manager.start_driver()
    options = manager.setup_options()

    time.sleep(5)
    login = Login(user_name=user_name, password=password, driver_manager=manager, url=None)
    
 
    login._init_login()



#and the search terms sheet
tracking_sheet = pd.read_excel('TrackingSheet_NEWbasinterms.xlsx') #to test the new basin search terms
# the sheet is in the same folder as this notebook, otherwise would need full file path
row = tracking_sheet[tracking_sheet['BCODE'] == basin_code.upper()]
search_term = row['Basin_Specific_Terms'].values[0]

time.sleep(5)

def NexisHome():
    nexis_home_substring = 'bisnexishome'
    if nexis_home_substring in driver.current_url:
        print('already on Nexis Uni home page')
        pass
    else:
        print("Navigate to Nexis Uni home page")
        driver.get("https://advance-lexis-com.ezproxy.library.tufts.edu/bisnexishome?crid=6537b0c7-d00a-4047-8afa-732967dfba6e&pdmfid=1519360&pdisurlapi=true")
        time.sleep(3)

# if we're not already on nexis homepage

NexisHome()

# add in the no element exception or whatever.

from classes.NoLinkClass import NoLinkClass
nlc = NoLinkClass(driver, search_term)

def search_process():
    nlc._init_search()
    nlc._search_box()
    time.sleep(5)
    nlc.complete_search() 

search_process()
time.sleep(10)