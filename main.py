#!/usr/bin/env python3

from src.bot import LinkedIn


def run_bot():
    import time
    bot = LinkedIn()
    bot.login()
    bot.generate_urls()
    bot.link_job_apply()

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
