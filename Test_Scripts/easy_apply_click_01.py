#!/usr/bin/env python3

"""
The purpose of this script is to test, and troubleshoot the bot's ability to 
click the Easy Apply button.
This process can be tricky if the XPATH & or Element values are incorrect

This versionn of the Easy Apply button click test uses the traditional
try-except blocks. The script loops over each method 
Xpath, Full Xpath, the Element, and finally Beautiful Soup
until the button is founc and clicked.

"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
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

        # Here we try four different ways find the easy apply button, and then click it.

    def xpath_find(self, driver):
        ###
        try:
            button = driver.find_element(By.XPATH, '//*[@id="ember58"]/svg')
            if button:
                button.click()
                print("Easy Apply Button Clicked!")
            else:
                print("Easy Apply Button Not Found!")
        except Exception as e:
            print("An error occurred while clicking the Easy Apply button: ", str(e))
        finally:
            # If the button is not found, remain logged in until the user manually closes the browser.
            time.sleep(60)


    def xpath_full(self, driver):
        try:
            button = driver.find_element(By.XPATH,
                                         '/html/body/div[4]/div[3]/div[4]/div/div/main/div/div[2]/div[2]/div/div[2]/div/div[1]/div/div[1]/div/div[1]/div/div[6]/div/div/div/button/svg')
            if button:
                button.click()
                print("Easy Apply Button Clicked!")
            else:
                print("Easy Apply Button Not Found!")
        except Exception as e:
            print("An error occurred while clicking the Easy Apply button: ", str(e))
        finally:
            # If the button is not found, remain logged in until the user manually closes the browser.
            time.sleep(60)

    def element_finder(self, driver):
        try:
            button = driver.find_element(By.CSS_SELECTOR,'svg[role="none"][aria-hidden="true"][class="artdeco-button__icon artdeco-button__icon--in-bug"]')
            if button:
                button.click()
                print("Easy Apply Button Clicked!")
            else:
                print("Easy Apply Button Not Found!")
        except Exception as e:
            print("An error occurred while clicking the Easy Apply button: ", str(e))
        finally:
            # If the button is not found, remain logged in until the user manually closes the browser.
            time.sleep(60)

    def bsoup_finder(self, driver):
        try:
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            button = soup.find('button', {'class': 'artdeco-button', 'data-control-name': 'apply'})
            if button:
                button.click()
                print("Easy Apply Button Clicked!")
            else:
                print("Easy Apply Button Not Found!")
        except Exception as e:
            print("An error occurred while clicking the Easy Apply button: ", str(e))
        finally:
            # If the button is not found, remain logged in until the user manually closes the browser.
            time.sleep(60)

    def click_ez_button(self):
        self.xpath_find(self.driver)
        self.xpath_full(self.driver)
        self.element_finder(self.driver)
        self.bsoup_finder(self.driver)


start = time.time()
while True:
    try:
        LinkedInClick().get_urls()
    except Exception as e:
        print("Error in main: " + str(e))
        end = time.time()
        print("---Took: " + str(round((time.time() - start) / 60)) + " minute(s).")
