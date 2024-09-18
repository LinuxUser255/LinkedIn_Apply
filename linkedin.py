#!/usr/bin/env python3

import math
import os
import random
from typing import Union
from selenium.webdriver.remote.webelement import WebElement
import constants
from selenium.webdriver.common.by import By
import utils
import time
from selenium import webdriver
import config
from selenium.webdriver.chrome.options import Options as ChromeOptions, Options


class LinkedIn:
    def __init__(self):
        self.driver = ""
        self.login()

    def login(self) -> None:
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
            time.sleep(5)  # Wait 5 seconds for the page to load completely before logging in.

            browser.find_element("xpath", '//*[@id="organic-div"]/form/div[3]/button').click()
            print('Checking if logged in...')
            time.sleep(5)

            # Check if the log in was successfull
            if browser.current_url == 'https://www.linkedin.com/feed/':

                # ! Code hangs here.
                # Need to make it continue through all the methods
                print('�� Logged in successfully!')
                # stay logged in until user closes the browser
                while True:
                    time.sleep(60)  # Wait 60 seconds before checking again
            else:
                print("❌ You were either not auto logged in, or the session ended prematurely.\n"
                      " check your credentials in config.py.")
        except Exception as e:
            print(e)

    @staticmethod
    def generate_urls() -> None:
        if not os.path.exists('data'):
            os.makedirs('data')
        try:
            with open('data/urlData.txt', 'w', encoding="utf-8") as file:
                linkedin_job_links = utils.LinkedinUrlGenerate().generate_url_links()
                for url in linkedin_job_links:
                    file.write(url + "\n")
            print("Urls are created successfully, now the bot will visit those urls.")
        except:
            print(
                "Couldnt generate url, make sure you have /data folder and modified config.py file for your "
                "preferances.")

    def link_job_apply(self) -> None:
        self.generate_urls()
        count_applied = 0
        count_jobs = 0

        url_data = utils.get_url_data_file()
        for url in url_data:
            self.driver.get(url)
            try:
                total_jobs = self.driver.find_element(By.XPATH, '//small').text
            except:
                print("No Matching Jobs Found")
                continue
            total_pages = utils.jobs_to_pages(total_jobs)

            url_words = utils.url_to_keywords(url)
            line_to_write = "\n Category: " + url_words[0] + ", Location: " + url_words[1] + ", Applying " + str(
                total_jobs) + " jobs."
            self.display_write_results(line_to_write)

            for page in range(total_pages):
                current_page_jobs = constants.jobsPerPage * page
                url = url + "&start=" + str(current_page_jobs)
                self.driver.get(url)
                time.sleep(random.uniform(1, constants.botSpeed))

                offers_per_page = self.driver.find_elements(By.XPATH, '//li[@data-occludable-job-id]')

                offer_ids = []
                for offer in offers_per_page:
                    offer_id = offer.get_attribute("data-occludable-job-id")
                    offer_ids.append(int(offer_id.split(":")[-1]))

                for jobID in offer_ids:
                    offer_page = 'https://www.linkedin.com/jobs/view/' + str(jobID)
                    self.driver.get(offer_page)
                    time.sleep(random.uniform(1, constants.botSpeed))

                    count_jobs += 1

                    job_properties = self.get_job_properties(count_jobs)

                    button = self.easy_apply_button()

                    if button is not False:
                        button.click()
                        time.sleep(random.uniform(1, constants.botSpeed))
                        count_applied += 1
                        try:
                            self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Submit application']").click()
                            time.sleep(random.uniform(1, constants.botSpeed))

                            line_to_write = job_properties + " | " + "* 🥳 Just Applied to this job: " + str(offer_page)
                            self.display_write_results(line_to_write)

                        except:
                            try:
                                self.driver.find_element(By.CSS_SELECTOR,
                                                         "button[aria-label='Continue to next step']").click()
                                time.sleep(random.uniform(1, constants.botSpeed))
                                com_percentage = self.driver.find_element(By.XPATH,
                                                                          'html/body/div[3]/div/div/div[2]/div/div/span').text
                                percen_number = int(com_percentage[0:com_percentage.index("%")])
                                result = self.apply_process(percen_number, offer_page)
                                line_to_write = job_properties + " | " + result
                                self.display_write_results(line_to_write)

                            except Exception as e:
                                try:
                                    self.driver.find_element(By.CSS_SELECTOR,
                                                             "option[value='urn:li:country:" + config.country_code + "']").click()
                                    time.sleep(random.uniform(1, constants.botSpeed))
                                    self.driver.find_element(By.CSS_SELECTOR, 'input').send_keys(config.phone_number)
                                    time.sleep(random.uniform(1, constants.botSpeed))
                                    self.driver.find_element(By.CSS_SELECTOR,
                                                             "button[aria-label='Continue to next step']").click()
                                    time.sleep(random.uniform(1, constants.botSpeed))
                                    com_percentage = self.driver.find_element(By.XPATH,
                                                                              'html/body/div[3]/div/div/div[2]/div/div/span').text
                                    percen_number = int(com_percentage[0:com_percentage.index("%")])
                                    result = self.apply_process(percen_number, offer_page)
                                    line_to_write = job_properties + " | " + result
                                    self.display_write_results(line_to_write)
                                except Exception as e:
                                    line_to_write = job_properties + " | " + "* 🥵 Cannot apply to this Job! " + str(
                                        offer_page)
                                    self.display_write_results(line_to_write)
                    else:
                        line_to_write = job_properties + " | " + "* 🥳 Already applied! Job: " + str(offer_page)
                        self.display_write_results(line_to_write)

            print("Category: " + url_words[0] + "," + url_words[1] + " applied: " + str(count_applied) +
                  " jobs out of " + str(count_jobs) + ".")

        # utils.donate(self)

    def get_job_properties(self, count: int) -> str:
        text_to_write = ""
        job_title = ""
        job_company = ""
        job_location = ""
        job_work_place = ""
        job_posted_date = ""
        job_applications = ""

        try:
            job_title = self.driver.find_element(By.XPATH, "//h1[contains(@class, 'job-title')]").get_attribute(
                "innerHTML").strip()
        except Exception as e:
            print("Warning in getting job_title: " + str(e)[0:50])
            job_title = ""
        try:
            job_company = self.driver.find_element(By.XPATH,
                                                   "//a[contains(@class, 'ember-view t-black t-normal')]").get_attribute(
                "innerHTML").strip()
        except Exception as e:
            print("Warning in getting job_company: " + str(e)[0:50])
            job_company = ""
        try:
            job_location = self.driver.find_element(By.XPATH, "//span[contains(@class, 'bullet')]").get_attribute(
                "innerHTML").strip()
        except Exception as e:
            print("Warning in getting job_location: " + str(e)[0:50])
            job_location = ""
        try:
            job_work_place = self.driver.find_element(By.XPATH,
                                                      "//span[contains(@class, 'workplace-type')]").get_attribute(
                "innerHTML").strip()
        except Exception as e:
            print("Warning in getting jobWorkPlace: " + str(e)[0:50])
            job_work_place = ""
        try:
            job_posted_date = self.driver.find_element(By.XPATH,
                                                       "//span[contains(@class, 'posted-date')]").get_attribute(
                "innerHTML").strip()
        except Exception as e:
            print("Warning in getting job_posted_date: " + str(e)[0:50])
            job_posted_date = ""
        try:
            job_applications = self.driver.find_element(By.XPATH,
                                                        "//span[contains(@class, 'applicant-count')]").get_attribute(
                "innerHTML").strip()
        except Exception as e:
            print("Warning in getting job_applications: " + str(e)[0:50])
            job_applications = ""

        text_to_write = str(
            count) + " | " + job_title + " | " + job_company + " | " + job_location + " | " + job_work_place + " | " + job_posted_date + " | " + job_applications
        return text_to_write

    def easy_apply_button(self) -> Union[WebElement, bool]:
        try:
            # Find the 'Easy Apply' button using the XPath selector.
            button = self.driver.find_element(By.XPATH,
                                              '//button[contains(@class, "jobs-apply-button")]')
            easy_apply_button = button
        except:
            # If the 'Easy Apply' button is not found, return False.
            easy_apply_button = False

        return easy_apply_button

    def apply_process(self, percentage: int, offer_page: str) -> str:
        apply_pages = math.floor(100 / percentage)
        result = ""
        try:
            for pages in range(apply_pages - 2):
                self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Continue to next step']").click()
                time.sleep(random.uniform(1, constants.botSpeed))

            self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Review your application']").click()
            time.sleep(random.uniform(1, constants.botSpeed))

            if config.followCompanies is False:
                self.driver.find_element(By.CSS_SELECTOR, "label[for='follow-company-checkbox']").click()
                time.sleep(random.uniform(1, constants.botSpeed))

            self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Submit application']").click()
            time.sleep(random.uniform(1, constants.botSpeed))

            result = "* 🥳 Just Applied to this job: " + str(offer_page)
        except:
            result = "* 🥵 " + str(apply_pages) + " Pages, couldn't apply to this job! Extra info needed. Link: " + str(
                offer_page)
        return result

    @staticmethod
    def display_write_results(line_to_write: str) -> None:
        try:
            print(line_to_write)
            utils.write_results(line_to_write)
        except Exception as e:
            print("Error in DisplayWriteResults: " + str(e))


start = time.time()
while True:
    try:
        LinkedIn().link_job_apply()
    except Exception as e:
        print("Error in main: " + str(e))
        # close firefox driver
        end = time.time()
        print("---Took: " + str(round((time.time() - start) / 60)) + " minute(s).")
        LinkedIn().driver.quit()




