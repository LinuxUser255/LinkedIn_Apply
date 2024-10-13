#!/usr/bin/env python3

import sys
import time
from selenium import webdriver
import config
from selenium.webdriver.chrome.options import Options as ChromeOptions, Options
from Finding_Elements import signin_mod


def check_selenium_linkedin():
    options = Options()
    options.add_argument("--window-size=1024,768")
    options.add_argument("--start-half-window")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-blink-features")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("-profile")
    browser = webdriver.Chrome(options=options)

    try:
        # Open LinkedIn login page.
        browser.get('https://www.linkedin.com/login')
        browser.find_element("id", "username").send_keys(config.email)
        browser.find_element("id", "password").send_keys(config.password)
        time.sleep(5)

        # Import the sign in fuctionality from signin_mod.py
        # Located in LinkedIn_Apply/Finding_Elements/signin_mod.py
        from signin_mod import Find_Sign_In_Button
        find_sign_in_button = Find_Sign_In_Button(browser)
        find_sign_in_button.use_xpath()  # Try to find the button using XPath.

        # If the button is not found, try with full XPath.
        if not find_sign_in_button.use_full_xpath():
            print('Sign in button not found.')

        if not find_sign_in_button.use_element_find():
            print('Sign in button not found.')

        if not find_sign_in_button.soup_find():
            print('Sign in button not found.')

        if not find_sign_in_button.use_js_path():
            print('Sign in button not found.')

        if not find_sign_in_button.use_styles():
            print('Sign in button not found.')

        # Wait until the login is successful.
        # The current_url of the browser will be 'https://www.linkedin.com/feed/' when login is successful.
        # If not, it means the login failed.
        # Keep checking every 60 seconds until the login is successful.
        # Note: This will not work if the login page changes. You might need to modify the code to handle that case.
        # Also, this script will keep the browser window open until user closes it.

        # Check if the login was successful & keep browser window open until user closes it.
        if browser.current_url == 'https://www.linkedin.com/feed/':
            print('Login successful')
            # stay logged in until user closes the browser
            while True:
                time.sleep(60)  # Wait 60 seconds before checking again
        else:
            print("You were either not auto logged in, or the session ended prematurely.\n"
                  "Check your credentials in config.py.")
    except Exception as e:
        print(e)


def check():
    check_selenium_linkedin()


if __name__ == "__main__":
    check()
