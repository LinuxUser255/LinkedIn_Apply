#!/usr/bin/env python3
"""LinkedIn Easy Apply bot.

Usage:
    python3 main.py                  Run the bot (asks which profile if there are several)
    python3 main.py --profile NAME   Run the bot for profile NAME
    python3 main.py setup [NAME]     Create a profile, or change an existing one
    python3 main.py list             Show saved profiles
"""

import argparse
import sys
import time

from src.bot import LinkedIn
from src.bot.profiles import Profile, ProfileError, app_home, list_profiles, load_profile
from src.bot.setup_wizard import setup_profile


def run_bot(profile: Profile) -> None:
    """Log in, build the search URLs and apply to jobs for ``profile``."""
    print(f"[MAIN] Starting bot for profile '{profile.name}'...")
    try:
        bot = LinkedIn(profile) # LinkedIn Bot object instance creation
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


def choose_profile() -> Profile:
    """Return the profile to run, creating the first one if none exist."""
    names = list_profiles()
    if not names:
        print("No profiles yet. Let's create one.\n")
        return setup_profile()
    if len(names) == 1:
        return load_profile(names[0])

    print("Which profile?")
    for number, name in enumerate(names, start=1):
        print(f"  {number}) {name}")
    while True:
        answer = input("> ").strip()
        if answer.isdigit() and 1 <= int(answer) <= len(names):
            return load_profile(names[int(answer) - 1])
        if answer in names:
            return load_profile(answer)
        print(f"Please enter a number from 1 to {len(names)}.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Apply to LinkedIn Easy Apply jobs using a saved profile.",
    )
    parser.add_argument("--profile", metavar="NAME", help="profile to run (skips the menu)")
    commands = parser.add_subparsers(dest="command", metavar="COMMAND")
    setup = commands.add_parser("setup", help="create a profile, or change an existing one")
    setup.add_argument("name", nargs="?", help="profile to create or change")
    commands.add_parser("list", help="show saved profiles")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "setup":
            setup_profile(args.name)
        elif args.command == "list":
            names = list_profiles()
            if names:
                print("\n".join(names))
            else:
                print("No profiles yet. Create one with: python3 main.py setup")
            print(f"(stored in {app_home() / 'profiles'})")
        else:
            run_bot(load_profile(args.profile) if args.profile else choose_profile())
    except ProfileError as error:
        print(error)
        return 1
    except (KeyboardInterrupt, EOFError):
        print("\nCancelled.")
        return 130
    return 0


if __name__ == "__main__":
    sys.exit(main())
