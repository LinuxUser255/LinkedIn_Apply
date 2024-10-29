#!/usr/bin/env python3

"""
The job of this script is to
Sign in then LinkedIn
navigate to the provided job listing URL in Provided/job_link.txt
Click on the 'Apply' button on the job listing page.
"""
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import config
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re


class LinkedInClickApply:
    def __init__(self) -> None:
        options = Options()
        options.add_argument("--window-size=800,600")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--disable-blink-features")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=options)

    def signin(self) -> None:
        try:
            # Open LinkedIn login page.
            self.driver.get('https://www.linkedin.com/login')
            self.driver.find_element(By.ID, "username").send_keys(config.email)
            self.driver.find_element(By.ID, "password").send_keys(config.password)
            time.sleep(5)

            # More robust way to find and click the Sign in button
            sign_in_button_xpath = "//button[contains(@class, 'btn__primary--large') and contains(@type, 'submit') and (contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'sign in') or contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'signin'))]"

            sign_in_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, sign_in_button_xpath))
            )
            sign_in_button.click()

         # Check if the login was successful & keep browser window open until user closes it
            if self.driver.current_url == 'https://www.linkedin.com/feed/':
                print('Sign in successful from test_apply.py....')
               # If the sign in was successful, then navigate to the job listing page
                self.navigate_to_job_listing()

                # Apply to the job
                self.try_click_easy_apply_button()

                # Check if the job application form is loaded
                # The job application form is loaded when the URL changes to 'https://www.linkedin.com/jobs/' followed by the job ID
                # Wait for 5 seconds to ensure the job application form is loaded
                time.sleep(5)
                if self.driver.current_url.startswith('https://www.linkedin.com/jobs/'):
                    print('Job application form loaded successfully, using test_apply.py....')
                    self.click_next_button()  # Submit the job application form
                else:
                    print('Job application form not loaded successfully, using test_apply.py....')

                # stay logged in until user closes the browser
                while True:
                    time.sleep(60)  # Wait 60 seconds before checking again
        except Exception as e:
            print(f"A sign in error occurred on the test_apply.py script: {e}")

   # Retrieve the job link from Provided/job_link.txt file and navigate to that page
    def navigate_to_job_listing(self):
        print('Navigating to job listing, using test_appy.py ...')
        try:
            with open('Provided/job_link.txt', 'r') as file:
                job_link = file.readline().strip()
            self.driver.get(job_link)
            time.sleep(3)  # wait three seconds for the page to load before clicking the apply button.
            self.try_click_easy_apply_button()
        except Exception as e:
            print(f"Error navigating to job listing directly using test_apply.py: {e}")

    # Click the  ' Easy Apply' button
    def try_click_easy_apply_button(self):
        # Use a robust Xpath & regex to find and submit the "Easy Apply" button using this xpath //*[@id="ember305"]/span
        print('Trying to click Easy Apply button, using test_apply.py...')
        try:
            # Use a more flexible XPath that doesn't rely on specific IDs //*[@id="ember320"]
            xpath = r"//*[contains(@id, 'ember') and contains(@class, 'apply-button') and contains(@aria-label, 'Easy Apply')]"
            self.driver.find_elements(By.XPATH, xpath)
            print("Attempting to click Easy Apply button, using test_apply.py...")
            self.driver.find_element(By.XPATH, xpath).click()
            print('Easy Apply button clicked using  test_apply.py....')
            time.sleep(5)  # wait five seconds before checking if the job application form is loaded
        except Exception as e:
            print(f"Error clicking Easy Apply button: {str(e)}")
            # stay logged in until user closes the browser

    def click_next_button(self):
                print('Trying to click the Next button, using test_apply.py...')
        try:
            # Use a more precise XPath that targets the specific button element
            xpath = "//button[@aria-label='Continue to next step' and contains(@class, 'artdeco-button--primary') and @data-easy-apply-next-button]"

            # Wait for the element to be clickable
            wait = WebDriverWait(self.driver, 10)
            next_button = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))

            print("Attempting to click Next button, using test_apply.py...")
            next_button.click()
            print('Next button clicked using test_apply.py...')

            # Wait for the page to load after clicking
            time.sleep(5)
        except Exception as e:
            print(f"Error clicking Next button: {str(e)}")
            # Log more details about the current page
            print(f"Current URL: {self.driver.current_url}")
            print(f"Page source: {self.driver.page_source[:500]}...")  # Print first 500 characters of page source
            # Stay logged in until user closes the browser
            self.keep_browser_open()


    @staticmethod
    def keep_browser_open():
        print("Keeping browser open. This is being run directly from test_apply.py.. Close manually to exit.")
        while True:
            time.sleep(60)
            print("Browser still open...")


    def run_click_apply(self):
        self.signin()
        self.keep_browser_open()


if __name__ == "__main__":
    linkedin_click_apply = LinkedInClickApply()
    linkedin_click_apply.run_click_apply()
