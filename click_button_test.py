#!/usr/bin/env python3

"""
The purpose of this script is for troubleshooting the 
click Easy Apply button.

It is similar to the primary one, linkedin.py.
However, this one is limitted to:

1. Logging in, 
2. Navigating to a user-supplied job url, 
3. and attempts to click the Easy Apply button.

If the script is unable to click the apply button, it will continue to run in an infinite loop
until you manually stop it.

I programmed this feature into it, for debugging purposes, and 
to prevent auto closing, and logging in again with each iteration.

That can cause problems with logging into your account. And force you to complete captchas.
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import random
import config
import constants


class LinkedInClick:
    def __init__(self) -> None:
        options = Options()
        options.add_argument("--window-size=1024,768")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-blink-features")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("-profile")
        self.driver = webdriver.Chrome(options=options)
        self.login()

    def login(self) -> None:
        try:
            self.driver.get('https://www.linkedin.com/login')
            self.driver.find_element(By.ID, "username").send_keys(config.email)
            self.driver.find_element(By.ID, "password").send_keys(config.password)
            time.sleep(5)
            self.driver.find_element(By.XPATH, '//*[@id="organic-div"]/form/div[3]/button').click()
            if self.driver.current_url == 'https://www.linkedin.com/feed/':
                print('✅ First Login Block: Logged in successful!')
                # stay logged in until user closes the browser, and continue to run the bot
                while True:
                    try:
                        self.get_urls()
                        # persist login session in same browser window
                        self.click_ez_button()
                    except Exception as e:
                        print("An error occurred Couldn't keep original session open: ", str(e))
                    finally:
                        time.sleep(60)
            else:
                print("❌ oops, check for errors in config.py.")
        except:
            pass

    def get_urls(self):
        try:
            with open('Provided/job_link.txt', 'r') as file:
                urls = file.readlines()
                for url in urls:
                    self.driver.get(url.strip())
                    time.sleep(random.uniform(5, constants.botSpeed))
                    self.click_ez_button()
        except:
            pass

    def click_ez_button(self):
        try:
            button = self.driver.find_element(By.XPATH,
                                              '//button[contains(@class, "artdeco-button__text") and.//span[contains(text(), "Easy Apply")]]')
            if button is not None:
                button.click()
                time.sleep(random.uniform(5, constants.botSpeed))
                print("Easy Apply Button Clicked!")
            else:
                print("Easy Apply Button Not Found!")
        except Exception as e:
            print("An error occurred while clicking the Easy Apply button: ", str(e))
        finally:
            # If the button is not found, remain logged in until the user manually closes the browser.
            time.sleep(60)


start = time.time()
while True:
    try:
        LinkedInClick().get_urls()
    except Exception as e:
        print("Error in main: " + str(e))
        end = time.time()
        print("---Took: " + str(round((time.time() - start) / 60)) + " minute(s).")
