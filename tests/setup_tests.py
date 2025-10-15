#!/usr/bin/env python3
import sys
import shutil

RESULTS = []

def check_python():
    RESULTS.append(("python", f"{sys.version.split()[0]}"))

def check_pip():
    pip = shutil.which('pip3') or shutil.which('pip')
    RESULTS.append(("pip", "found" if pip else "missing"))

def check_import(pkg):
    try:
        __import__(pkg)
        return True
    except Exception:
        return False

def main():
    check_python()
    check_pip()
    RESULTS.append(("selenium", "ok" if check_import('selenium') else "missing"))
    RESULTS.append(("dotenv", "ok" if check_import('dotenv') else "missing"))

    print("Dependency check:")
    for name, status in RESULTS:
        print(f"- {name}: {status}")

if __name__ == "__main__":
    main()