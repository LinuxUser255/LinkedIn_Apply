

# LinkedIn Job Application Bot


![linkedin-logo-02](https://github.com/user-attachments/assets/8829660c-8021-49a2-951f-241ea62394e4)


**Built with**

![PythonLogo](https://github.com/user-attachments/assets/4c25054e-c5b1-4577-b1cc-35930bc6cae6)    
![SeleniumLoge](https://github.com/user-attachments/assets/cef6469b-8193-41ac-b663-992b2a788c0a)

**[Selenium docs](https://selenium-python.readthedocs.io/)**



<br>



## A Python bot that will apply to the, "Easy Apply", jobs based on your preferences.

- I may be adding Ollama at some point in the future.

- This repo/codebase is a work in progress, & is intended to be an updated version of [my other linkedin bot](https://github.com/LinuxUser255/linkedin-application-bot)

<br>

## Features
Using only Chrome and Chromedriver (no Firefox):

- Ability to filter jobs by:
  - Easy Apply, location (Worldwide, Europe, Poland, etc.), keyword (python, react, node), experience, position, job type, and date posted.
- Apply based on your salary preference (works best for U.S. job offers).
- Automatically apply to single-page jobs requiring just CV and contact.
- Automatically apply to multi-page offers using saved LinkedIn info (experience, legal rights, resume, etc.).
- Output results to data/ text files for later review.
- Print links for jobs the bot couldn’t apply to due to extra requirements (for manual follow-up).
- Randomized time breaks between actions to avoid thresholds.
- Automatically runs in the background (headless mode optional).
- Chrome-only, runs based on your preferences in config.py or .env.
- Optional: follow or not follow company after successful application.

<br>

## Tests
There is a tests folder to verify your setup and integration:

- python3 tests/setup_tests.py
  - Outputs whether Python, pip, selenium, and dotenv are installed.
- python3 tests/selenium_test.py
  - Verifies Selenium can retrieve data from a website.
- python3 tests/LinkedinTest.py
  - Tries to log into your LinkedIn account using the CHROME_PROFILE_PATH from .env.
  - If it errors, ensure the path exists and that you have created and logged in to your LinkedIn account once.

<br>

## Requirements
- Chrome and matching ChromeDriver only.
- Create a .env from .env.example and adjust values, or edit config.py directly.
- Outputs are written to data/.

<br>

## Credentials and profile setup

There are two ways to provide credentials and applicant info. The recommended approach is to keep secrets outside the repo in a profile directory.

1) Create and edit .env in this project
```shell
cp .env.example .env
# Then open .env and set at minimum:
# Path where Chrome will store/reuse your session (choose any directory you own)
CHROME_PROFILE_PATH="$HOME/.config/LinkedIn_Apply_Profile"
# Optional if your user-data-dir has multiple sub-profiles (e.g., "Default", "Profile 1")
CHROME_PROFILE_DIR="Default"
# Headless off for visibility (optional)
HEADLESS=false
# You may put credentials here, but prefer the profile credentials file below
LINKEDIN_EMAIL=""
LINKEDIN_PASSWORD=""
```

2) Keep secrets in your profile directory (preferred)
- Create the directory if it does not exist and point .env to it via CHROME_PROFILE_PATH.
- Copy the provided template and fill it in locally (do not commit secrets):
```shell
mkdir -p "$HOME/.config/LinkedIn_Apply_Profile"
cp config_forms/credentials.json "$HOME/.config/LinkedIn_Apply_Profile/credentials.json"
```
- Edit "$HOME/.config/LinkedIn_Apply_Profile/credentials.json" and fill the fields you need (all are optional, examples shown as empty strings or booleans):
```json
{
  "LINKEDIN_EMAIL": "",
  "LINKEDIN_PASSWORD": "",
  "PHONE": "",
  "RESUME_PATH": "",
  "CITY": "",
  "STATE": "",
  "ZIP": "",
  "COUNTRY": "",
  "ADDRESS": "",
  "PORTFOLIO_URL": "",
  "GITHUB_URL": "",
  "WEBSITE_URL": "",
  "WORK_AUTH": true,
  "SPONSORSHIP": false,
  "RELOCATE": false,
  "EXPECTED_SALARY": "",
  "START_DATE": "",
  "YEARS_EXPERIENCE": "",
  "HEADLESS": false,
  "CHROME_PROFILE_DIR": "Default"
}
```
Notes:
- The app loads variables in this order, with later sources overriding earlier ones:
  1) Project .env
  2) "$CHROME_PROFILE_PATH"/credentials.env or .env (if present)
  3) "$CHROME_PROFILE_PATH"/credentials.json
- If CHROME_PROFILE_PATH points to a specific sub-profile (e.g., ends with "Default" or "Profile 1"), it is auto-detected; otherwise the default sub-profile "Default" is used, or set CHROME_PROFILE_DIR explicitly.
- Ensure RESUME_PATH points to an existing file if you want automatic resume upload.
- Do not commit secrets. Keep them only in your profile directory.

## Installation and Use

### Clone the repository & install requirements
```shell
git clone https://github.com/LinuxUser255/LinkedIn_Apply.git
cd LinkedIn_Apply
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### Run tests
```shell
python3 tests/setup_tests.py
python3 tests/selenium_test.py
python3 tests/LinkedinTest.py
```

### Run the bot
```shell
python3 main.py
```

<br>

## Notes
- Download the [ChromeDriver](https://googlechromelabs.github.io/chrome-for-testing/#stable) matching your Chrome version and make sure it’s on PATH or placed alongside the project.
- Headless behavior can be toggled via config.headless or HEADLESS in .env.
- See [TODO.md](https://github.com/LinuxUser255/LinkedIn_Apply/blob/main/TODO.md) for roadmap.
