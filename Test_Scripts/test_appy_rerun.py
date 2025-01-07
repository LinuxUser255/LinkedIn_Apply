#!/usr/bin/env python3

"""
This is a modified version of test_apply.py, that enables you to make changes to the code
Re-run the augmented code without having to start allover with the login part
The purpose it to avoid LinkedIn captias triggerd by multiple logins

Log in once and then allow you to edit and re-run parts of the code without logging in again. 
Here's how it works

1. Separate the login process from the main application logic.
2. Use a persistent browser session.
3. Implement a mechanism to reload and re-run specific parts of your code.

"""

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config
import importlib

class LinkedInClickApply:
    def __init__(self):
        self.driver = None

    def initialize_driver(self):
        if self.driver is None:
            options = Options()
            options.add_argument("--window-size=800,600")
            options.add_argument("--ignore-certificate-errors")
            options.add_argument("--disable-blink-features")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            self.driver = webdriver.Chrome(options=options)

    def signin(self):
        self.initialize_driver()
        self.driver.get('https://www.linkedin.com/login')
        self.driver.find_element(By.ID, "username").send_keys(config.email)
        self.driver.find_element(By.ID, "password").send_keys(config.password)
        time.sleep(8)

        sign_in_button_xpath = "//button[contains(@class, 'btn__primary--large') and contains(@type, 'submit') and (contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'sign in') or contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'signin'))]"

        sign_in_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, sign_in_button_xpath))
        )
        sign_in_button.click()

        if self.driver.current_url == 'https://www.linkedin.com/feed/':
            print('Sign in successful from test_apply.py....')
            return True
        return False

    def run_application_logic(self):
        # This method will be reloaded and re-run
        print("Running application logic...")
        # Add your application logic here
        # For example:
        # self.navigate_to_job_listing()
        # self.try_click_easy_apply_button()

    def reload_and_run(self):
        importlib.reload(importlib.import_module(__name__))
        self.run_application_logic()

def main():
    linkedin_bot = LinkedInClickApply()
    
    # Sign in only once
    if linkedin_bot.signin():
        while True:
            command = input("Enter 'r' to reload and run, or 'q' to quit: ")
            if command.lower() == 'r':
                linkedin_bot.reload_and_run()
            elif command.lower() == 'q':
                break
    
    if linkedin_bot.driver:
        linkedin_bot.driver.quit()

if __name__ == "__main__":
    main()
