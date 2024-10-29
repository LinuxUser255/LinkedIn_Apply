"""
The job of this module is to use the xpath value to find
and click the easy apply button on a LinkedIn job listing page.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re


# Still unable to find and click the sign in button regardless of the method used.

class ApplyButtonClicker:
    def __init__(self, driver):
        self.click_easy_apply_button_element = None
        self.driver = driver

    # method to find and click the easy apply button using the Regular Xpath
    def click_easy_apply_button_regular_xpath(self):
        print('Using regular XPath...')
        try:
            # Use a more flexible XPath that doesn't rely on specific IDs
            xpath = "//button[contains(@class, 'jobs-apply-button') and contains(@aria-label, 'Easy Apply')]"
            wait = WebDriverWait(self.driver, 10)
            easy_apply_button = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))

            if easy_apply_button:
                easy_apply_button.click()
                print('Easy apply button clicked using regular XPath.')
            else:
                print('Easy apply button not found using regular XPath.')
        except Exception as e:
            print(f'Error clicking easy apply button using regular XPath: {e}')

    def submit_contact_info(self):
        # Use a robust Xpath & regex to find and submit the "Next" button using this xpath //*[@id="ember305"]/span
        print('Trying to click Next button...')
        try:
            xpath = "//button[contains(@class, 'next-button') and contains(@aria-label, 'Next')]"
            wait = WebDriverWait(self.driver, 10)
            next_button = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))

            if next_button:
                next_button.click()
                print('Next button clicked.')
            else:
                print('Next button not found.')
        except Exception as e:
            print(f'Error clicking Next button: {e}')

