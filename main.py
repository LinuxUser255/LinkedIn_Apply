#!/usr/bin/env python3

from linkedin import (
    LinkedIn,
)

def run_bot():
    bot = LinkedIn()
    bot.login()
    bot.generate_urls()
    bot.link_job_apply()


def main():
    run_bot()


if __name__ == "__main__":
    main()
