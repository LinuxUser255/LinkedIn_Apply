#!/usr/bin/env python3

import os
import sys
import time
from selenium import webdriver

import config
from config import email, password
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions, Options
from dotenv import load_dotenv


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

    #options.add_argument("--start-maximized")
    # do not maximize browser window
    options.add_argument("--start-half-window")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-blink-features")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("-profile")
    # options.headless = True..should I use this?
    browser = webdriver.Chrome(options=options)

    browser.get('https://www.linkedin.com/feed/?trk=guest_homepage-basic_nav-header-signin')
    browser.find_element("id", "username").send_keys(config.email)
    browser.find_element("id", "password").send_keys(config.password)
    time.sleep(5)

    browser.find_element("xpath", '//*[@id="organic-div"]/form/div[3]/button').click()
    browser = browser.find_element(by="class name", value="btn__primary--large from__button--floating")
    # selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element:
    # {"method":"css selector","selector":".btn__primary--large from__button--floating"}
    # need to find this: <button class="btn__primary--large from__button--floating" data-litms-control-urn="login-submit" aria-label="Sign in" type="submit">
    #               Sign in
    #           </button>
    browser.click()

    try:
        browser.url('https://www.linkedin.com/')
        time.sleep(3)
        if "homepage" in browser.url:
            print('✅ Successfully you are logged in to Linkedin, you can now run main bot script!')
        else:
            print('❌ You are not automatically logged in, check your credentials in config.py.')
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

