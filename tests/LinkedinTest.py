#!/usr/bin/env python3
import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def main():
    load_dotenv()
    profile = os.getenv('CHROME_PROFILE_PATH', '').strip()
    opts = Options()
    if profile:
        opts.add_argument(f'--user-data-dir={profile}')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=opts)
    try:
        driver.get('https://www.linkedin.com/')
        WebDriverWait(driver, 15).until(
            EC.any_of(
                EC.url_contains('linkedin.com/feed'),
                EC.url_contains('linkedin.com/login'),
                EC.presence_of_element_located((By.TAG_NAME, 'body')),
            )
        )
        url = driver.current_url
        if 'linkedin.com/feed' in url:
            print('LinkedIn session: logged in (via profile)')
        elif 'linkedin.com/login' in url:
            print('LinkedIn session: login required. Ensure CHROME_PROFILE_PATH exists and is logged in once.')
        else:
            print(f'LinkedIn session: unknown state -> {url}')
        time.sleep(1)
    finally:
        driver.quit()

if __name__ == '__main__':
    main()