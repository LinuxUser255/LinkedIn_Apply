#!/usr/local/bin/python3.13

"""
This script is to independently test the login capability
And to isolate for trouble-shooting if needed
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import config

# This script is working as of 10/28/24

class LoginClicker:
    def __init__(self) -> None:
        """Instantiates the Chrome webdriver with the specified options."""
        options = Options()
        options.add_argument("--window-size=1024,768")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-blink-features")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("-profile")
        self.driver = webdriver.Chrome(options=options)
        # self.login()

    def login_test(self) -> None:
        try:
            # Open LinkedIn login page.
            self.driver.get('https://www.linkedin.com/login')
            self.driver.find_element(By.ID, "username").send_keys(config.email)
            self.driver.find_element(By.ID, "password").send_keys(config.password)
            time.sleep(5)

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

            # Check if the login was successful & keep browser window open until user closes it
            if self.driver.current_url == 'https://www.linkedin.com/feed/':
                print('Login successful')
                # stay logged in until user closes the browser
                while True:
                    time.sleep(60)  # Wait 60 seconds before checking again
        except Exception as e:
            print(f"An error occurred: {e}")

    def run_test(self):
        self.login_test()


if __name__ == "__main__":
    login_clicker = LoginClicker()
    login_clicker.run_test()
