from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys 
from datetime import datetime
import os

# when all this stuff is greyed out, does this mean I'm not using it outside the classes and don't need it here?

from selenium.common.exceptions import (
    StaleElementReferenceException, TimeoutException, 
    ElementClickInterceptedException, ElementNotInteractableException, 
    NoSuchElementException)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select

import pandas as pd
import time
import getpass

from classes.UserClass import UserClass
from classes.LoginClass import PasswordManager, WebDriverManager, Login
from classes.NoLinkClass import NoLinkClass
from classes.DownloadClass import Download

#USER INFORMATION: User and Basin Information Setup (Set this for yourself and the current basin)
external_user = False
basin_code = "gron"
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

time.sleep(5)

if __name__ == "__main__":  

    pm = PasswordManager()
    if pm.password is None:
        password = pm.get_password()
        print("Password set!")
    else: pass
    
    manager = WebDriverManager()
    options = manager.setup_options()
    driver = manager.start_driver()

    time.sleep(5)
    login = Login(user_name=user_name, password=password, driver_manager=manager, url=None)
    
    login._init_login()

time.sleep(5)
nlc = NoLinkClass(driver, basin_code)
nlc._search_process()
time.sleep(10)

download = Download(
    driver=driver,
    basin_code=basin_code,
    user_name=user_name,
    index=0,  
    login = login,
    nlc = nlc,
    download_folder = download_folder,
    download_folder_temp = download_folder_temp,
    status_file=status_file,
    finished=False,  
    url=None,  
    timeout=20  
)

status_data = download.status_data
finished = download.finished

download.main(index=0, basin_code = basin_code)

