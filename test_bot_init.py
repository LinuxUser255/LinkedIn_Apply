#!/usr/bin/env python3

import sys
import os

# Test bot initialization
try:
    print("[TEST] Testing bot initialization...")
    from src.bot import LinkedIn
    
    # Set headless mode for testing
    os.environ['HEADLESS'] = 'true'
    
    print("[TEST] Creating LinkedIn bot instance...")
    bot = LinkedIn()
    print("[TEST] ✅ Bot initialized successfully!")
    
    print("[TEST] Testing Chrome driver...")
    if bot.driver:
        print("[TEST] ✅ Chrome driver is active")
        bot.driver.get("https://www.example.com")
        print(f"[TEST] ✅ Successfully navigated to: {bot.driver.title}")
        bot.driver.quit()
        print("[TEST] ✅ Bot test completed successfully!")
    else:
        print("[TEST] ❌ Chrome driver not initialized")
        
except Exception as e:
    print(f"[TEST] ❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)