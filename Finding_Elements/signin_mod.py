from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

class Find_Sign_In_Button:
    """Attempts to find the 'Sign in' button on the login page using all possible methods.
    Each method tries to find the button and returns True if found, False otherwise."""

    def __init__(self, driver):
        self.driver = driver
        self.options = self.chrome_options()

    def chrome_options(self):
        """Sets up Chrome options to ignore certificate errors and disable Chrome's automation controls."""
        options = Options()
        options.add_argument("--window-size=800,600")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--disable-blink-features")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--headless")
        return options

    # The usual XPath expressions
    def use_xpath(self):
        try:
            self.driver.find_element(By.XPATH, '//*[@id="organic-div"]/form/div[4]/button').click()
            print("Sign in button clicked using XPath.")
        except Exception as e:
            print(f"Error using XPath: {str(e)}")

    def use_full_xpath(self):
        try:
            self.driver.find_element(By.XPATH, '/html/body/div/main/div[2]/div[1]/form/div[4]/button').click()
            print("Sign in button clicked using full XPath.")
        except Exception as e:
            print(f"Error using full XPath: {str(e)}")

    def use_element_find(self):
        try:
            self.driver.find_element(By.CSS_SELECTOR,
                                     'button.btn__primary--large.from__button--floating[data-litms-control-urn="login-submit"]').click()
            print("Sign in button clicked using CSS selector.")
        except Exception as e:
            print(f"Error using CSS selector: {str(e)}")

    def soup_find(self):
        try:
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            button = soup.find('button', {'class': 'btn__primary--large from__button--floating',
                                          'data-litms-control-urn': 'login-submit'})
            if button:
                button.click()
                print("Sign in Button Clicked using BeautifulSoup!")
            else:
                print("Beautiful Soup: Sign in Button Not Found!")
        except Exception as e:
            print(f"Error using BeautifulSoup: {str(e)}")

    def use_js_path(self):
        try:
            button = self.driver.execute_script(
                "return document.querySelector('#organic-div > form > div.login__form_action_container > button')")
            if button:
                button.click()
                print("Sign in button clicked using JavaScript path.")
            else:
                print("JavaScript path: Sign in Button Not Found!")
        except Exception as e:
            print(f"Error using JavaScript path: {str(e)}")

    def use_styles(self):
        try:
            button = self.driver.execute_script(
                "return document.querySelector('button.btn__primary--large.from__button--floating[data-litms-control-urn=\"login-submit\"]')")
            if button:
                button.click()
                print("Sign in button clicked using styles.")
            else:
                print("Styles: Sign in Button Not Found!")
        except Exception as e:
            print(f"Error using styles: {str(e)}")
