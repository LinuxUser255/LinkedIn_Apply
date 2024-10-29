#from selenium import webdriver
#from selenium.webdriver.chrome.options import Options
#from selenium.webdriver.common.by import By
#from bs4 import BeautifulSoup
#import time
#import random
#import config
#import constants
#
#
#class FindSignInButton:
#    """
#    This is a moudule that is imported to other scripts. It's purpose:
#    Attempts to find the 'Sign in' button on the login page using all possible methods.
#    Each method tries to find the button and returns True if found, False otherwise.
#    """
#    def __init__(self, driver):
#        self.driver = driver
#        self.options = self.chrome_options
#
#    @property
#    def chrome_options(self):
#        """
#        This method is decorated with the @property, which means it can be accessed as an attribute.
#        Sets up Chrome options to ignore certificate errors and disable Chrome's automation controls.
#        """
#        options = Options()
#        options.add_argument("--window-size=800,600")
#        options.add_argument("--ignore-certificate-errors")
#        options.add_argument("--disable-blink-features")
#        options.add_argument("--disable-blink-features=AutomationControlled")
#        options.add_argument("--no-sandbox")
#        options.add_argument("--disable-dev-shm-usage")
#        return options
#
#    # The usual XPath expressions
#    def use_xpath(self):
#        print("Attempting Sign in using XPath from signin_mod.py ...")
#        try:
#            # use this XPath to find the 'Sign in' button: //*[@id="organic-div"]/form/div[4]/button
#            self.driver.find_element(By.XPATH, '//*[@id="organic-div"]/form/div[4]/button').click()
#            print("Sign in button clicked using XPath.")
#        except Exception as e:
#            print(f"Error using XPath: {str(e)}")
