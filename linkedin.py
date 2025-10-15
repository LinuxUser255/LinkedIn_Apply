#!/usr/bin/env python3

import math
import os
import random
import time
from typing import Optional

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from dotenv import load_dotenv

import config
import constants
import utils


class LinkedIn:
    def __init__(self) -> None:
        load_dotenv()  # Load .env if present
        self.driver = self._init_chrome()

    def _init_chrome(self) -> webdriver.Chrome:
        options = Options()
        if getattr(config, 'headless', False) or os.getenv('HEADLESS', 'false').lower() in ('1','true','yes'):
            options.add_argument('--headless=new')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--window-size=1280,800')
        options.add_argument('--disable-blink-features=AutomationControlled')
        profile_path = os.getenv('CHROME_PROFILE_PATH', '').strip()
        if profile_path:
            options.add_argument(f'--user-data-dir={profile_path}')
        binary_path = os.getenv('CHROME_BINARY', '').strip()
        if binary_path:
            options.binary_location = binary_path
        driver = webdriver.Chrome(options=options)
        return driver

    def login(self) -> None:
        # Prefer using existing logged-in Chrome profile if CHROME_PROFILE_PATH is provided.
        email = os.getenv('LINKEDIN_EMAIL', config.email)
        password = os.getenv('LINKEDIN_PASSWORD', config.password)
        self.driver.get('https://www.linkedin.com/login')
        time.sleep(random.uniform(2, 4))
        try:
            if email and password:
                self.driver.find_element(By.ID, 'username').clear()
                self.driver.find_element(By.ID, 'username').send_keys(email)
                self.driver.find_element(By.ID, 'password').clear()
                self.driver.find_element(By.ID, 'password').send_keys(password)
                sign_in_button_xpath = (
                    "//button[contains(@class,'btn__primary--large') and contains(@type,'submit')]"
                )
                WebDriverWait(self.driver, 15).until(
                    EC.element_to_be_clickable((By.XPATH, sign_in_button_xpath))
                ).click()
            # Wait for either feed or jobs page
            WebDriverWait(self.driver, 20).until(
                EC.any_of(
                    EC.url_contains('linkedin.com/feed'),
                    EC.url_contains('linkedin.com/jobs')
                )
            )
        except Exception as e:
            print(f"Login flow warning: {e}")

    def generate_urls(self) -> None:
        os.makedirs('data', exist_ok=True)
        try:
            with open('data/urlData.txt', 'w', encoding='utf-8') as file:
                linkedin_job_links = utils.LinkedinUrlGenerate().generate_url_links()
                for url in linkedin_job_links:
                    file.write(url + "\n")
            print('URLs created successfully. The bot will visit those URLs.')
        except Exception as e:
            print("Couldn't generate URLs. Ensure ./data exists and config.py preferences are set.")
            print(str(e))

    def link_job_apply(self) -> None:
        count_applied = 0
        count_jobs = 0

        url_data = utils.get_url_data_file()
        if not url_data:
            self.generate_urls()
            url_data = utils.get_url_data_file()
        if not url_data:
            print('No URLs to process.')
            return

        for base_url in url_data:
            self.driver.get(base_url)
            time.sleep(random.uniform(3, 6))
            try:
                total_jobs_el = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//small[contains(.,'results') or contains(.,'result') or contains(.,'jobs') or contains(.,'Job')]"))
                )
                total_jobs = total_jobs_el.text
            except Exception:
                print("No matching jobs found for URL:", base_url)
                continue
            total_pages = utils.jobs_to_pages(total_jobs)

            url_words = utils.url_to_keywords(base_url)
            line_to_write = f"\n Category: {url_words[0]}, Location: {url_words[1]}, Applying {total_jobs} jobs."
            self.display_write_results(line_to_write)

            for page in range(total_pages):
                current_page_jobs = constants.jobsPerPage * page
                url = base_url + "&start=" + str(current_page_jobs)
                self.driver.get(url)
                time.sleep(random.uniform(5, constants.botSpeed))

                offers_per_page = self.driver.find_elements(By.XPATH, "//li[@data-occludable-job-id]")

                offer_ids = []
                for offer in offers_per_page:
                    offer_id = offer.get_attribute("data-occludable-job-id")
                    try:
                        offer_ids.append(int(offer_id.split(":")[-1]))
                    except Exception:
                        continue

                for job_id in offer_ids:
                    offer_page = f'https://www.linkedin.com/jobs/view/{job_id}'
                    self.driver.get(offer_page)
                    time.sleep(random.uniform(5, constants.botSpeed))
                    count_jobs += 1

                    job_properties = self.get_job_properties(count_jobs)
                    button = self.find_easy_apply_button()

                    if button:
                        try:
                            button.click()
                        except Exception:
                            try:
                                self.driver.execute_script('arguments[0].click();', button)
                            except Exception:
                                utils.log_failed_job(offer_page, 'Easy Apply button not clickable')
                                continue
                        time.sleep(random.uniform(5, constants.botSpeed))
                        try:
                            if self.try_submit_single_page():
                                count_applied += 1
                                line_to_write = job_properties + " | " + "* Just Applied to this job: " + str(offer_page)
                                self.display_write_results(line_to_write)
                            else:
                                # Multi-step flow
                                result = self.apply_process_multi_step(offer_page)
                                line_to_write = job_properties + " | " + result
                                self.display_write_results(line_to_write)
                        except Exception:
                            utils.log_failed_job(offer_page, 'Submit flow failed')
                    else:
                        line_to_write = job_properties + " | " + "* Cannot apply (no Easy Apply). Job: " + str(offer_page)
                        self.display_write_results(line_to_write)
                        utils.log_failed_job(offer_page, 'No Easy Apply')

            print(
                "Category: " + url_words[0] + "," + url_words[1] + " applied: " + str(count_applied) +
                " jobs out of " + str(count_jobs) + "."
            )

    def try_submit_single_page(self) -> bool:
        # Try to submit immediately if single-page form
        try:
            submit_btn = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Submit application']"))
            )
            submit_btn.click()
            time.sleep(random.uniform(2, 4))
            return True
        except Exception:
            return False

    def get_job_properties(self, count: int) -> str:
        def safe_text(by: By, selector: str) -> str:
            try:
                el = self.driver.find_element(by, selector)
                t = el.get_attribute('innerText') or el.get_attribute('textContent') or ''
                return t.strip()
            except Exception:
                return ''

        job_title = safe_text(By.CSS_SELECTOR, 'h1')
        job_company = safe_text(By.CSS_SELECTOR, "a[href*='/company/']")
        job_location = safe_text(By.CSS_SELECTOR, "span.jobs-unified-top-card__bullet")
        job_work_place = safe_text(By.CSS_SELECTOR, "span.jobs-unified-top-card__workplace-type")
        job_posted_date = safe_text(By.CSS_SELECTOR, "span.jobs-unified-top-card__posted-date")
        job_applications = safe_text(By.CSS_SELECTOR, "span.jobs-unified-top-card__applicant-count")
        text_to_write = (
            f"{count} | {job_title} | {job_company} | {job_location} | {job_work_place} | {job_posted_date} | {job_applications}"
        )
        return text_to_write

    def find_easy_apply_button(self) -> Optional[object]:
        selectors = [
            (By.CSS_SELECTOR, "button[aria-label*='Easy Apply']"),
            (By.XPATH, "//button[contains(., 'Easy Apply') and not(@disabled)]"),
            (By.XPATH, "//button[contains(@class,'jobs-apply-button')]"),
        ]
        for by, sel in selectors:
            try:
                el = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((by, sel))
                )
                return el
            except Exception:
                continue
        return None

    def apply_process_multi_step(self, offer_page: str) -> str:
        # Continue through multi-step forms then submit
        try:
            # Click through Next/Continue until Review
            for _ in range(5):  # safety cap
                time.sleep(random.uniform(2, 4))
                try:
                    next_btn = WebDriverWait(self.driver, 4).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Continue to next step']"))
                    )
                    next_btn.click()
                    continue
                except Exception:
                    pass
                try:
                    review_btn = WebDriverWait(self.driver, 2).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Review your application']"))
                    )
                    review_btn.click()
                    break
                except Exception:
                    continue

            # Optional follow
            try:
                if not getattr(config, 'followCompanies', False):
                    follow_label = self.driver.find_element(By.CSS_SELECTOR, "label[for='follow-company-checkbox']")
                    if follow_label:
                        follow_label.click()
            except Exception:
                pass

            submit_btn = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Submit application']"))
            )
            submit_btn.click()
            time.sleep(random.uniform(2, 4))
            return "* Just Applied to this job: " + str(offer_page)
        except Exception:
            utils.log_failed_job(offer_page, 'Extra info needed')
            return "* Couldn't apply to this job! Extra info needed. Link: " + str(offer_page)

    @staticmethod
    def display_write_results(line_to_write: str) -> None:
        try:
            print(line_to_write)
            utils.write_results(line_to_write)
        except Exception as e:
            print("Error in DisplayWriteResults: " + str(e))
