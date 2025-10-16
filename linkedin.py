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
import json

import config
import constants
import utils


class LinkedIn:
    def __init__(self) -> None:
        # Load project .env if present, then overlay with profile credentials
        load_dotenv()  # Load .env if present
        self._load_profile_credentials()
        self.driver = self._init_chrome()

    def _load_profile_credentials(self) -> None:
        try:
            profile_dir = os.getenv('CHROME_PROFILE_PATH', '').strip()
            if not profile_dir:
                print("[DEBUG] CHROME_PROFILE_PATH not set, skipping profile credentials")
                return
            profile_dir = os.path.expanduser(os.path.expandvars(profile_dir))
            print(f"[DEBUG] Looking for credentials in: {profile_dir}")
            candidates = [
                os.path.join(profile_dir, 'credentials.env'),
                os.path.join(profile_dir, '.env'),
                os.path.join(profile_dir, 'credentials.json'),
            ]
            # Load env files first
            for p in candidates[:2]:
                try:
                    if os.path.isfile(p):
                        print(f"[DEBUG] Loading env file: {p}")
                        load_dotenv(dotenv_path=p, override=True)
                    else:
                        print(f"[DEBUG] File not found: {p}")
                except Exception as e:
                    print(f"[DEBUG] Error loading {p}: {e}")
                    continue
            # Then JSON (overrides if provided)
            p = candidates[2]
            if os.path.isfile(p):
                try:
                    print(f"[DEBUG] Loading JSON file: {p}")
                    with open(p, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    if isinstance(data, dict):
                        for k, v in data.items():
                            if isinstance(k, str):
                                os.environ[k] = '' if v is None else str(v)
                                if k in ['LINKEDIN_EMAIL', 'LINKEDIN_PASSWORD']:
                                    print(f"[DEBUG] Set {k}: {'***' if v else '(empty)'}")
                    print(f"[DEBUG] Loaded {len(data)} entries from JSON")
                except Exception as e:
                    print(f"[DEBUG] Error loading JSON: {e}")
            else:
                print(f"[DEBUG] File not found: {p}")
        except Exception as e:
            print(f"[DEBUG] Error in _load_profile_credentials: {e}")

    def _init_chrome(self) -> webdriver.Chrome:
        options = Options()
        if getattr(config, 'headless', False) or os.getenv('HEADLESS', 'false').lower() in ('1','true','yes'):
            options.add_argument('--headless=new')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--window-size=1280,800')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--no-first-run')
        options.add_argument('--no-default-browser-check')
        options.add_argument('--disable-search-engine-choice-screen')

        # Resolve and prepare Chrome user data dir (profile)
        profile_env = os.getenv('CHROME_PROFILE_PATH', '').strip()
        profile_env = os.path.expanduser(os.path.expandvars(profile_env)) if profile_env else ''
        if profile_env:
            user_data_dir = profile_env
            profile_dir = os.getenv('CHROME_PROFILE_DIR', '').strip()

            # If CHROME_PROFILE_PATH points to a specific profile subdir (e.g., .../Default or .../Profile 1),
            # split it into user-data-dir and profile-directory automatically.
            base = os.path.basename(user_data_dir.rstrip(os.sep))
            if not profile_dir and (base.lower() == 'default' or base.lower().startswith('profile ')):
                profile_dir = base
                user_data_dir = os.path.dirname(user_data_dir)

            # Ensure directory exists
            try:
                os.makedirs(user_data_dir, exist_ok=True)
            except Exception:
                pass

            options.add_argument(f'--user-data-dir={user_data_dir}')
            if profile_dir:
                options.add_argument(f'--profile-directory={profile_dir}')
            else:
                # Default profile name in a fresh user-data-dir is "Default"
                options.add_argument('--profile-directory=Default')

        binary_path = os.getenv('CHROME_BINARY', '').strip()
        if binary_path:
            options.binary_location = binary_path

        driver = webdriver.Chrome(options=options)
        return driver

    def login(self) -> None:
        # Prefer using existing logged-in Chrome profile if CHROME_PROFILE_PATH is provided.
        email = os.getenv('LINKEDIN_EMAIL', getattr(config, 'email', ''))
        password = os.getenv('LINKEDIN_PASSWORD', getattr(config, 'password', ''))

        # Try to go straight to feed; if not logged in, LinkedIn will redirect to login.
        self.driver.get('https://www.linkedin.com/feed')
        time.sleep(random.uniform(2, 4))
        try:
            # If we're already in feed or jobs, we're done.
            if any(s in self.driver.current_url for s in ('linkedin.com/feed', 'linkedin.com/jobs')):
                return

            # Otherwise, we're on the login page.
            # Fill credentials only if fields are present.
            try:
                username_el = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.ID, 'username'))
                )
                password_el = self.driver.find_element(By.ID, 'password')

                if email:
                    try:
                        username_el.clear()
                    except Exception:
                        pass
                    username_el.send_keys(email)
                if password:
                    try:
                        password_el.clear()
                    except Exception:
                        pass
                    password_el.send_keys(password)

                # Ensure "Remember me" is checked if present.
                remember_clicked = False
                remember_input_selectors = [
                    (By.ID, 'remember-me-checkbox'),
                    (By.NAME, 'rememberMe'),
                    (By.CSS_SELECTOR, "input[type='checkbox'][name*='remember']"),
                    (By.CSS_SELECTOR, "input[type='checkbox'][id*='remember']"),
                ]
                for by, sel in remember_input_selectors:
                    try:
                        el = self.driver.find_element(by, sel)
                        if el.get_attribute('type') == 'checkbox' and not el.is_selected():
                            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
                            el.click()
                        remember_clicked = True
                        break
                    except Exception:
                        continue
                if not remember_clicked:
                    # Fall back to clicking the label if inputs weren't found
                    try:
                        lbl = self.driver.find_element(By.CSS_SELECTOR, "label[for*='remember']")
                        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", lbl)
                        lbl.click()
                    except Exception:
                        pass

                sign_in_button_xpath = (
                    "//button[contains(@class,'btn__primary--large') and contains(@type,'submit')]"
                )
                WebDriverWait(self.driver, 15).until(
                    EC.element_to_be_clickable((By.XPATH, sign_in_button_xpath))
                ).click()
            except Exception:
                # No login form; continue
                pass

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
        count_skipped = 0
        count_saved = 0
        self.pause_file = 'data/pause_bot.txt'

        url_data = utils.get_url_data_file()
        if not url_data:
            self.generate_urls()
            url_data = utils.get_url_data_file()
        if not url_data:
            print('No URLs to process.')
            return

        # Load already-applied jobs
        print("\n[INFO] Loading previously applied jobs...")
        applied_jobs = utils.get_applied_jobs()
        print(f"[INFO] Found {len(applied_jobs)} previously applied/attempted jobs.\n")

        print("[INFO] Bot started. To pause, create file: data/pause_bot.txt")
        print("[INFO] To resume, delete the pause file.\n")

        for base_url in url_data:
            # Check for pause
            if os.path.exists(self.pause_file):
                print("\n[PAUSED] Bot paused. Delete data/pause_bot.txt to resume.")
                while os.path.exists(self.pause_file):
                    time.sleep(5)
                print("[RESUMED] Bot resuming...\n")
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
                    # Skip if already applied
                    if utils.is_job_already_applied(str(job_id), applied_jobs):
                        count_skipped += 1
                        print(f"[SKIP] Already applied to job {job_id}, skipping...")
                        continue

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
                                if "Just Applied" in result:
                                    count_applied += 1
                                elif "Couldn't apply" in result:
                                    # Save for later and move on
                                    if self.save_job_for_later():
                                        count_saved += 1
                                        result += " (Saved for later)"
                                line_to_write = job_properties + " | " + result
                                self.display_write_results(line_to_write)
                        except Exception as e:
                            utils.log_failed_job(offer_page, 'Submit flow failed')
                            # Try to save for later
                            if self.save_job_for_later():
                                count_saved += 1
                                print(f"[SAVE] Saved job {job_id} for later review")
                    else:
                        line_to_write = job_properties + " | " + "* Cannot apply (no Easy Apply). Job: " + str(offer_page)
                        self.display_write_results(line_to_write)
                        utils.log_failed_job(offer_page, 'No Easy Apply')
                        try:
                            utils.append_url_for_manual_apply(offer_page)
                            # Also try to save for later
                            if self.save_job_for_later():
                                count_saved += 1
                        except Exception:
                            pass

            print(
                f"Category: {url_words[0]}, {url_words[1]} | Applied: {count_applied} | "
                f"Skipped: {count_skipped} | Saved: {count_saved} | Total processed: {count_jobs}"
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

    def save_job_for_later(self) -> bool:
        """Click the Save button to save job for later review."""
        # First, close any open Easy Apply dialogs
        try:
            close_selectors = [
                (By.CSS_SELECTOR, "button[aria-label='Dismiss']"),
                (By.CSS_SELECTOR, "button[data-test-modal-close-btn]"),
                (By.XPATH, "//button[@aria-label='Dismiss']"),
                (By.XPATH, "//button[contains(@class,'artdeco-modal__dismiss')]"),
            ]
            for by, sel in close_selectors:
                try:
                    close_btn = self.driver.find_element(by, sel)
                    if close_btn.is_displayed():
                        close_btn.click()
                        time.sleep(1)
                        break
                except Exception:
                    continue
        except Exception:
            pass
        
        save_selectors = [
            (By.CSS_SELECTOR, "button.jobs-save-button"),
            (By.CSS_SELECTOR, "button[aria-label*='Save']"),
            (By.XPATH, "//button[contains(@class,'jobs-save-button')]"),
            (By.XPATH, "//button[.//span[contains(text(),'Save')]]"),
        ]
        
        for by, sel in save_selectors:
            try:
                save_btn = WebDriverWait(self.driver, 3).until(
                    EC.presence_of_element_located((by, sel))
                )
                if save_btn.is_displayed() and save_btn.is_enabled():
                    # Check if already saved
                    label = save_btn.get_attribute('aria-label') or ''
                    if 'unsave' in label.lower() or 'saved' in label.lower():
                        print("[INFO] Job already saved, skipping save action")
                        return True
                    # Click save
                    self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", save_btn)
                    time.sleep(0.5)
                    try:
                        save_btn.click()
                    except Exception:
                        self.driver.execute_script('arguments[0].click();', save_btn)
                    time.sleep(1)
                    return True
            except Exception:
                continue
        return False

    def find_easy_apply_button(self) -> Optional[object]:
        # Give the page a moment
        time.sleep(1.5)

        # Highest-signal selectors first
        button_xpaths = [
            "//button[starts-with(@id,'jobs-apply-button') and not(@disabled)]",
            "//button[contains(@class,'jobs-apply-button') and not(@disabled)]",
            "//button[contains(@aria-label,'Easy Apply') and not(@disabled)]",
            "//button[.//span[contains(normalize-space(),'Easy Apply')] and not(@disabled)]",
            "//div[contains(@class,'jobs-apply-button--top-card')]//button[not(@disabled)]",
        ]

        # Try direct button matches
        for xp in button_xpaths:
            try:
                btn = WebDriverWait(self.driver, 4).until(
                    EC.presence_of_element_located((By.XPATH, xp))
                )
                # Ensure we have the button element even if a child was matched
                if btn.tag_name.lower() != 'button':
                    try:
                        btn = btn.find_element(By.XPATH, 'ancestor::button[1]')
                    except Exception:
                        pass
                label = (btn.text or btn.get_attribute('aria-label') or '').lower()
                if 'apply' in label:
                    self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
                    try:
                        WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((By.XPATH, xp)))
                    except Exception:
                        pass
                    if btn.is_displayed() and btn.is_enabled():
                        print(f"[DEBUG] Found Easy Apply via XPath: {xp}")
                        return btn
            except Exception:
                continue

        # Fallback: search any button with text/aria containing Apply and job apply classes
        try:
            cand = None
            for b in self.driver.find_elements(By.TAG_NAME, 'button'):
                txt = (b.text or b.get_attribute('aria-label') or '').strip().lower()
                cls = (b.get_attribute('class') or '').lower()
                if ('apply' in txt) and ('jobs-apply-button' in cls or 'artdeco-button' in cls):
                    cand = b
                    break
            if cand:
                self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", cand)
                print("[DEBUG] Fallback matched Easy Apply button")
                return cand
        except Exception:
            pass

        print("[DEBUG] No Easy Apply button found on this job")
        return None

    def _env(self, key: str, default: str = "") -> str:
        return os.getenv(key, default).strip()

    def _env_bool(self, key: str, default: bool = False) -> bool:
        val = os.getenv(key)
        if val is None:
            return default
        return val.strip().lower() in ("1", "true", "yes", "y")

    def _get_modal(self):
        try:
            return WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='dialog']"))
            )
        except Exception:
            return None

    def _fill_text_like(self, modal):
        from selenium.webdriver.common.keys import Keys
        mappings = [
            (['phone', 'mobile', 'tel'], self._env('PHONE', '')),
            (['city', 'town'], self._env('CITY', '')),
            (['state', 'province', 'region'], self._env('STATE', '')),
            (['zip', 'postal'], self._env('ZIP', '')),
            (['country'], self._env('COUNTRY', '')),
            (['address'], self._env('ADDRESS', '')),
            (['portfolio', 'website', 'url'], self._env('PORTFOLIO_URL', self._env('WEBSITE_URL', ''))),
            (['github'], self._env('GITHUB_URL', '')),
            (['salary', 'compensation'], self._env('EXPECTED_SALARY', '')),
            (['notice', 'available', 'availability', 'start date'], self._env('START_DATE', '')),
            (['years', 'experience'], self._env('YEARS_EXPERIENCE', '')),
        ]
        inputs = modal.find_elements(By.CSS_SELECTOR, "input[type='text'], input[type='tel'], input:not([type]), textarea")
        for el in inputs:
            try:
                desc = " ".join(filter(None, [
                    (el.get_attribute('aria-label') or ''),
                    (el.get_attribute('name') or ''),
                    (el.get_attribute('placeholder') or ''),
                    (el.get_attribute('id') or ''),
                ])).lower()
                if not desc:
                    continue
                for keys, value in mappings:
                    if value and any(k in desc for k in keys):
                        try:
                            el.clear()
                        except Exception:
                            # some inputs need select-all + delete
                            el.send_keys(Keys.CONTROL, 'a')
                            el.send_keys(Keys.DELETE)
                        el.send_keys(value)
                        break
            except Exception:
                continue

    def _upload_resume_if_needed(self, modal):
        path = self._env('RESUME_PATH', '')
        if not path:
            return
        try:
            abs_path = os.path.expanduser(os.path.expandvars(path))
            if not os.path.isfile(abs_path):
                return
            file_inputs = modal.find_elements(By.CSS_SELECTOR, "input[type='file']")
            for fi in file_inputs:
                try:
                    fi.send_keys(abs_path)
                    time.sleep(1)
                    break
                except Exception:
                    continue
        except Exception:
            pass

    def _answer_yes_no(self, modal, question_substrings, answer_yes: bool) -> bool:
        choice = 'Yes' if answer_yes else 'No'
        lowered = [s.lower() for s in question_substrings]
        # Strategy 1: fieldset + legend
        for sub in lowered:
            try:
                el = modal.find_element(By.XPATH,
                    f".//fieldset[.//legend[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'), '{sub}')]]")
                try:
                    lbl = el.find_element(By.XPATH, f".//label[normalize-space()='{choice}']")
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", lbl)
                    lbl.click()
                    return True
                except Exception:
                    pass
            except Exception:
                pass
        # Strategy 2: generic question container containing text
        for sub in lowered:
            try:
                q = modal.find_element(By.XPATH,
                    f".//*[self::p or self::span or self::div][contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'), '{sub}')]")
                container = q.find_element(By.XPATH, "ancestor::*[self::div or self::section or self::form][1]")
                lbls = container.find_elements(By.XPATH, f".//label[normalize-space()='{choice}']")
                for lbl in lbls:
                    try:
                        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", lbl)
                        lbl.click()
                        return True
                    except Exception:
                        continue
            except Exception:
                continue
        return False

    def _fill_selects(self, modal):
        # simple dropdown handling using expected values from env
        desired_city = self._env('CITY', '')
        selects = modal.find_elements(By.TAG_NAME, 'select')
        for sel in selects:
            try:
                desc = " ".join(filter(None, [
                    (sel.get_attribute('aria-label') or ''),
                    (sel.get_attribute('name') or ''),
                    (sel.get_attribute('id') or ''),
                ])).lower()
                from selenium.webdriver.support.ui import Select
                s = Select(sel)
                if 'city' in desc and desired_city:
                    for opt in s.options:
                        if desired_city.lower() in (opt.text or '').lower():
                            s.select_by_visible_text(opt.text)
                            break
            except Exception:
                continue

    def _handle_follow_company(self):
        try:
            if not getattr(config, 'followCompanies', False):
                follow_label = self.driver.find_element(By.CSS_SELECTOR, "label[for='follow-company-checkbox']")
                if follow_label:
                    follow_label.click()
        except Exception:
            pass

    def _click_button_if_present(self, selector, timeout=3) -> bool:
        try:
            btn = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
            btn.click()
            return True
        except Exception:
            return False

    def _fill_current_step(self):
        modal = self._get_modal()
        if not modal:
            return
        self._fill_text_like(modal)
        self._upload_resume_if_needed(modal)
        self._fill_selects(modal)

        # Yes/No questions
        self._answer_yes_no(modal, [
            'authorized to work', 'legally authorized', 'eligible to work'
        ], self._env_bool('WORK_AUTH', True))
        self._answer_yes_no(modal, [
            'require sponsorship', 'require visa sponsorship', 'now or in the future require sponsorship'
        ], self._env_bool('SPONSORSHIP', False))
        self._answer_yes_no(modal, [
            'relocat'
        ], self._env_bool('RELOCATE', False))

    def apply_process_multi_step(self, offer_page: str) -> str:
        try:
            # up to 8 steps to be safe
            for _ in range(8):
                time.sleep(random.uniform(1.5, 3.5))
                self._fill_current_step()

                # Click Continue/Next; else try Review; else break
                advanced = False
                advanced |= self._click_button_if_present("button[aria-label='Continue to next step']", timeout=3)
                if not advanced:
                    # Many dialogs use a generic Next
                    advanced |= self._click_button_if_present("button[aria-label*='Next']", timeout=2)
                if not advanced:
                    advanced |= self._click_button_if_present("button[aria-label='Review your application']", timeout=2)
                if not advanced:
                    # If submit present, break to submit
                    pass

                # Try to submit
                if self._click_button_if_present("button[aria-label='Submit application']", timeout=2):
                    time.sleep(random.uniform(2, 4))
                    return "* Just Applied to this job: " + str(offer_page)

                # If nothing advanced and cannot submit, we're likely stuck
                if not advanced:
                    break

            # Final attempt: uncheck follow company and submit
            self._handle_follow_company()
            if self._click_button_if_present("button[aria-label='Submit application']", timeout=3):
                time.sleep(random.uniform(2, 4))
                return "* Just Applied to this job: " + str(offer_page)

            utils.log_failed_job(offer_page, 'Extra info needed')
            return "* Couldn't apply to this job! Extra info needed. Link: " + str(offer_page)
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
