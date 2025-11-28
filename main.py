#!/usr/bin/env python3

from src.bot import LinkedIn


def run_bot():
    import time
    print("[MAIN] Starting bot...")
    try:
        bot = LinkedIn()
        print("[MAIN] LinkedIn instance created")
    except Exception as e:
        print(f"[MAIN] Failed to create LinkedIn instance: {e}")
        return
    
    try:
        print("[MAIN] Logging in...")
        bot.login()
        print("[MAIN] Login completed")
    except Exception as e:
        print(f"[MAIN] Login failed: {e}")
        return
    
    try:
        print("[MAIN] Generating URLs...")
        bot.generate_urls()
        print("[MAIN] URLs generated")
    except Exception as e:
        print(f"[MAIN] URL generation failed: {e}")
        return
    
    try:
        print("[MAIN] Starting job application process...")
        bot.link_job_apply()
        print("[MAIN] Job application process completed")
    except Exception as e:
        print(f"[MAIN] Job application process failed: {e}")
        return

    # Keep the browser open; user must close it manually.
    print("Keeping browser open. Close the browser window to exit.")
    try:
        while True:
            time.sleep(60)
            try:
                # Break when all windows are closed
                if not bot.driver.window_handles:
                    break
            except Exception:
                break
    except KeyboardInterrupt:
        pass


def main():
    run_bot()


if __name__ == "__main__":
    main()
