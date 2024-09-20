#!/usr/bin/env python3

import math
import os
import random
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import config
import constants
import utils


class LinkedIn:
    def __init__(self) -> None:
        self.driver = webdriver.Chrome()
        self.login()

    def login(self) -> None:
        options = Options()

        options.add_argument("--window-size=1024,768")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-blink-features")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("-profile")
        browser = webdriver.Chrome(options=options)
        # Use the same driver instance for login and job application
        self.driver = webdriver.Chrome(options=options)

        try:
            # Launches the browser window: the login page
            # Fill out the email and password from the conf
            self.driver.get('https://www.linkedin.com/login')
            self.driver.find_element("id", "username").send_keys(config.email)
            self.driver.find_element("id", "password").send_keys(config.password)
            time.sleep(5)

            # Looks for the login button and clicks it
            self.driver.find_element("xpath", '//*[@id="organic-div"]/form/div[3]/button').click()

            # Check if the login was successful
            if self.driver.current_url == 'https://www.linkedin.com/feed/':
                print('✅ Logged in successfully!')
                # stay logged in until user closes the browser, and continue to run the bot
                while True:
                    try:
                        self.generate_urls()
                        # Apply to all the jobs generated in the urlData.txt file.
                        self.link_job_apply()
                    except Exception as e:
                        print("An error occurred: ", str(e))
                    finally:
                        time.sleep(60)
            else:
                print("❌ oops, check config.py.")
        except:
            pass
        options = Options()

        options.add_argument("--window-size=800,600")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-blink-features")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("-profile")
        browser = webdriver.Chrome(options=options)

        try:
            # Launches the browser window: the login page
            # Fill out the email and password from the conf
            browser.get('https://www.linkedin.com/login')
            browser.find_element("id", "username").send_keys(config.email)
            browser.find_element("id", "password").send_keys(config.password)
            time.sleep(5)

            # Looks for the login button and clicks it
            browser.find_element("xpath", '//*[@id="organic-div"]/form/div[3]/button').click()

            # Check if the login was successful
            if browser.current_url == 'https://www.linkedin.com/feed/':
                print('�� Logged in successfully!')
                # stay logged in until user closes the browser, and continue to run the bot
                while True:
                    try:
                        self.generate_urls()
                        # open the link_job_apply in the same browser window as the login window
                        browser.execute_script("window.open('');")
                        browser.switch_to.window(browser.window_handles[-1])
                        # Apply to all the jobs generated in the urlData.txt file.
                        self.link_job_apply()
                    except Exception as e:
                        print("An error occurred: ", str(e))
                    finally:
                        time.sleep(60)
            else:
                print("❌ oops, check config.py.")
        except:
            pass

    # Generate LinkedIn job URLs based on the specified criteria in the config file.
    def generate_urls(self):
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
                "Couldnt generate url, make sure you have /data folder and modified config.py file for your ""prefrences.")
        finally:
            pass

    # Apply to all the jobs generated in the urlData.txt file.
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
                time.sleep(random.uniform(5, constants.botSpeed))

                offers_per_page = self.driver.find_elements(By.XPATH, '//li[@data-occludable-job-id]')

                offer_ids = []
                for offer in offers_per_page:
                    offer_id = offer.get_attribute("data-occludable-job-id")
                    offer_ids.append(int(offer_id.split(":")[-1]))

                for jobID in offer_ids:
                    # Bot works better when setting offer page to /search, instead of /view/
                    # offer_page = 'https://www.linkedin.com/jobs/view/' + str(jobID)
                    offer_page = 'https://www.linkedin.com/jobs/search/' + str(jobID)
                    self.driver.get(offer_page)
                    time.sleep(random.uniform(5, constants.botSpeed))

                    count_jobs += 1

                    job_properties = self.get_job_properties(count_jobs)

                    button = self.easy_apply_button()
                   # button = self.driver.find_element(By.XPATH, '//button[contains(@class, "easy_apply_button")]')

                    if button is not False:
                        self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Easy Apply']").click()
                        time.sleep(random.uniform(5, constants.botSpeed))
                        # button.click()
                        time.sleep(random.uniform(5, constants.botSpeed))
                        count_applied += 1
                        try:
                            self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Submit application']").click()
                            time.sleep(random.uniform(5, constants.botSpeed))

                            line_to_write = job_properties + " | " + "* 🥳 Just Applied to this job: " + str(offer_page)
                            self.display_write_results(line_to_write)

                        except:
                            try:
                                self.driver.find_element(By.CSS_SELECTOR,
                                                         "button[aria-label='Continue to next step']").click()
                                time.sleep(random.uniform(5, constants.botSpeed))
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

    def easy_apply_button(self):
        try:
            button = self.driver.find_element(By.XPATH,'//button[contains(@class, "artdeco-button__text")]')
            easy_apply_button = button
        except:
            easy_apply_button = False

        return easy_apply_button

    def apply_process(self, percentage: int, offer_page: str) -> str:
        apply_pages = math.floor(100 / percentage)
        result = ""
        try:
            for pages in range(apply_pages - 2):
                self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Continue to next step']").click()
                time.sleep(random.uniform(5, constants.botSpeed))

            self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Review your application']").click()
            time.sleep(random.uniform(5, constants.botSpeed))

            if config.followCompanies is False:
                self.driver.find_element(By.CSS_SELECTOR, "label[for='follow-company-checkbox']").click()
                time.sleep(random.uniform(5, constants.botSpeed))

            self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Submit application']").click()
            time.sleep(random.uniform(5, constants.botSpeed))

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
        end = time.time()
        print("---Took: " + str(round((time.time() - start) / 60)) + " minute(s).")
        LinkedIn().driver.quit()
