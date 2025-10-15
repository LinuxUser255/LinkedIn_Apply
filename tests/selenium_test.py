#!/usr/bin/env python3
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def main():
    opts = Options()
    opts.add_argument('--headless=new')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=opts)
    try:
        driver.get('https://example.org')
        time.sleep(1)
        title = driver.title
        print(f"Title: {title}")
        print("Selenium fetch: ok" if title else "Selenium fetch: failed")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()