from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager

class WebDriverManager:
    def __init__(self):
        self.driver = None
        self.setup_options()
        self.setup_service()

    def setup_options(self):
        self.options = ChromeOptions()
        self.options.page_load_strategy = 'normal'
        self.options.add_argument("--start-maximized")
        self.options.add_argument("user-data-dir=/tmp/storedLoginInformation3")
        prefs = {'download.prompt_for_download': False}
        self.options.add_experimental_option('prefs', prefs)

    def setup_service(self):
        self.service = Service(ChromeDriverManager().install())

    def start_driver(self):
        if not self.driver:
            self.driver = webdriver.Chrome(service=self.service, options=self.options)
        return self.driver

    def stop_driver(self):
        if self.driver:
            self.driver.quit()
            self.driver = None