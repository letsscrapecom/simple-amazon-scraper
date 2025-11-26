from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from config import Config

class DriverManager:
    def __init__(self):
        self.driver = None
        self.wait = None
    
    def connect(self):
        options = Options()
        options.add_experimental_option("debuggerAddress", f"localhost:{Config.CHROME_DEBUG_PORT}")
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, Config.SELENIUM_TIMEOUT)
        print(f"Connected to Chrome on port {Config.CHROME_DEBUG_PORT}")
        return self.driver
    
    def get_driver(self):
        if not self.driver:
            self.connect()
        return self.driver
    
    def close(self):
        if self.driver:
            self.driver.quit()
            self.driver = None

driver_manager = DriverManager()
