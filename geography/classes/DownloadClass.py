from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys 
from datetime import datetime

from selenium.common.exceptions import (
    StaleElementReferenceException, TimeoutException, 
    ElementClickInterceptedException, ElementNotInteractableException, 
    NoSuchElementException)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select

import pandas as pd
import time
import os

from classes.LoginClass import Login
from classes.NoLinkClass import NoLinkClass
from classes.conversions.combine_results import CombineResults


class ResetRequiredException(Exception):
    pass

class SkipRowException(Exception):
    pass

class SingleResultException(Exception):
    pass

class Download:

    def __init__(self, driver, basin_code, user_name, index, login, nlc, download_folder: str, download_folder_temp, status_file, finished, url = None, timeout = 20):
        self.driver = driver
        self.basin_code = basin_code
        self.user_name = user_name
        self.index = index
        self.login = login
        self.nlc = nlc
        self.status_file = status_file
        self.finished = finished 
        self.url = url
        self.timeout = timeout
        self.download_folder = download_folder
        self.download_folder_temp = download_folder_temp 
        
        #Set Basin Status CSV File 
        self.status_data = pd.read_csv(status_file, index_col=0)
        #self.result_tally = 0  # initialize it at 0
    
    def _click_from_xpath(self, xpath):
        try:
            element = WebDriverWait(self.driver, self.timeout).until(
                EC.element_to_be_clickable((By.XPATH, xpath)))
            element.click()
        except TimeoutException:
            raise NoSuchElementException(f"Element with xpath '{xpath}' not found")
        
        #can move if run-through containing xpaths works 
        #wait = WebDriverWait(driver, 10)
        #element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath))) 
        #self.driver.execute_script("arguments[0].scrollIntoView();", element)
        #element.click()

    def _send_keys_from_xpath(self, xpath, keys):
        wait = WebDriverWait(self.driver, self.timeout)
        element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath))) 
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        element.send_keys(keys)

    def _click_from_css(self, css_selector):
        try:
            element = WebDriverWait(self.driver, self.timeout).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector))
            )
            element.click()
        except TimeoutException:
            raise NoSuchElementException(f"Element with selector '{css_selector}' not found")

       
    def _send_keys_from_css(self, css_selector, keys):
        element = WebDriverWait(self.driver, self.timeout).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
        )
        element.send_keys(keys)

    def open_timeline(self):
        timeline_button = '#podfiltersbuttondatestr-news' # this is CSS selector
        self._click_from_css(timeline_button)
        time.sleep(10)
        # instead try with XPath
        #wait = WebDriverWait(driver, 10)
        #timeline_button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/main/div/main/ln-gns-resultslist/div[2]/div/div[1]/div[1]/div[2]/div/aside/button[2]")))
        #timeline_button.click()
        #time.sleep(5)

    def parse_date(self, date_string):
        date_formats = [
            '%m/%d/%y',  # 8/1/08
            '%m/%d/%Y',  # 8/1/2008
            '%Y-%m-%d',  # 2008-08-01
            '%d-%m-%Y',  # 01-08-2008
            '%Y/%m/%d',  # 2008/08/01
            # Add more formats as needed
        ]
        
        for date_format in date_formats:
            try:
                return datetime.strptime(date_string, date_format)
            except ValueError:
                continue
        
        # If no format worked, raise an error
        raise ValueError(f"Unable to parse date string: {date_string}")
        # this would be a good place to add an exception
        #and then maybe add in a skip/break of the loop, move to next index #
        
    def set_date_range(self, index):

        #START_DATE AND END_DATE get established here
        row = self.status_data.index.get_loc(index)
        start_date_column = self.status_data.columns.get_loc('start_date')
        end_date_column = self.status_data.columns.get_loc('end_date')

        self.start_date_raw = self.status_data.iloc[row, start_date_column]
        self.end_date_raw = self.status_data.iloc[row, end_date_column]

        try:
            start_date_str = self.parse_date(self.start_date_raw)
            end_date_str = self.parse_date(self.end_date_raw)
        except ValueError as e:
            print(f"Error parsing dates for index {index}: {e}")
            return

        self.start_date = start_date_str.strftime('%m/%d/%Y')
        self.end_date = end_date_str.strftime('%m/%d/%Y')

        print(f"Setting the date range from {self.start_date} to {self.end_date}")
        time.sleep(1)

        timeline_reset_button = '#sidebar > div.search-controls > div.filter-container.filterpanel-target > ul > li:nth-child(2) > button > span'
        try:
            self._click_from_css(timeline_reset_button)
            print("Cleared previous timeline filter")
            time.sleep(10)
        except (NoSuchElementException, TimeoutException):
            print("Default time filter")

            print("Opening timeline")
            self.open_timeline()
              
        # these are css selectors
        #min_date_field = '#refine > div.supplemental.timeline > div.date-form > div.min-picker > input'
        #max_date_field = '#refine > div.supplemental.timeline > div.date-form > div.max-picker > input'
        
        # trying again with xpaths instead of css selector
        self.min_date_field = "//input[@class='min-val' and @aria-label='Input Min Date']"
        self.max_date_field = "//input[@class='max-val' and @aria-label='Input Max Date']"

        # need to include error handling for when timeline freezes, see what David did
        
        '''
        try:
            self._click_from_css(min_date_field)
            
        except NoSuchElementException:
            print('timeline frozen')
            # try something like:
            driver.refresh() # does that work? or:
            #search_link = driver.current_url
            #driver.get(search_link) # ??? or:
            #driver.execute_script("location.reload()")
            time.sleep(5)
            self.open_timeline()
            time.sleep(5)
            # how did he get it to try several times
            pass
        # if after five tries, still no timeline, reset login information
        '''

        # Clear out the default min date
        #self._click_from_css(min_date_field)
        time.sleep(5)
        self.select_all = Keys.COMMAND, "a"
        #self._send_keys_from_css(min_date_field, select_all); 

        # try with xpath
        self._send_keys_from_xpath(self.min_date_field, self.select_all); 
        # Put the new min date in 
        self._send_keys_from_xpath(self.min_date_field, self.start_date)
        print (f"Min date set to {self.start_date}")
        time.sleep(3)

        # Clear out the default max date 
        self._send_keys_from_xpath(self.max_date_field, self.select_all); 
        # Put the new max date in 
        self._send_keys_from_xpath(self.max_date_field, self.end_date)
        print (f"Max date set to {self.end_date}")
        time.sleep(3)

        timeline_ok_button = '#refine > div.supplemental.timeline > div.date-form > button'

        try:
            self._click_from_css(timeline_ok_button)
            time.sleep(10) 
        except NoSuchElementException:
            self.driver.refresh()
            print (f"resetting dates to default")
            raise SingleResultException

    def group_duplicates(self):
        actions_dropdown_xpath = "//button[@id='resultlistactionmenubuttonhc-yk' and text()='Actions']"
        time.sleep(5)
        self._click_from_xpath(actions_dropdown_xpath)
        time.sleep(5)
        moderate_button = "//button[contains(@class, 'action') and @data-action='changeduplicates' and @data-value='moderate']"
        self._click_from_xpath(moderate_button)
        print("group duplicate results by moderate similarity")
        time.sleep(10)
    
    def sort_by_date(self):
        sortby_dropdown_css = '#select'
        oldestnewest_option_text = 'Date (oldest-newest)'
            
        def handle_popup():
            analytics_popup = "//button[@class='_pendo-close-guide' and @aria-label='Close' and contains(@id, 'pendo-close-guide')]"
            try:
                popup_element = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, analytics_popup))
                )
                popup_element.click()
                print("Popup closed")
                time.sleep(2)
            except TimeoutException:
                print("No popup found") 

        for attempt in range(3):  # Try up to 3 times
            try:
                # Check for and close popup before interacting with dropdown
                handle_popup()

                # Wait for the dropdown to be clickable
                dropdown = WebDriverWait(self.driver, 20).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, sortby_dropdown_css))
                )
                
                # Use Select class to interact with the dropdown
                select = Select(dropdown)
                select.select_by_visible_text(oldestnewest_option_text)
                
                print("Selected 'Date (oldest-newest)' option")
                time.sleep(5)  # Wait for the page to update
                return  # Success, exit the function
                
            except StaleElementReferenceException:
                print("Stale element, retrying...")
                time.sleep(2)
                continue
                
            except (TimeoutException, NoSuchElementException):
                print(f"Attempt {attempt + 1}: Can't find sort-by dropdown, refreshing the page")
                self.driver.refresh()
                time.sleep(5)
                continue
                
            except ElementClickInterceptedException:
                print("Popup is in the way, attempting to close it")
                handle_popup()
                continue
                
            except ElementNotInteractableException:
                print("Element not interactable, attempting to close popup if present")
                handle_popup()
                continue
        
        print("Failed to sort by date after multiple attempts")


    def DownloadSetup(self):
        self.group_duplicates()
        self.sort_by_date()

    def get_result_count(self, index, max_attempts=3):
        for attempt in range(max_attempts):
            try:
                # Wait for the element to be present
                count_element = WebDriverWait(self.driver, self.timeout).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "#sidebar > div.search-controls > div.content-type-container.isBisNexisRedesign > ul > li.active"))
                )
                
                # Wait for the attribute to be non-empty
                WebDriverWait(self.driver, self.timeout).until(
                    lambda d: count_element.get_attribute("data-actualresultscount") != ""
                )
                
                result_count_element = count_element.get_attribute("data-actualresultscount")
                self.result_count = int(result_count_element)
                print(f"Result count for row {index} is {self.result_count}")

                if self.result_count < 1000:
                    # Update status data and return result
                    self.status_data.loc[index, 'basin_count'] = self.result_count
                    self.status_data.to_csv(self.status_file)
                    return self.result_count
                else:
                    # If result count is 1000 or more, check one more time
                    print("Result count is 1000 or more. Checking again...")
                    time.sleep(5)  # Wait a bit before checking again
                    
                    # Repeat the process to get the count again
                    count_element = WebDriverWait(self.driver, self.timeout).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "#sidebar > div.search-controls > div.content-type-container.isBisNexisRedesign > ul > li.active"))
                    )
                    result_count_element = count_element.get_attribute("data-actualresultscount")
                    self.result_count = int(result_count_element)
                    print(f"Second check result count for row {index} is {self.result_count}")
                    
                    if self.result_count < 1000:
                        # Update status data and return result
                        self.status_data.loc[index, 'basin_count'] = self.result_count
                        self.status_data.to_csv(self.status_file)
                        return self.result_count
                    else:
                        # If still 1000 or more, update status data and raise SkipRowException
                        self.status_data.loc[index, 'basin_count'] = self.result_count
                        self.status_data.loc[index, 'over_one_thousand'] = 1
                        self.status_data.to_csv(self.status_file)
                        raise SkipRowException(f"Result count is still {self.result_count} after second check.")

            except TypeError:
                print("Result count type error, waiting 20s for count to appear")
                time.sleep(20)
                continue

            except (TimeoutException, NoSuchElementException, StaleElementReferenceException) as e:
                print(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt < max_attempts - 1:
                    print("Refreshing page and retrying...")
                    self.driver.refresh()
                    time.sleep(5)  # Wait for page to reload
                else:
                    print("Max attempts reached. Could not retrieve result count.")
                    self.status_data.loc[index, 'basin_count'] = None
                    self.status_data.to_csv(self.status_file)
                    return None

            except ValueError as e:
                print(f"Error converting result count to integer: {str(e)}")
                self.status_data.loc[index, 'basin_count'] = None
                self.status_data.to_csv(self.status_file)
                return None

    # this portion deals with if the downloads exceed 1000 cumulatively
    # but I'm actually going to comment it out because idk it's working fine without tally
    '''
    def tally_result_count(self, index):
        current_count = self.get_result_count(index)
        self.result_tally += current_count
        time.sleep(3)
       
        if self.result_tally >= 1000:
            print("exceeded 1000 results downloaded, need to reset StoredLoginInformation")
            time.sleep(30)
            self.reset(index) # maybe??

        else:
            pass
            '''

    def DateFilter(self, index):
        self.set_date_range(index)
        try:
            self.get_result_count(index)
        except SkipRowException:
            raise
            #end the loop, go to next one
        #self.tally_result_count(index) #and this method is commented out at the moment
    
    def ExcelSegments(self):
        # we just want headline, summary, publication, date
        self.checkboxes = self.driver.find_elements(By.CSS_SELECTOR, 'input[type="checkbox"]')
        self.keep_checked_ids = ['HEA', 'PUB', 'PDT'] # headline, publication, published date
        # Scroll into view and uncheck each checkbox if it is checked
        for checkbox in self.checkboxes:
            id = checkbox.get_attribute('id')
            try:    
                if checkbox.is_selected() and id not in self.keep_checked_ids:
                    ActionChains(self.driver).move_to_element(checkbox).perform()
                    checkbox.click()
            except Exception as e:
                #print(f"Error processing checkboxes: {e}")
                #print(f"Error processing checkboxes") # terminal looks messy printing the whole error but I can keep this if necessary
                pass
        print("unchecked unnecessary columns")

    def get_filename(self, index):
        self.filename = f'ResultsList_{self.basin_code}_index{index}'
        return self.filename

    def DownloadOptions(self, index):
        self.open_download_options = "//button[@class='has_tooltip' and @data-action='downloadopt']"
        self._click_from_xpath(self.open_download_options)
        time.sleep(5)

        max_retries = 3
        for attempt in range(max_retries):
            try:
                # Wait for the element to be clickable
                results_list_option = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//input[@type='radio' and @id='ResultsListOnly']"))
                )
                results_list_option.click()
                print("choose resultslist download type")
                break  # Exit the loop if successful

            except (NoSuchElementException, TimeoutException):
                if attempt < max_retries - 1:
                    print(f"Attempt {attempt + 1} failed to open download window, retrying in 10 seconds")
                    time.sleep(10)
                    self._click_from_xpath(self.open_download_options)  # Try opening the download options again
                    time.sleep(5)
                else:
                    print("download limit banner appeared, need to reset login")
                    self.reset_needed = True
                    raise ResetRequiredException()


        #self.result_count = self.get_result_count(index)
        time.sleep(2)
        
        #self.result_list_field = '#SelectedRange' #css
        #self.result_list_field = '//*[@id="SelectedRange"]' #xpath copied
        #self.result_list_field = "//input[@type='text' and @id='SelectedRange']" #xpath my guess
        self.result_list_field = '/html/body/aside/form/div[4]/div[2]/div[1]/section/fieldset[1]/div[2]/div[1]/div/input' #full xpath, for some reason this works here
        try:
            self.download_result_string = f"1-{self.result_count}"
            print(f"Results {self.download_result_string}")
            time.sleep(2)
        except SingleResultException:
            self.download_result_string = self.result_count
            print(f"Only one result to download")
            time.sleep(2)

        # put in results count to download
        self._send_keys_from_xpath(self.result_list_field, self.download_result_string)
        
        self.filetype_excel_option = "//input[@type='radio' and @id='XLSX']"
        print("choose excel option")
        self._click_from_xpath(self.filetype_excel_option)
        time.sleep(2)

        # un-select unnecessary columns
        self.ExcelSegments()
        time.sleep(2)

        # rename file name
        self.filename_field = "//input[@type='text' and @id='FileName']"
        self._send_keys_from_xpath(self.filename_field, (Keys.COMMAND, "a"))
        self.filename = self.get_filename(index)
        print(f'changing filename to {self.filename}')
        self._send_keys_from_xpath(self.filename_field, self.filename)

        # click download
        self.download_button = "//button[@type='submit' and @class='button primary' and @data-action='download']"
        self._click_from_xpath(self.download_button)
        print(f"downloading {self.filename}")
        time.sleep(10)

    def move_file(self, index):
        self.filename = self.get_filename(index)
        self.default_download_path = self.download_folder_temp + self.filename + ".ZIP"
        self.geography_download_path = self.download_folder + self.filename + ".ZIP"

        max_attempts = 6
        attempts = 0

        while attempts < max_attempts:
            try:
                os.rename(self.default_download_path, self.geography_download_path)
                print(f"file in {self.basin_code} download folder")
                time.sleep(2)
                return
            
            except FileNotFoundError:
                time.sleep(10)
                attempts += 1

        try:
            self.driver.refresh() # maybe a coincidence but this did the trick last time?
            time.sleep(5)
            os.rename(self.default_download_path, self.geography_download_path)
            print(f"file in {self.basin_code} download folder")
            time.sleep(2)
         
        except FileNotFoundError:
            print(f"file {self.filename} stuck in default download folder")
            time.sleep(2)

        #would love to be able to create the folders... https://stackoverflow.com/questions/70235696/checking-folder-and-if-it-doesnt-exist-create-it

    def update_status(self, index):
        self.filename = self.get_filename(index)
        self.downloaded_file = self.filename + ".ZIP"
        #self.result_count = self.get_result_count(index)
        #filename_column
        #finished_column
        
        downloaded_file_path = os.path.join(self.download_folder, self.downloaded_file)
        file_exists = os.path.isfile(downloaded_file_path)

        if file_exists:
            self.status_data.loc[index, 'file_name'] = self.filename
            self.status_data.loc[index, 'finished'] = 1
            self.status_data.to_csv(self.status_file)
            print(f"status sheet row {index} updated")
        else:
            self.status_data.loc[index, 'finished'] = 0
            print(f"row {index} not marked as finished")

    def file_handling(self, index):
        self.move_file(index)
        self.update_status(index)

    def DownloadProcess(self, index):
        self.DateFilter(index)
        try:
            self.DownloadOptions(index) # i had these indented too... the logic was that these don't need to happen if reset
            self.file_handling(index)
        except SkipRowException:
            raise
        except ResetRequiredException:
            raise


    def main(self, index, basin_code):
        print(f"Download for {basin_code}")
        self.DownloadSetup()  # sort by date and group duplicates before date filtering
        
        row_index = 0
        while row_index < len(self.status_data):

            # Check if all rows are finished
            if (self.status_data['finished'] == 1).all():
                print(f"All rows for {basin_code} are downloaded!")
                #if self.download_type == "excel": # oh is download type not here yet?
                    #combine_excel = CombineResults(basin_code)
                    #combine_excel.combine()
                #else:
                   #pass
                break

            row = self.status_data.iloc[row_index]
            self.finished = row['finished']
            self.over_thousand = row['over_one_thousand']

            if self.finished != 1 and self.over_thousand != 1:
                try:
                    print(f"Proceeding to download basin {basin_code} row {row_index}")
                    time.sleep(1)
                    self.current_row = row
                    self.DownloadProcess(row_index)
                    row_index += 1  # Move to next row only if successful
                except SkipRowException:    
                    print(f"row {row_index} result count exceeds 1000, skipping to next row")
                    self.status_data.at[row_index, 'over_one_thousand'] = 1  # Update status
                    row_index += 1  # Move to next row
                except ResetRequiredException:
                    if self.reset_needed:
                        self.reset()
                        self.reset_needed = False
                        time.sleep(1)
                        print(f"Restarting download process at row {row_index}")
                        # Don't increment row_index, will retry the same row
            else:
                row_index += 1  # Move to next row if finished or over thousand
    

    def reset(self):
        sign_in_button = "//button[@id='SignInRegisterBisNexis']"
        self._click_from_xpath(sign_in_button)
        print("logging out")
        self.driver.delete_all_cookies()
        print("deleting cookies before logging in again")
        time.sleep(3)
        self.login._init_login()
        self.nlc._search_process()
        time.sleep(5)
        self.DownloadSetup()

#this calls it 
'''
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
'''
# and then to run it/check it 

# now this will run the iterrows method
#download.main(index=0, basin_code = basin_code)