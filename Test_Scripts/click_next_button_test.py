#!/usr/bin/env python3
import time
from unittest.mock import MagicMock, patch

from httpcore import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from test_apply_working_full import LinkedInClickApply

class TestLinkedInClickApply:
    def setUp(self):
        self.linkedin_apply = LinkedInClickApply()

def test_click_next_again_button_success(self):
    # Mock the WebDriver and WebDriverWait
    self.linkedin_apply.driver = MagicMock()
    WebDriverWait = MagicMock()
    WebDriverWait.return_value.until.return_value = MagicMock()

    # Mock the click_next_button method
    self.linkedin_apply.click_next_button = MagicMock()

    # Mock time.sleep
    with patch('time.sleep') as mock_sleep:
        # Call the method
        self.linkedin_apply.click_next_again_button()

        # Assert that WebDriverWait was called with the correct arguments
        WebDriverWait.assert_called_once_with(self.linkedin_apply.driver, 10)

        # Assert that the Next button was found and clicked
        WebDriverWait.return_value.until.assert_called_once_with(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(@id, 'ember')]/span[text()='Next']"))
        )
        WebDriverWait.return_value.until.return_value.click.assert_called_once()

        # Assert that click_next_button was called
        self.linkedin_apply.click_next_button.assert_called_once()

        # Assert that time.sleep was called with the correct argument
        mock_sleep.assert_called_once_with(5)
    

def test_click_next_again_button_not_clickable(self):
    # Mock the WebDriver and WebDriverWait
    self.linkedin_apply.driver = MagicMock()
    WebDriverWait = MagicMock()
    WebDriverWait.return_value.until.side_effect = TimeoutException("Element not clickable")

    # Mock the click_next_button method
    self.linkedin_apply.click_next_button = MagicMock()

    # Mock the keep_browser_open function
    with patch('test_apply_working_full.keep_browser_open') as mock_keep_browser_open:
        # Call the method
        self.linkedin_apply.click_next_again_button()

        # Assert that WebDriverWait was called with the correct arguments
        WebDriverWait.assert_called_once_with(self.linkedin_apply.driver, 10)
        
        # Assert that the exception was caught and handled
        self.linkedin_apply.driver.current_url.assert_not_called()
        self.linkedin_apply.driver.page_source.__getitem__.assert_not_called()
        
        # Assert that keep_browser_open was called
        mock_keep_browser_open.assert_called_once()

    # Assert that click_next_button was not called
    self.linkedin_apply.click_next_button.assert_not_called()
    

def main():
    test_click_next_again_button_success(self=TestLinkedInClickApply())
    test_click_next_again_button_not_clickable(self=TestLinkedInClickApply())  # Call the test method)  # Call the test method
    
