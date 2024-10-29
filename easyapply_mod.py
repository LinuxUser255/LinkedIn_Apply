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


    def click_easy_apply_button_element(self):
        print('Trying Element with regex...')
        try:
            # Use WebDriverWait to wait for the element to be present
            wait = WebDriverWait(self.driver, 10)  # Wait up to 10 seconds
            easy_apply_button = wait.until(
                EC.presence_of_element_located((By.XPATH,
                                                "//button[contains(@class, '') and .//span[contains(text(), 'Easy Apply')]]"))
            )
            easy_apply_button = self.driver .find_element(By.XPATH, "//div[@class='card-layout']")
            if easy_apply_button:
                easy_apply_button.click()
                print('Easy apply button clicked using Element Selector with regex.')
            else:
                print('Easy apply button Not found using Element Selector with regex.')
        except Exception as e:
            print(f'Error clicking easy apply button using Element selector with regex: {e}')
