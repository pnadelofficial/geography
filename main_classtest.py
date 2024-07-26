from geography.classes.UserClass import UserClass
from classes.BasinClass import BasinClass
from classes.NoLinkClass import NoLinkClass

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from chromedriver_py import binary_path  

import os
import sys
import pandas as pd
import time

#USER INFORMATION: User and Basin Information Setup (sSet this for yourself and the current basin)
external_user = True
basin_code = "hanx" 
master_user = "selena"

#SETUP: 
#PART 1: Chrome Configuration 
options = Options()
options.page_load_strategy = 'normal'
options.add_argument("--start-maximized")

#options.add_argument("user-data-dir=Users/<username>/Library/Application Support/Google/Chrome/Default")
#prefs = {'download.default_directory' : '/Users/dvas22/Desktop/David/www/geography/downloads'}
options.add_argument("user-data-dir=/tmp/storedLoginInformation1")
prefs = {'download.prompt_for_download' : False}
options.add_experimental_option('prefs', prefs)

service = Service()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

#PART 2: File Paths for each user
currentUser = UserClass(basin_code, master_user, external_user)
currentBasin = BasinClass(basin_code, external_user)

currentUser.getName()
paths = currentUser.getPath("excel")

#Base Paths 
user_name = paths["user_name"]
geography_folder = paths["geography_folder"]
download_folder_temp = paths["download_folder_temp"]
download_folder = paths["download_folder"]
status_file = paths["status_file"]

#Search Link
#search_link = currentBasin.get_basin_path()

#Set Basin Status CSV File 
status_data = pd.read_csv(status_file, index_col=0)

def main():
    
    #OSU Login
    #single_login() #this is for non Tufts users 
    
    #Tufts Login:
    #login_tufts_user(user_name)
    
    #Run Main Program
    single_basin_search() 
    time.sleep(60)


#Single Basin Search
def single_basin_search():
    print("MAIN: Starting a single basin search for ", basin_code)
    
    for index, row in status_data.iterrows():
        #basin = row['Basin_Name']
        basin = row['BCODE'] 
        start_date = convert_date(row['start_date'])
        end_date = convert_date(row['end_date'])
        finished = row['finished']

        if finished == 2:
             print(basin_code, " is done!")
             time.sleep(1)
             quit()

        if finished != 1:

            #STEP 1: Base Search 
            base_search()

df = pd.read_excel('TrackingSheet_basinterms.xlsx')
#the sheet is in the same folder as this notebook, otherwise would need full file path
#in NoLinkClass we'd want to refer to basin_code variable in main.py
row = df[df['BCODE'] == basin_code.upper()]
search_term = row['Basin_Specific_Terms'].values[0]
#print(search_term) 
nlc = NoLinkClass(driver, search_term)           

#STEP 1: Navigate to first level search
def base_search(): 
    nlc = NoLinkClass(driver, search_term)
    nlc.get_search_term()
    nlc._init_search()
    nlc._box_1()
    nlc._box_2()
    nlc._box_3()
    nlc._box_4()
    nlc.complete_search()


#### UTILITY FUNCTIONS ####   
#FUNCTIONS A: Login Related Functions (there are three login functions one for a Tufts user, one for an external user and one that will run once if the login session is not working)
#Function A1: Login an internal Tufts User 
def login_tufts_user(user_name):
    time.sleep(3)
    print("Logging in user with userName " + user_name)
    driver.get("https://login.ezproxy.library.tufts.edu/login?auth=tufts&url=http://www.nexisuni.com")
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR, ".btn-shib > .login").click()
    time.sleep(3)
    driver.find_element(By.ID, "username").send_keys(user_name)
    driver.find_element(By.ID, "password").send_keys("")

    #Wait for user to manually put in user name 60 seconds
    time.sleep(30)
    try:
        driver.find_element(By.NAME, "_eventId_proceed").click()
        time.sleep(10)
    except NoSuchElementException:  
        print("Logged In _eventId_proceed")

    try:
        driver.find_element(By.ID, "trust-browser-button").click()
        time.sleep(10)
    except NoSuchElementException:  
        print("Logged In trust-browser-button")
    time.sleep(20)

    
#Function A2: Login an External User with Temporary Access
def login_external_user():
    print("LOGIN") 
    print("Step 1: Get base search link") 
    #driver.get("https://nam04.safelinks.protection.outlook.com/?url=https%3A%2F%2Ftufts.alma.exlibrisgroup.com%2Fview%2FemailLogin%3Finstitute%3D01TUN_INST%26jwt%3DeyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJBbG1hIiwiYXVkIjoiUHJpbW8iLCJleHAiOjE2OTMwOTMzNzksImp0aSI6Ik9QSHBnNXFSbEZRWjVDUVhiUGFxM2ciLCJpYXQiOjE2OTMwODk3NzksIm5iZiI6MTY5MzA4OTY1OSwic3ViIjoicGF0cm9uIiwiaWQiOiIyMTE5MjU0ODI5MDAwMzg1MSIsIm5hbWUiOiJDaGFybGVzLCBEYXZpZCIsImVtYWlsIjoidmFzcXVlemRAb3JlZ29uc3RhdGUuZWR1IiwicHJvdmlkZXIiOiJFTUFJTCIsImZpcnN0X25hbWUiOiJEYXZpZCIsImxhc3RfbmFtZSI6IkNoYXJsZXMifQ.TGOloKdYD2xLHiedNJiHsM62Jrxc6fXLKqoxcMfrKuw%26backUrl%3Dhttps%253A%252F%252Ftufts.primo.exlibrisgroup.com%252Fprimaws%252FsuprimaLogin%253Fsortby%253Drank%2526vid%253D01TUN_INST%253A01TUN%2526lang%253Den%2526target-url%253Dhttps%25253A%25252F%25252Ftufts.primo.exlibrisgroup.com%25252Fdiscovery%25252Fsearch%25253Fsortby%25253Drank%252526vid%25253D01TUN_INST%25253A01TUN%252526lang%25253Den&data=05%7C01%7Cvasquezd%40oregonstate.edu%7C7567c95eff17406b9bd208dba685cd10%7Cce6d05e13c5e4d6287a84c4a2713c113%7C0%7C0%7C638286865856140715%7CUnknown%7CTWFpbGZsb3d8eyJWIjoiMC4wLjAwMDAiLCJQIjoiV2luMzIiLCJBTiI6Ik1haWwiLCJXVCI6Mn0%3D%7C3000%7C%7C%7C&sdata=%2BDGfY8G4tN8GpUeAlFW%2BZux%2BORKQxoVCePxKR9zqoUc%3D&reserved=0")
    time.sleep(2)
    driver.get("https://tufts.primo.exlibrisgroup.com/discovery/search?sortby=rank&vid=01TUN_INST:01TUN&lang=en")
    time.sleep(4)
    driver.find_element(By.ID, "searchBar").click()
    time.sleep(2)
    print("Step 2: Search for Nexis Uni") 
    driver.find_element(By.ID, "searchBar").send_keys("nexis uni")
    time.sleep(2)
    driver.find_element(By.ID, "searchBar").send_keys(Keys.ENTER)
    time.sleep(4)
    driver.find_element(By.CSS_SELECTOR, "#alma991017244849703851availabilityLine0 > .availability-status").click()
    time.sleep(6)
    print("Step 3: Move to new window") 
    driver.switch_to.window(driver.window_handles[1])
    driver.find_element(By.CSS_SELECTOR, ".btn-library > .login").click()
    time.sleep(1)
    print("Step 4: Send Temporary Code") 
    driver.find_element(By.ID, "user").click()
    time.sleep(1)

    driver.find_element(By.ID, "user").send_keys("862295360")
    time.sleep(1)

    driver.find_element(By.NAME, "submit").click()
    print("Step 5: Finish pause to sleep")
    time.sleep(8)


#Function A3: Login that runs once (if the browser crashed you will have to login again)
def single_login():
    print("single login") 
    #driver.get("https://nam04.safelinks.protection.outlook.com/?url=https%3A%2F%2Ftufts.alma.exlibrisgroup.com%2Fview%2FemailLogin%3Finstitute%3D01TUN_INST%26jwt%3DeyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJBbG1hIiwiYXVkIjoiUHJpbW8iLCJleHAiOjE2OTMwOTMzNzksImp0aSI6Ik9QSHBnNXFSbEZRWjVDUVhiUGFxM2ciLCJpYXQiOjE2OTMwODk3NzksIm5iZiI6MTY5MzA4OTY1OSwic3ViIjoicGF0cm9uIiwiaWQiOiIyMTE5MjU0ODI5MDAwMzg1MSIsIm5hbWUiOiJDaGFybGVzLCBEYXZpZCIsImVtYWlsIjoidmFzcXVlemRAb3JlZ29uc3RhdGUuZWR1IiwicHJvdmlkZXIiOiJFTUFJTCIsImZpcnN0X25hbWUiOiJEYXZpZCIsImxhc3RfbmFtZSI6IkNoYXJsZXMifQ.TGOloKdYD2xLHiedNJiHsM62Jrxc6fXLKqoxcMfrKuw%26backUrl%3Dhttps%253A%252F%252Ftufts.primo.exlibrisgroup.com%252Fprimaws%252FsuprimaLogin%253Fsortby%253Drank%2526vid%253D01TUN_INST%253A01TUN%2526lang%253Den%2526target-url%253Dhttps%25253A%25252F%25252Ftufts.primo.exlibrisgroup.com%25252Fdiscovery%25252Fsearch%25253Fsortby%25253Drank%252526vid%25253D01TUN_INST%25253A01TUN%252526lang%25253Den&data=05%7C01%7Cvasquezd%40oregonstate.edu%7C7567c95eff17406b9bd208dba685cd10%7Cce6d05e13c5e4d6287a84c4a2713c113%7C0%7C0%7C638286865856140715%7CUnknown%7CTWFpbGZsb3d8eyJWIjoiMC4wLjAwMDAiLCJQIjoiV2luMzIiLCJBTiI6Ik1haWwiLCJXVCI6Mn0%3D%7C3000%7C%7C%7C&sdata=%2BDGfY8G4tN8GpUeAlFW%2BZux%2BORKQxoVCePxKR9zqoUc%3D&reserved=0")
    time.sleep(2)
    driver.get("https://tufts.primo.exlibrisgroup.com/discovery/search?sortby=rank&vid=01TUN_INST:01TUN&lang=en")
    time.sleep(4)
    driver.find_element(By.ID, "searchBar").click()
    time.sleep(2)
    driver.find_element(By.ID, "searchBar").send_keys("nexis uni")
    time.sleep(2)
    driver.find_element(By.ID, "searchBar").send_keys(Keys.ENTER)
    time.sleep(4)
    driver.find_element(By.CSS_SELECTOR, "#alma991017244849703851availabilityLine0 > .availability-status").click()
    time.sleep(6)
    driver.switch_to.window(driver.window_handles[1])
    driver.find_element(By.CSS_SELECTOR, ".btn-library > .login").click()
    time.sleep(1)

    driver.find_element(By.ID, "user").click()
    time.sleep(1)

    driver.find_element(By.ID, "user").send_keys("862295360")
    time.sleep(1)

    driver.find_element(By.NAME, "submit").click()

    time.sleep(4)
 
#Function B3: Convert excel date to correct format
def convert_date(date):
   """Convert date format to match this output (add leading zeros and make year 4 digits)
   Month/Day/Year
   01/01/2000
   """

    # Split date
   if "/" in date: 
        date_list = date.split('/')
        day = date_list[1]
        month = date_list[0]
        year = date_list[2]

   elif "-" in date:
        date_list = date.split('-')
        day = date_list[1]
        month = date_list[0]
        year = date_list[2]
   else: 
        day = "01"
        month = "01"
        year = "2000"
        print(date, "Date is not in correct format. Please check the status sheet ")
        sys.exit(1)

   if len(date_list) < 2:
        day = "01"
        month = "01"
        year = "2000"
        print(date, "Date is not in correct format. Please check the status sheet ")
        sys.exit(1)

   # Convert Day  
   if len(day) < 2:
        correct_day = "0" + day
   else:
        correct_day = day

   # Convert Month
   if len(month) < 2:
       correct_month = "0" + month
   else:
        correct_month = month

    # Convert Year
   if len(year) < 3:
        correct_year = "20" + year
   else:
        correct_year = year

   correct_date = correct_month + "/" + correct_day + "/" + correct_year

   return correct_date    

if __name__ == "__main__":
    main()


