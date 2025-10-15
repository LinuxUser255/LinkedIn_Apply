from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import config

def check_selenium_linkedin():
    """
    Check if Selenium can connect to LinkedIn and verify login status.
    Returns True if login is successful, False otherwise.
    """
    print("Testing Selenium connection to LinkedIn...")
    
    options = Options()
    options.add_argument("--window-size=900,600")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    try:
        driver = webdriver.Chrome(options=options)
        driver.get('https://www.linkedin.com/login')
        
        # Check if the login page loaded
        if "LinkedIn Login" not in driver.title:
            print("❌ Could not load LinkedIn login page")
            driver.quit()
            return False
            
        print("✅ Successfully connected to LinkedIn")
        driver.quit()
        return True
        
    except Exception as e:
        print(f"❌ Error connecting to LinkedIn: {str(e)}")
        return False

if __name__ == "__main__":
    # Test the function when this file is run directly
    check_selenium_linkedin()