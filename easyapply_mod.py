"""
The job of this module is to use the xpath value to find
and click the easy apply button on a LinkedIn job listing page.
"""

from selenium.webdriver.common.by import By

# Still unable to find and click the sign in button regardless of the method used.

class ApplyButtonClicker:
    def __init__(self, driver):
        self.driver = driver

    # method to find and click the easy apply button using the Regular Xpath
    def click_easy_apply_button_regular_xpath(self):
        print('Using regular XPath...')
        try:
            # accept any number for the ember element ID
            easy_apply_button = self.driver.find_element(By.XPATH, '//button[starts-with(@id, "ember")]')
            if easy_apply_button:
                easy_apply_button.click()
                print('Easy apply button clicked using regular XPath.')
            else:
                print('Easy apply button not found using regular XPath.')
            if easy_apply_button:
                easy_apply_button.click()
                print('Easy apply button clicked using regular XPath.')
            else:
                print('Easy apply button not found using regular XPath.')
        except Exception as e:
            print(f'Error clicking easy apply button using regular XPath: {e}')

    # Method uses the page element find for the easy apply button using The Element selector
    def click_easy_apply_button_element(self):
        print('Trying Element...')
        try:
            # the element to search for and click:
            # <button aria-label="Easy Apply to " id="ember" class="jobs-apply-button artdeco-button artdeco-button--3 artdeco-button--primary ember-view">
            # <svg role="none" aria-hidden="true" class="artdeco-button__icon artdeco-button__icon--in-bug" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 14 14" data-supported-dps="14x14" data-test-icon="linkedin-bug-xxsmall">
            # <!---->
            #     <use href="#linkedin-bug-xxsmall" width="14" height="14"></use>
            # </svg>
            #
            #
            # <span class="artdeco-button__text">
            #     Easy Apply
            # </span></button>
            easy_apply_button = self.driver.find_element(By.CSS_SELECTOR, '#ember > svg[role="none"][aria-hidden="true"]''.artdeco-button__icon')
            if easy_apply_button:
                easy_apply_button.click()
                print('Easy apply button clicked using Element Selector.')
            else:
                print('Easy apply button Not found using Element Selector.')
        except Exception as e:
            print(f'Error clicking easy apply button using Element selector: {e}')

