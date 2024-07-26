from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class NoLinkClass:
    def __init__(self, driver: webdriver, search_term, timeout=20, url=None):
        self.driver = driver
        self.url = url
        self.timeout = timeout
        self.search_term = search_term

        # search keys
        self.box_1_keys = '*water* OR river* OR lake OR dam OR stream OR tributary OR diversion OR irrigation OR pollution OR water quality OR flood! OR drought! OR channel OR canal OR hydroelect! OR reservoir OR groundwater OR aquifer OR drought OR recharge OR "water table" OR "bore hole"'
        self.box_2_keys = 'treaty OR agree! OR negotiat! OR resolution OR commission OR secretariat OR joint management OR basin management OR peace OR accord OR "peace accord" OR settle! OR cooperat! OR collaborat! OR disput! OR conflict! OR disagree! OR sanction! OR war OR troops OR "letter of protest" OR hostility OR "shots fired" OR boycott OR protest! OR appeal OR intent OR reject OR threat! OR force OR coerce OR assault OR fight OR demand OR disapprove OR diploma! OR statement OR memorandum'
        self.box_3_keys = search_term
        self.box_4_keys = 'ocean OR navigat! OR nuclear OR "water cannon" OR "light water reactor" OR "mineral water" OR "hold water" OR "cold water" OR "hot water" OR "water canister" OR "water tight" OR " water down" OR "flood of refugees" OR Rivera OR Suez OR Panama OR oil OR drugs OR "three gorges" OR waterski OR watermelon OR dishwater OR waterproof OR "water resistant" OR "water bath" '

    def get_search_term(self):
        print(f"Search Term: {self.search_term}")

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
        news_button = 'body > main > div > ln-navigation > navigation > div.global-nav.light.margin-bottom-30 > div.zones.pagewrapper.product-switcher-navigation.pagewrapper-nexis > nexissearchtabmenu > div > tabmenucomponent > div > div > ul > li:nth-child(3) > button'
        self._click_from_css(news_button) # click to search in News
        news_advancedsearch_button = '#wbbhkkk > ul > li:nth-child(1) > button'
        self._click_from_css(news_advancedsearch_button) # click advanced search
        self.driver.execute_script("window.scrollTo(0,102)")
        print(f"Initializing search with driver: {self.driver} and search term: {self.search_term}")

    def _search_box(self):
        self.search_box = '#searchTerms'
        self.search_string = 'hlead(' + self.box_1_keys + ') and hlead(' + self.box_2_keys + ') and hlead(' + self.box_3_keys + ') and not hlead(' + self.box_4_keys + ')'
        self._send_keys_from_css(self.search_box, self.search_string)
    
# methods below are obsolete due to July 2024 Nexis Uni update
    def _box_1(self):
        self._send_keys_from_css(".searchterm-input-box:nth-child(1)", self.box_1_keys) 
        self._click_from_css(".search-input-row-outline > .dropdown:nth-child(3) > .icon")
        self._click_from_css(".expanded .dropdown-option:nth-child(7) > .option-text")

    def _box_2(self):
        self._send_keys_from_css(".search-input-row:nth-child(2) .searchterm-input-box", self.box_2_keys)
        self._click_from_css(".dropdown:nth-child(5) > .icon")
        self._click_from_css(".expanded .dropdown-option:nth-child(7) > .option-description")

    def _box_3(self):
        self._send_keys_from_css(".search-input-row:nth-child(3) .searchterm-input-box", self.box_3_keys)
        self._click_from_css(".search-input-row:nth-child(3) .dropdown:nth-child(5) > .icon")
        self._click_from_css(".expanded .dropdown-option:nth-child(7) > .option-description")

    def _box_4(self):
        self._click_from_css(".search-input-row:nth-child(4) .dropdown:nth-child(1) > .icon")
        self._click_from_css(".expanded .dropdown-option:nth-child(5) > .option-description")
        self._send_keys_from_css(".search-input-row:nth-child(4) .searchterm-input-box", self.box_4_keys)
        self._click_from_css(".search-input-row:nth-child(4) .dropdown:nth-child(5) > .icon")
        self._click_from_css(".expanded .dropdown-option:nth-child(7) > .option-description")

    #click search
    def complete_search(self):
        search_button_old = ".search" # this is what it used to be
        search_button = '#mainSearch'
        self._click_from_css(search_button)
        

#how to instantiate in main 
'''
from classes.NoLinkClass import NoLinkClass
nlc = NoLinkClass(driver, search_term)

nlc._init_search()
nlc._search_box()
nlc.complete_search()
'''


# plop the below in main code to get search term (formerly box 3 keys), 
'''
import pandas as pd
basin_code = 'tigr' # main should already refer to this

df = pd.read_excel('TrackingSheet_basinterms.xlsx') 
# this sheet is in my class folder, need full file path otherwise
# it's the tracking sheet, but needs headers removed, terms in default (or only) tab
row = df[df['BCODE'] == basin_code.upper()]

search_term = row['Basin_Specific_Terms'].values[0] # maybe the column will be renamed
print(search_term) 
'''
#actually this could all be here if I can figure out how to like...
'''
import pandas as pd # at top of this class
# because maybe search_term doesn't need to be passed in?
    
    def get_search_term(self): #but basin_code would need to be pulled in
        print(f"Search Term: {self.search_term}")

        # this all extra indented because it's underneath NoLinkClass
'''