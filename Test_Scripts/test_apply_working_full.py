#!/usr/bin/env python3

"""
The job of this script is to
Sign in then LinkedIn
navigate to the provided job listing URL in Provided/job_link.txt
Click on the
'Easy Apply', then follow the remaining steps in the easy Apply process.
"""
import time
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import config
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def keep_browser_open():
    print("Keeping browser open. This is being run directly from keep_browser_open.. Close manually to exit.")
    while True:
        time.sleep(60)
        print("Browser still open...")


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
        #self.run_click_apply()

    def signin(self) -> None:
        try:
            # Open LinkedIn login page.
            self.driver.get('https://www.linkedin.com/login')
            self.driver.find_element(By.ID, "username").send_keys(config.email)
            self.driver.find_element(By.ID, "password").send_keys(config.password)
            time.sleep(8)

            # More robust way to find and click the Sign in button
            sign_in_button_xpath = "//button[contains(@class, 'btn__primary--large') and contains(@type, 'submit') and (contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'sign in') or contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'signin'))]"

            sign_in_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, sign_in_button_xpath))
            )
            sign_in_button.click()

            # Check if the login was successful & keep browser window open until user closes it
            if self.driver.current_url == 'https://www.linkedin.com/feed/':
                print('def signin method....')
                # If the sign in was successful, then navigate to the job listing page
                self.navigate_to_job_listing()
                time.sleep(8)

                # Apply to the job
                self.try_click_easy_apply_button()

                time.sleep(5)
                if self.driver.current_url.startswith('https://www.linkedin.com/jobs/search/'):
                    print('Job application form loaded successfully....')
                    self.click_next_button()  # Submit the job application form
                else:
                    print('Job application form not loaded successfully...')

                # stay logged in until user closes the browser
                while True:
                    time.sleep(60)  # Wait 60 seconds before checking again
        except Exception as e:
            print(f"A sign in error occurred on the test_apply.py script: {e}")

    # Retrieve the job link from Provided/job_link.txt file and navigate to that page
    def navigate_to_job_listing(self):
        print('navigate_to_job_listing method  ...')
        try:
            # retrieve the URL from /home/linux/Projects/Bots/LinkedINBots/CurrentWorkingVersion/linkedin-application-bot/Provided/job_link.txt
            file_path = "/home/linux/Projects/Bots/LinkedINBots/CurrentWorkingVersion/linkedin-application-bot/Provided/job_link.txt"  # Replace with your actual file path if necessary.
            # Check if the file exists
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"The file {file_path} does not exist.")

            with open(file_path, 'r') as file:
                job_link = file.readline().strip()

            self.driver.get(job_link)
            time.sleep(5)  # wait five seconds for the page to load before clicking the apply button.
            self.try_click_easy_apply_button()

            # Check if the file exists
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"The file {file_path} does not exist.")

            with open(file_path, 'r') as file:
                job_link = file.readline().strip()

            self.driver.get(job_link)
            time.sleep(5)  # wait five seconds for the page to load before clicking the apply button.
            self.try_click_easy_apply_button()
        except Exception as e:
            print(f"Error navigating to job listing directly: {e}")
            # Log the current working directory for debugging
            print(f"Current working directory: {os.getcwd()}")

    # Click the  ' Easy Apply' button
    def try_click_easy_apply_button(self):
        # Use a robust Xpath & regex to find and submit the "Easy Apply" button using this xpath //*[@id="ember305"]/span
        print('try_click_easy_apply_button method...')
        try:
            # Use a more flexible XPath that doesn't rely on specific IDs //*[@id="ember320"]
            xpath = r"//*[contains(@id, 'ember') and contains(@class, 'apply-button') and contains(@aria-label, 'Easy Apply')]"
            self.driver.find_elements(By.XPATH, xpath)
            print("Attempting to click Easy Apply button, try_click_easy-apply_button...")
            self.driver.find_element(By.XPATH, xpath).click()
            print('Easy Apply button clicked using  try_click_easy_apply_buton ....')

            self.click_next_button()  # go to the next step
            time.sleep(5)  # wait five seconds before checking if the job application form is loaded
        except Exception as e:
            print(f"Error clicking Easy Apply button: {str(e)}")
            # stay logged in until user closes the browser

    def click_next_button(self):
        print('click_next_button method...')
        try:
            # 1. Search for the element containing the text 'Next'
            # 2. Use a flexible XPath that matches the structure
            # 3. Use a regular expression to allow any number for the 'id' value
            # 4. Click the 'Next' button when found
            xpath = "//button[contains(@class, 'artdeco-button')]/span[text()='Next']/parent::button"

            print("Attempting to click Next button...")
            wait = WebDriverWait(self.driver, 10)
            next_button = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            next_button.click()
            print('Next button clicked...')

            self.click_review_button()  # review the job application form
            # Wait for the page to load after clicking
            time.sleep(5)
        except Exception as e:
            print(f"Error clicking Next button: {str(e)}")
            # Log more details about the current page
            print(f"Current URL: {self.driver.current_url}")
            print(f"Page source: {self.driver.page_source[:500]}...")  # Print first 500 characters of page source
            self.click_review_button()
            # Stay logged in until user closes the browser
            keep_browser_open()



# Code execution seems to be stuck here
    def click_review_button(self):
        print('click_review_button...')
        try:
            # Use a precise XPath that targets the specific Review button element
            xpath = "//button[@aria-label='Review your application' and contains(@class, 'artdeco-button--primary')]"

            # Wait for the element to be clickable
            wait = WebDriverWait(self.driver, 10)
            review_button = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))

            print("click_review_button,...")
            review_button.click()
            print('Review button clicked ...')

            # Wait for the page to load after clicking
            self.submit_application()  # submit the job application form
            time.sleep(5)
        except Exception as e:
            print(f"Error clicking Review button: {str(e)}")
            # Log more details about the current page
            print(f"Current URL: {self.driver.current_url}")
            print(f"Page source: {self.driver.page_source[:500]}...")  # Print first 500 characters of page source
            # Stay logged in until user closes the browser
            keep_browser_open()


    def submit_application(self):
        print('submit_application method...')
        try:
            #  Use a robust Xpath & regex to find and submit the "Easy Apply" button using this xpath: //*[@id="ember458"]/span
            xpath = r"//*[contains(@id, 'ember') and contains(@class, 'submit-button') and contains(@aria-label, 'Submit')]"

            # Wait for the element to be clickable
            wait = WebDriverWait(self.driver, 10)
            submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))

            # Wait for the element to be clickable
            wait = WebDriverWait(self.driver, 10)
            submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))

            print("Attempting to click Submit button...")
            submit_button.click()
            print('Submit button clicked')
            self.click_done_button()  # go to the next step

            # Wait for the page to load after clicking
            time.sleep(5)
        except Exception as e:
            print(f"Error clicking Submit button: {str(e)}")
            # Log more details about the current page
            print(f"Current URL: {self.driver.current_url}")
            print(f"Page source: {self.driver.page_source[:500]}...")  # Print first 500 characters of page source

            
    def click_done_button(self):
        print('click_done_button method...')
        try:
            # Use a robust Xpath & regex to find and submit the "Done" button
            xpath = r"//*[contains(@id, 'ember') and contains(@class, 'done-button') and contains(@aria-label, 'Done')]"

            # Wait for the element to be clickable
            wait = WebDriverWait(self.driver, 10)
            done_button = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))

            print("Attempting to click Done button...")
            done_button.click()
            print('Done button clicked...')

            # Wait for the page to load after clicking
            time.sleep(5)
        except Exception as e:
            print(f"Error clicking Done button: {str(e)}")
            # Log more details about the current page
            print(f"Current URL: {self.driver.current_url}")
            print(f"Page source: {self.driver.page_source[:500]}...")  # Print first 500 characters of page source



    def run_click_apply(self):
        print("run_click_apply...")
        self.signin()
        keep_browser_open()


if __name__ == "__main__":
    linkedin_click_apply = LinkedInClickApply()
    linkedin_click_apply.run_click_apply()
