#!/usr/bin/env python3

"""
The job of this script is to work as a kinda diagnostic script for troubleshooting errors etc..
First: it signs in then LinkedIn
Second: Navigates to the provided job listing URL in Provided/job_link.txt
Third: Click on the 'Easy Apply', then follows the remaining steps in the easy Apply process.
The code self documents via each method, (function)
"""
import time
import os

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import config
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def keep_browser_open():
    print()
    print("Keep Browser Open Method Running.")
    print()
    print(".. Close manually to exit.")
    print()
    while True:
        time.sleep(60)
        print("Browser still open...")
        print()


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

    # First method
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
                print()
                print('Sign In Method Running....')
                print()
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
                    print()
                    print('Job application form not loaded successfully...')
                    print()

                # stay logged in until user closes the browser
                while True:
                    time.sleep(60)  # Wait 60 seconds before checking again
        except Exception as e:
            print()
            print(f"A sign in error occurred on the test_apply.py script: {e}")
            print()

    # Second method
    # Retrieve the job link from Provided/job_link.txt file and navigate to that page
    def navigate_to_job_listing(self):
        print()
        print('Navigating to Job Listing Method Running ...')
        print()
        try:
            # Url located here:  /home/linux/Projects/Bots/LinkedIn_Apply/Provided/job_link.txt
            file_path = "/home/linux/Projects/Bots/LinkedIn_Apply/Provided/job_link.txt"
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
            print()
            print(f"Error navigating to job listing directly: {e}")
            # Log the current working directory for debugging
            print(f"Current working directory: {os.getcwd()}")
            print()

    # Third method try_click_easy_appy
    # Click the  ' Easy Apply' button
    def try_click_easy_apply_button(self):
        print('Try Click Easy Apply Button Method Running...')
        try:
            xpath = "//button[contains(@class, 'jobs-apply-button') and contains(@aria-label, 'Easy Apply')]"

            # Wait for the button to be present
            wait = WebDriverWait(self.driver, 10)
            button = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))

            # Scroll the button into view
            self.driver.execute_script("arguments[0].scrollIntoView(true);", button)

            # Wait a bit for any animations to complete
            time.sleep(2)

            # Try to click using different methods
            try:
                button.click()
            except:
                try:
                    ActionChains(self.driver).move_to_element(button).click().perform()
                except:
                    self.driver.execute_script("arguments[0].click();", button)

            print('Easy Apply button clicked successfully')

            # Wait for the next step to load
            time.sleep(5)
            self.click_next_button()
        except Exception as e:
            print(f"Error clicking Easy Apply button: {str(e)}")
            keep_browser_open()
            
    # CLICK NEXT (first time)
    # Fourth method click_next_button
    def click_next_button(self):
        print()
        print('Upload resume')
        print('Click Next Button Method Running...')
        print()
        try:
            xpath = r"//button[contains(@id, 'ember') and contains(@class, 'artdeco-button--primary') and (contains(@aria-label, 'Next') or contains(@aria-label, 'Continue'))]"
            wait = WebDriverWait(self.driver, 10)
            next_button = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))

            print("Attempting to click Next button, click_next_button...")
            next_button.click()
            print('Next button clicked using click_next_button ....')

            # If this was successful, then go to the Work authorization method
            self.handle_work_authorization()
            time.sleep(5)  # wait five seconds for the page to load before clicking the apply button.
        except Exception as e:
            print()
            print(f"Error clicking Next button: {str(e)}")
            print()
            keep_browser_open()

    # WORK AUTHORIZATION: Yes, or No selection.
    def handle_work_authorization(self):
        try:
            xpath = r"//*[contains(@id, 'radio-button-form-component-formElement-urn-li-jobs-applyformcommon-easyApplyFormElement-4129161503-8437332817-multipleChoice') and contains(@for, 'urn:li:fsd_formElement:urn:li:jobs_applyformcommon_easyApplyFormElement:(4129161503,8437332817,multipleChoice)-1')]"
            self.driver.find_elements(By.XPATH, xpath)

            # If Work authorization is selected as No, then click the Review button
            self.driver.find_element(By.XPATH, xpath).click()
            print('Work authorization selected as No...')

            # Call the method to click the Review button
            self.click_next_again_button()
        except Exception as e:
            print(f"Error handling work authorization: {str(e)}")
            keep_browser_open()

     # CLICK NEXT AGAIN (second time)
    def click_next_again_button(self):
        print('Click Next Again Button Method Running...')
        try:
            xpath = r"//button[contains(@id, 'ember') and contains(@class, 'artdeco-button--primary') and (contains(@aria-label, 'Next') or contains(@aria-label, 'Continue'))]"
            wait = WebDriverWait(self.driver, 10)
            next_button = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))

            print("Attempting to click Next button, click_next_button...")
            next_button.click()
            print('Next button clicked using click_next_button ....')

            # If this was successful, then go to the Work authorization method
            self.click_next_button()
            time.sleep(5)  # wait five seconds for the page to load before clicking the apply button.
        except Exception as e:
            print()
            print(f"Error clicking Next button: {str(e)}")
            print()
            keep_browser_open()

    # CLICK REVIEW
    def click_review_button(self):
        print()
        print('Click Review_Button Method Running...')
        print()
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
            print()
            print(f"There was an Error clicking Review button: {str(e)}")
            # Log more details about the current page
            print(f"Current URL: {self.driver.current_url}")
            print()
            print(f"Page source: {self.driver.page_source[:500]}...")  # Print first 500 characters of page source
            print()
            # Stay logged in until user closes the browser
            keep_browser_open()

    def submit_application(self):
        print()
        print('Submit Application Method Running...')
        print()
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
            keep_browser_open()

    def click_done_button(self):
        print()
        print('Click Done Button Method Running...')
        print()
        try:
            # Use a robust Xpath & regex to find and submit the "Done" button
            xpath = r"//*[contains(@id, 'ember') and contains(@class, 'done-button') and contains(@aria-label, 'Done')]"

            # Wait for the element to be clickable
            wait = WebDriverWait(self.driver, 10)
            done_button = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))

            print()
            print()
            print("Attempting to click Done button...")
            done_button.click()
            print('Done button clicked...')
            print()

            # Wait for the page to load after clicking
            time.sleep(5)
        except Exception as e:
            print()
            print(f"Error clicking Done button: {str(e)}")
            # Log more details about the current page
            print(f"Current URL: {self.driver.current_url}")
            print(f"Page source: {self.driver.page_source[:500]}...")  # Print first 500 characters of page source
            print()

    # The Main method to run the bot
    def run_click_apply(self):
        print()
        print("run_click_apply...")
        print()
        self.signin()
        keep_browser_open()


if __name__ == "__main__":
    linkedin_click_apply = LinkedInClickApply()
    linkedin_click_apply.run_click_apply()

 
