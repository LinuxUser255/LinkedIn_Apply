#!/usr/bin/env python3

"""
This script is used to test the auto apply process.
It uses only one job link, that the user places in: /Provided/job_link.txt

Order of operations:
=====================

1. First Action:  Click the 1st Easy Apply button.

2. Second Action: Click Next button on the Contact info popup.

3. Third Action: Click Next button on Upload resume.

4. Fourth Action: Click Next button on Additional questions.

5. Fith Action: Click the down arrow on the Drop-down menu.

6. Sixth Action: Select either Yes of No to certs, (default set to No).

7. Seventh Action: Click Next on the Additional questions box.

8. Eighth Action: Click Review on Work Auth, (default set to Yes).

9. Ninth Action: Click Submit Application.

See the, `def handle_work_authorization(self) -> None:` , method, for latest debug.
"""

import os
import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import config


def keep_browser_open() -> None:
    print("\nKeep Browser Open Method Running.")
    print(".. Close manually to exit.\n")
    while True:
        time.sleep(60)
        print("Browser still open...\n")

class LinkedInClickApply:
    def __init__(self) -> None:
        options = Options()
        options.add_argument("--window-size=800,600")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--disable-blink-features")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=options)


   # SIGN IN TO YOUR ACCOUNT
    def signin(self) -> None:
        try:
            self.driver.get('https://www.linkedin.com/login')
            self.driver.find_element(By.ID, "username").send_keys(config.email)
            self.driver.find_element(By.ID, "password").send_keys(config.password)
            time.sleep(8)

            sign_in_button_xpath = ("//button[contains(@class, 'btn__primary--large') and contains(@type, 'submit') "
                                    "and (contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', "
                                    "'abcdefghijklmnopqrstuvwxyz'), 'sign in') or contains(translate(., "
                                    "'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'signin'))]")
            sign_in_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, sign_in_button_xpath))
            )
            sign_in_button.click()

            if self.driver.current_url == 'https://www.linkedin.com/feed/':
                print('\nSign In Button Clicked....\n')
                self.navigate_to_job_listing()
                time.sleep(8)
                self.try_click_easy_apply_button()

                time.sleep(5)
                if self.driver.current_url.startswith('https://www.linkedin.com/jobs/search/'):
                    print('Job application form loaded successfully....')
                    #self.click_next_button()
                    self.navigate_to_job_listing()
                else:
                    print('\nJob application form not loaded successfully...\n')

                while True:
                    time.sleep(60)
        except Exception as e:
            print(f"\nA sign in error occurred: {e}\n")


   # GO TO THE JOB LISTING URL
    def navigate_to_job_listing(self) -> None:
        print('\nNavigating to Job Listing Method Running ...\n')
        try:
            file_path = "/home/linux/Projects/Bots/LinkedIn_Apply/Provided/job_link.txt"
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"The file {file_path} does not exist.")

            with open(file_path, 'r') as file:
                job_link = file.readline().strip()

            self.driver.get(job_link)
            time.sleep(5)
            self.try_click_easy_apply_button()
        except Exception as e:
            print(f"\nError navigating to job listing: {e}")
            print(f"Current working directory: {os.getcwd()}\n")


    # CLICK ON THE 'Easy Apply' BUTTON
    def try_click_easy_apply_button(self) -> None:
        print('Attempting to Click Easy Apply Button...\n')
        try:
            xpath = "//button[contains(@class, 'jobs-apply-button') and contains(@aria-label, 'Easy Apply')]"
            button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
            time.sleep(2)
            self.click_button(button)
            print('Easy Apply button clicked successfully\n')
            time.sleep(5)

            # Call the resume_pop_up_box method after successfully clicking the Easy Apply button
           #  self.resume_pop_up_box() # trying to call it in the method below
            self.click_button(button)
        except Exception as e:
            print(f"Error clicking Easy Apply button: {str(e)}\n")
            keep_browser_open()

    def click_button(self, button: WebElement) -> None:
        try:
            button.click()
            # Call the resume_pop_up_box method after successfully clicking the Easy Apply button
            self.resume_pop_up_box()
        except:
            try:
                ActionChains(self.driver).move_to_element(button).click().perform()
            except:
                self.driver.execute_script("arguments[0].click();", button)


    # !! Currently, this is not clicking the Next button on the Upload resume page.
    # UPLOAD RESUME: Change the name of this method
    def resume_pop_up_box(self) -> None:
        print('Handling The Resume Pop-Up Box:\n')
        try:
            # //*[@id="ember353"]/span
            resume_popup_xpath = ("//button[contains(@id, 'ember') and contains(@class, 'artdeco-button--primary') and "
                                  "(contains(@aria-label, 'Next') or contains(@aria-label, 'Continue'))]")
    
            next_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, resume_popup_xpath)))
            time.sleep(2)
            print("Attempting to click Next button on the Resume Pop-Up Box...\n")

            # Try multiple methods to click the button
            try:
                next_button.click()
            except Exception as e:
                print(f"Direct click failed: {str(e)}")
                try:
                    ActionChains(self.driver).move_to_element(next_button).click().perform()
                    print("ActionChains click successful")
                except Exception as e:
                    print(f"ActionChains click failed: {str(e)}")
                    try:
                        self.driver.execute_script("arguments[0].click();", next_button)
                        print("JavaScript click successful")
                    except Exception as e:
                        print(f"JavaScript click failed: {str(e)}")
                        raise Exception("All click methods failed")
            print("Next button clicked successfully.\n")
            
            # Wait for the next page to load
            time.sleep(5)
            
            # Verify if the Next button was clicked by searching for the text "Upload resume"
            # Maybe edit: in.self.driver.page_source.lower():  Because it seems to not be enforced.
            if "upload resume" in self.driver.page_source.lower():
                # if "upload resume" in self.driver.page_source.lower(): was successful, proceed to then click the Next button
                print("Attempting to click the Next Button on the Upload Resume Box...\n")
                try:
                    next_button.click()
                except Exception as e:
                    print(f"Direct click failed: {str(e)}")
                    try:
                        ActionChains(self.driver).move_to_element(next_button).click().perform()
                        print("ActionChains click successful")
                    except Exception as e:
                        print(f"ActionChains click failed: {str(e)}")
                        try:
                            self.driver.execute_script("arguments[0].click();", next_button)
                            print("JavaScript click successful")
                        except Exception as e:
                            print(f"JavaScript click failed: {str(e)}")
                            raise Exception("All click methods failed")

                print("Next button clicked successfully.\n")
                time.sleep(5)

                # should be clicking the Next button..but it's not working as expected
                print("Should be clicking the Next button on the Upload resume box.\n")
                self.handle_additional_questions_certs() # <-- This calls the next method to handle the additional questions/certifications
                print("Proceeding to the next method: handle_additional_questions_certs.\n")
            else:
                print("Failed to click the Next button. 'Upload resume' not found.")
                print("Current page source:", self.driver.page_source)
                keep_browser_open()
        
        except Exception as e:
            print(f"\nError in resume_pop_up_box: {str(e)}")
            print(f"Current URL: {self.driver.current_url}")
            print(f"Page source: {self.driver.page_source[:500]}...")
            keep_browser_open()

            # OK, ALL THAT WORKED ^^^^^^^


    # ADDITIONAL QUESTIONS: Certifications
    def handle_additional_questions_certs(self) -> None:
        print('Handling the Additional Questions Pop-Up Box...\n')
        try:
            # Set the drop_down_menu_xpath
            drop_down_menu_xpath = ("//*[@id='text-entity-list-form-component-formElement-urn-li-jobs-applyformcommon"
                                    "-easyApplyFormElement-4140989961-14995880972-multipleChoice']")
            
            # Wait for the dropdown menu to be present and clickable
            drop_down_menu = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, drop_down_menu_xpath))
            )
            
            # Click the dropdown menu to open it
            drop_down_menu.click()
            print('Dropdown menu clicked successfully.\n')
    
            # Wait for the "No certifications" option to be visible and click it
            no_cert_option_xpath = ("//*[@id='text-entity-list-form-component-formElement-urn-li-jobs-applyformcommon"
                                    "-easyApplyFormElement-4140989961-14995880972-multipleChoice']/option[3]")
            no_cert_option = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, no_cert_option_xpath))
            )
            no_cert_option.click()
            print('No certifications option selected.\n')
    
            next_button_xpath = "//button[contains(@aria-label, 'Next') or contains(@aria-label, 'Continue')]"
            next_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, next_button_xpath))
            )
            next_button.click()
            print('Next button clicked successfully. Moving on to Work authorization.\n')
    
        except Exception as e:
            print(f'Error handling additional questions (certifications): {str(e)}\n')
            print('Attempting to continue with the application process...\n')
    
        # Continue with the next step in the application process
        self.handle_work_authorization()



    # WORK AUTHORIZATION: Clicks the NEXT button on Additional questions box
    def handle_work_authorization(self) -> None:
        """
        Sticking Pont:
        Interesting Error Message Received:

        Error handling work authorization:
        Message: element click intercepted:

        Element <span class="artdeco-button__text">...</span>
        is not clickable at point (883, 64).

        Other element would receive the click:
        <use href="#close-medium" width="24" height="24"></use>

        Possible culprit:
        This error message is likely caused by the element being obscured by another element on the page.
        """
        print('Handling the Work Authorization Questions Box...\n')
        try:
            # Use the provided XPath, accepting any number for the ID
            # Not Working:  work_auth_xpath = "//*[contains(@id, 'ember')]/span" # Error message Is not clickable
            # So I'm customizing this:
            work_auth_clickable_element = '"<use href="#close-medium" width="24" height="24"></use>"'
            # Error message Is not clickable
#            work_auth_element = WebDriverWait(self.driver, 10).until(
#                EC.element_to_be_clickable((By.XPATH, work_auth_xpath))
#            )
            work_auth_element = WebDriverWait(self.driver, 10).until(
                # The XPath doesn't work, so I'm trying a partial link text instead
                EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, work_auth_clickable_element))
            )
            print('Attempting to click the Work Authorization element...\n')

            if work_auth_element:
                work_auth_element.click()
                print('Success: Work authorization element clicked...\n')
                time.sleep(2)  # Wait for any potential changes after clicking
                self.review_application()
                print('Proceeding to submit the application...\n')
            else:
                print('Work authorization element not found. Proceeding to submit application...\n')
                self.review_application()
        except Exception as e:
            print(f"Error handling work authorization: {str(e)}\n")
            print(f"Current URL: {self.driver.current_url}")
            print(f"Page source: {self.driver.page_source[:500]}...")
            keep_browser_open()


    # REVIEW APPLICATION button
    # And clicks the Submit Application button
    # REVIEW APPLICATION button
    # And clicks the Submit Application button
    def review_application(self) -> None:
        print('\nSubmit Application Method Running...\n')
        try:
            # XPath: //*[@id="ember363"]/span
            review_application_xpath = "//*[contains(@id, 'ember')]/span"
            submit_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, review_application_xpath))
            )
            print("Attempting to click Submit button...\n")
            submit_button.click()
            print('Submit button clicked\n')
            print('Congrats! Your application has been submitted.\n')
            time.sleep(5)  # Wait for any potential changes after clicking
        except Exception as e:
            print(f"Error clicking Submit button: {str(e)}")
            print(f"Current URL: {self.driver.current_url}\n")
            print(f"Page source: {self.driver.page_source[:500]}...\n")
            keep_browser_open()


    # KEEP THE  BROWSER OPEN
    def run_click_apply(self) -> None:
        print("\nrun_click_apply...\n")
        self.signin()
        keep_browser_open()


if __name__ == "__main__":
    linkedin_click_apply = LinkedInClickApply()
    linkedin_click_apply.run_click_apply()



