#!/usr/bin/env python3

"""
This is a backup of my working test_apply.py script..before any rerun or async changes were made

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
            from Bkup_files.signin_mod import FindSignInButton
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
                self.click_apply_button()
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
        except Exception as e:
            print(f"Error navigating to job listing: {e}")

    # Use ezapply_mod.py to click the 'Apply' button on the job listing page
    def click_apply_button(self):
        try:
            # import the ezapply_mod.py and implement its functionality.
            from Bkup_files.ezapply_mod import ApplyButtonClicker
            apply_button_clicker = ApplyButtonClicker(self.driver)
            apply_button_clicker.click_easy_apply_button_regular_xpath()  # Try to find the button using regular XPath.

            if not apply_button_clicker.click_easy_apply_button_full_xpath():
                print('Easy apply button not found.')

            if not apply_button_clicker.click_easy_apply_button_js_path():
                print('Easy apply button not found.')

            if not apply_button_clicker.click_easy_apply_button_element():
                print('Easy apply button not found.')

            print('Easy apply button clicked.')
        except Exception as e:
            print(f"Error clicking apply button: {e}")

    def run_click_apply(self):
        self.login_first()
        self.navigate_to_job_listing()
        self.click_apply_button()


if __name__ == "__main__":
    linkedin_click_apply = LinkedInClickApply()
    linkedin_click_apply.run_click_apply()
