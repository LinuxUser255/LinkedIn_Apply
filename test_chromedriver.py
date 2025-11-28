#!/usr/bin/env python3

import sys
import os

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    print("[TEST] Starting ChromeDriver test...")
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    # Use the Chrome binary in the project
    chrome_binary = './chrome-linux64/chrome'
    if os.path.exists(chrome_binary):
        options.binary_location = chrome_binary
        print(f"[TEST] Using Chrome binary: {chrome_binary}")
    
    # Try with local chromedriver
    service = Service('./chromedriver')
    driver = webdriver.Chrome(service=service, options=options)
    
    print("[TEST] ✅ ChromeDriver initialized successfully!")
    print("[TEST] Testing navigation...")
    
    driver.get("https://www.example.com")
    print(f"[TEST] ✅ Navigated to: {driver.title}")
    
    driver.quit()
    print("[TEST] ✅ ChromeDriver test completed successfully!")
    
except Exception as e:
    print(f"[TEST] ❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)