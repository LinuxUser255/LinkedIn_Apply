#!/usr/bin/env python3

import sys
import time
from selenium import webdriver
import config
from selenium.webdriver.chrome.options import Options as ChromeOptions, Options


print("This script will check if the bot can automatically log in Linkedin for you.")


def check_python():
    try:
        if sys.version:
            print("✅ Python is succesfully installed!")
        else:
            print("❌ Python is not installed please install Python first: https://www.python.org/downloads/")
    except Exception as e:
        print(e)


def check_pip():
    try:
        import pip
        print("✅ Pip is succesfully installed!")
    except ImportError:
        print("❌ Pip not present. Install pip: https://pip.pypa.io/en/stable/installation/")


def check_selenium():
    try:
        import selenium
        print("✅ Selenium is succesfully installed!")
    except ImportError:
        print("❌ Selenium not present. Install Selenium: https://pypi.org/project/selenium/")


def check_chrome():
    try:
        import subprocess
        output = subprocess.check_output(['firefox', '--version'])
        if output:
            print("✅ Chrome is succesfully installed!")
        else:
            print("❌ Chrome not present. Install firefox: https://www.mozilla.org/en-US/firefox/")

    except ImportError as e:
        print(e)


def check_selenium_linkedin():
    options = Options()

    options.add_argument("--start-half-window")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-blink-features")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("-profile")
    browser = webdriver.Chrome(options=options)

    try:
        # Log in to LinkedIn using the email and password specified in config.py.
        browser.get('https://www.linkedin.com/login')
        browser.find_element("id", "username").send_keys(config.email)
        browser.find_element("id", "password").send_keys(config.password)
        time.sleep(5)

        # Logging in
        browser.find_element("xpath", '//*[@id="organic-div"]/form/div[3]/button').click()

       # Check if the log in was successfull
        if browser.current_url == 'https://www.linkedin.com/feed/':
            print('�� Logged in successfully!')
            # stay logged in until user closes the browser
            while True:
                time.sleep(60)  # Wait 60 seconds before checking again
        else:
            print("❌ You were either not auto logged in, or the session ended prematurely.\n"
                  " check your credentials in config.py.")
    except Exception as e:
        print(e)


def check():
    check_python()
    check_pip()
    check_selenium()
    check_chrome()
    check_selenium_linkedin()


if __name__ == "__main__":
    check()
