#!/usr/bin/env python3

"""
The job of this script is to work out the correct automation of the 'Easy appy' process.
1. Sign in to LinkedIn.
2. Navigate to the provided job listing URL from Provided/job_link.txt
3. Find and click on all the buttons that are part of the 'Easy apply' process.
4. Once this is worked out, then the functionality of this script, will be implemented in linkedin.py.
5. The most consistant obstical in this project, has been, coding the correct xpath variable-value, for each button that must be clicked.
6. I've attempted to make this code as clean, and self-documenting as possible.
"""

import os
import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import config


def keep_browser_open() -> None:
    print("\nKeep Browser Open Method Running.")
    print(".. Close manually to exit.\n")
    while True:
        time.sleep(60)
        print("Browser still open...\n")

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
            self.driver.get('https://www.linkedin.com/login')
            self.driver.find_element(By.ID, "username").send_keys(config.email)
            self.driver.find_element(By.ID, "password").send_keys(config.password)
            time.sleep(8)

            sign_in_button_xpath = ("//button[contains(@class, 'btn__primary--large') and contains(@type, 'submit') "
                                    "and (contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', "
                                    "'abcdefghijklmnopqrstuvwxyz'), 'sign in') or contains(translate(., "
                                    "'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'signin'))]")
            sign_in_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, sign_in_button_xpath))
            )
            sign_in_button.click()

            if self.driver.current_url == 'https://www.linkedin.com/feed/':
                print('\nSign In Method Running....\n')
                self.navigate_to_job_listing()
                time.sleep(8)
                self.try_click_easy_apply_button()

                time.sleep(5)
                if self.driver.current_url.startswith('https://www.linkedin.com/jobs/search/'):
                    print('Job application form loaded successfully....')
                    self.click_next_button()
                else:
                    print('\nJob application form not loaded successfully...\n')

                while True:
                    time.sleep(60)
        except Exception as e:
            print(f"\nA sign in error occurred: {e}\n")

    def navigate_to_job_listing(self) -> None:
        print('\nNavigating to Job Listing Method Running ...\n')
        try:
            file_path = "/home/linux/Projects/Bots/LinkedIn_Apply/Provided/job_link.txt"
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"The file {file_path} does not exist.")

            with open(file_path, 'r') as file:
                job_link = file.readline().strip()

            self.driver.get(job_link)
            time.sleep(5)
            self.try_click_easy_apply_button()
        except Exception as e:
            print(f"\nError navigating to job listing: {e}")
            print(f"Current working directory: {os.getcwd()}\n")

    def try_click_easy_apply_button(self) -> None:
        print('Try Click Easy Apply Button Method Running...')
        try:
            xpath = "//button[contains(@class, 'jobs-apply-button') and contains(@aria-label, 'Easy Apply')]"
            button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
            time.sleep(2)
            self.click_button(button)
            print('Easy Apply button clicked successfully\n')
            time.sleep(5)
            self.click_next_button()
        except Exception as e:
            print(f"Error clicking Easy Apply button: {str(e)}\n")
            keep_browser_open()

    def click_button(self, button: WebElement) -> None:
        try:
            button.click()
        except:
            try:
                ActionChains(self.driver).move_to_element(button).click().perform()
            except:
                self.driver.execute_script("arguments[0].click();", button)

# Need to test this code, it is not clicking the Next button on the Upload resume page.
    def click_next_button(self) -> None:
        print('Upload resume')
        print('Click Next Button Method Running...\n')
        try:
            xpath = (r"//button[contains(@id, 'ember') and contains(@class, 'artdeco-button--primary') and (contains("
                     r"@aria-label, 'Next') or contains(@aria-label, 'Continue'))]")
            next_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            print("Attempting to click Next button, click_next_button...\n")
            next_button.click()
            print("Next button clicked using click_next_button ....\n")
            self.handle_work_authorization()
            time.sleep(5)
        except Exception as e:
            print(f"\nError clicking Next button: {str(e)}\n")
            keep_browser_open()

    def handle_work_authorization(self) -> None:
        try:
            # xpath_auth = //*[@id="ember424"]/div/div[2]/form/div/div/h3
            work_auth_element = self.driver.find_elements(By.XPATH, xpath)
            
            if work_auth_element:
                work_auth_element[0].click()
                print('Work authorization selected as No...\n')
                self.click_next_again_button()
            else:
                print('Work authorization question not found. Proceeding...\n')
                self.click_next_again_button()
        except Exception as e:
            print(f"Error handling work authorization: {str(e)}\n")
            keep_browser_open()

    def click_next_again_button(self) -> None:
        print('Click Next Again Button Method Running...\n')
        try:
            # Create xpath_two variable with the new XPath
            xpath_two = ("//button[contains(@id, 'ember') and @class='artdeco-button artdeco-button--2 "
                         "artdeco-button--primary ember-view' and @data-easy-apply-next-button and "
                         "@data-live-test-easy-apply-next-button and .//span[text()='Next']]")
    
            # Wait for the element to be clickable
            next_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, xpath_two))
            )
    
            print("Attempting to click Next button...\n")
            next_button.click()
            print('Next button clicked successfully...\n')
    
            # Continue with the rest of the process
            self.click_next_button()
            time.sleep(5)
        except Exception as e:
            print(f"\nError clicking Next button: {str(e)}\n")
            keep_browser_open()

    def click_review_button(self) -> None:
        print('\nClick Review_Button Method Running...\n')
        try:
            xpath = "//button[@aria-label='Review your application' and contains(@class, 'artdeco-button--primary')]"
            review_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            print("click_review_button,...\n")
            review_button.click()
            print('Review button clicked ...\n')
            self.submit_application()
            time.sleep(5)
        except Exception as e:
            print(f"\nThere was an Error clicking Review button: {str(e)}")
            print(f"Current URL: {self.driver.current_url}\n")
            print(f"Page source: {self.driver.page_source[:500]}...\n")
            keep_browser_open()

    def submit_application(self) -> None:
        print('\nSubmit Application Method Running...\n')
        try:
            xpath = r"//*[contains(@id, 'ember') and contains(@class, 'submit-button') and contains(@aria-label, 'Submit')]"
            submit_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            print("Attempting to click Submit button...\n")
            submit_button.click()
            print('Submit button clicked\n')
            self.click_done_button()
            time.sleep(5)
        except Exception as e:
            print(f"Error clicking Submit button: {str(e)}")
            print(f"Current URL: {self.driver.current_url}\n")
            print(f"Page source: {self.driver.page_source[:500]}...\n")
            keep_browser_open()

    def click_done_button(self) -> None:
        print('\nClick Done Button Method Running...\n')
        try:
            xpath = r"//*[contains(@id, 'ember') and contains(@class, 'done-button') and contains(@aria-label, 'Done')]"
            done_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            print("\nAttempting to click Done button...")
            done_button.click()
            print('Done button clicked...\n')
            time.sleep(5)
        except Exception as e:
            print(f"\nError clicking Done button: {str(e)}\n")
            print(f"Current URL: {self.driver.current_url}\n")
            print(f"Page source: {self.driver.page_source[:500]}...\n")

    def run_click_apply(self) -> None:
        print("\nrun_click_apply...\n")
        self.signin()
        keep_browser_open()

if __name__ == "__main__":
    linkedin_click_apply = LinkedInClickApply()
    linkedin_click_apply.run_click_apply()

