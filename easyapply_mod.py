"""
The job of this module is to use the xpath value to find 
and click the easy apply button on a LinkedIn job listing page.
"""
from random import randint


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
            easy_apply_button = self.driver.find_element(By.XPATH, f'//button[@id="ember{randint(1, 1000)}"]')
            if easy_apply_button:
                easy_apply_button.click()
                print('Easy apply button clicked using regular XPath.')
            else:
                print('Easy apply button not found using regular XPath.')
            # easy_apply_button = self.driver.find_element(By.XPATH, '//*[@id="ember148"]/svg')
            if easy_apply_button:
                easy_apply_button.click()
                print('Easy apply button clicked using regular XPath.')
            else:
                print('Easy apply button not found using regular XPath.')
        except Exception as e:
            print(f'Error clicking easy apply button using regular XPath: {e}')

    # method to find and click the easy apply button using the Full Xpath
    def click_easy_apply_button_full_xpath(self):
        print('Using full XPath...')
        try:
            easy_apply_button = self.driver.find_element(By.XPATH, '/html/body/div[6]/div[3]/div['
                                                                   '4]/div/div/main/div/div[2]/div[2]/div/div['
                                                                   '2]/div/div[1]/div/div[1]/div/div[1]/div/div['
                                                                   '6]/div/div/div/button/svg')
            if easy_apply_button:
                # easy_apply_button
                easy_apply_button.click()
                print('Easy apply button clicked using full XPath.')
        except Exception as e:
            print(f'Error clicking easy apply button using full XPath: {e}')

    # Method uses the page element find for the easy apply button using CSS selector
    def click_easy_apply_button_element(self):
        print('Trying Element...')
        try:
            easy_apply_button = self.driver.find_element(By.CSS_SELECTOR, 'svg[role="none"][aria-hidden="true"]['
                                                                          'class="artdeco-button__icon "]')
            if easy_apply_button:
                easy_apply_button.click()
                print('Easy apply button clicked using CSS selector.')
            else:
                print('Easy apply button not found using CSS selector.')
        except Exception as e:
            print(f'Error clicking easy apply button using CSS selector: {e}')

    def click_easy_apply_button_js_path(self):
        print('Trying JavaScript...')
        # document.querySelector("#ember1084 > svg")
        try:
            easy_apply_button = self.driver.execute_script(
                "return document.querySelector('#ember1084 > svg')")
            if easy_apply_button:
                easy_apply_button.click()
                print('Easy apply button clicked using JavaScript path.')
            else:
                print('JavaScript path: Easy apply Button Not Found!')
        except Exception as e:
            print(f'Error using JavaScript path: {e}')
