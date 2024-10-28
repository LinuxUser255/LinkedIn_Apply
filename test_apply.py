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
from ezapply_mod import ApplyButtonClicker
import config


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

    def login_first(self) -> None:
        print('Logging in...')
        try:
            # Open LinkedIn login page.
            self.driver.get('https://www.linkedin.com/login')
            self.driver.find_element(By.ID, "username").send_keys(config.email)
            self.driver.find_element(By.ID, "password").send_keys(config.password)
            time.sleep(5)

            # Still unable to find and click the sign in button regardless of the method used.
            # Import the signin_mod.py and implement its functionality.
            from signin_mod import FindSignInButton
            find_sign_in_button = FindSignInButton(self.driver)
            find_sign_in_button.use_xpath()  # Try to find the button using XPath.

            if not find_sign_in_button.use_full_xpath():
                print('Sign in button not found.')

            if not find_sign_in_button.use_element_find():
                print('Sign in button not found.')

            if not find_sign_in_button.use_js_path():
                print('Sign in button not found.')

            if not find_sign_in_button.use_styles():
                print('Sign in button not found.')

            # Check if the login was successful & if so, then navigate to the job listing page.
            if self.driver.current_url == 'https://www.linkedin.com/feed/':
                print('Login successful')
                print('Now navigating to job listing...')
                self.navigate_to_job_listing()
           #     self.try_click_apply_button()
            else:
                print('Login failed')
                # if login fails, keep the browser window open for manual inspection.
                while True:
                    time.sleep(60)
                    print("Keeping browser open...")
        except Exception as e:
            print(f"Error logging in: {e}")

    # Retrieve the job link from Provided/job_link.txt file and navigate to that page
    def navigate_to_job_listing(self):
        print('Navigating to job listing...')
        try:
            with open('Provided/job_link.txt', 'r') as file:
                job_link = file.readline().strip()
            self.driver.get(job_link)
            time.sleep(3)  # wait three seconds for the page to load before clicking the apply button.
            self.try_click_apply_button()
        except Exception as e:
            print(f"Error navigating to job listing: {e}")

    # Using the ApplyButtonClicker class from ezapply_mod.py to click the 'Apply' button
    def try_click_apply_button(self):
        clicker = ApplyButtonClicker(self.driver)
        methods = [
            ('XPath', clicker.click_easy_apply_button_regular_xpath),
            ('Element selector', clicker.click_easy_apply_button_element)
        ]

        for method_name, method in methods:
            print(f'Trying {method_name}...')
            if method():
                return True
            print(f'Easy apply button not found using {method_name}.')

        return False

    @staticmethod
    def keep_browser_open():
        print("Keeping browser open. Close manually to exit.")
        while True:
            time.sleep(60)
            print("Browser still open...")


    def run_click_apply(self):
        self.login_first()
        self.keep_browser_open()


if __name__ == "__main__":
    linkedin_click_apply = LinkedInClickApply()
    linkedin_click_apply.run_click_apply()
