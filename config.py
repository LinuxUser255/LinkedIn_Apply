import json
import os
from pathlib import Path

# Load credentials from user's config directory
CONFIG_PATH = Path.home() / ".config" / "LinkedIn_Apply_Profile" / "credentials.json"

# Default configuration (for development/template)
default_config = {
    "BROWSER": ["Chrome"],
    "HEADLESS": False,
    "LINKEDIN_EMAIL": "",
    "LINKEDIN_PASSWORD": "",
    "LINKEDINBOTPROPASSWORD": "",
    "LOCATION": ["United States"],
    "KEYWORDS": ["Software Engineer", "Developer"],
    "EXPERIENCE_LEVELS": ["Entry level", "Mid-Senior level"],
    "YEARS_OF_EXPERIENCE": ["1-3 years"],
    "DATE_POSTED": ["Past Week"],
    "JOB_TYPE": ["Full-time"],
    "REMOTE": ["Remote"],
    "SALARY": ["$80,000+"],
    "SORT": ["Recent"],
    "BLACKLIST_COMPANIES": [],
    "BLACKLIST_TITLES": [],
    "ONLY_APPLY_COMPANIES": [],
    "ONLY_APPLY_TITLES": [],
    "FOLLOW_COMPANIES": False,
    "PHONE_COUNTRY_CODE": "us",
    "PHONE": ""
}

# Try to load user's credentials, fall back to defaults if not found
if CONFIG_PATH.exists():
    try:
        with open(CONFIG_PATH, 'r') as f:
            user_config = json.load(f)
    except Exception as e:
        print(f"Warning: Could not load credentials from {CONFIG_PATH}: {e}")
        print("Using default configuration values.")
        user_config = default_config
else:
    print(f"Note: No credentials file found at {CONFIG_PATH}")
    print("Using default configuration values.")
    print(f"To set up your credentials, create {CONFIG_PATH} with your settings.")
    user_config = default_config

# Map configuration to expected variable names
browser = user_config.get("BROWSER", default_config["BROWSER"])
headless = user_config.get("HEADLESS", default_config["HEADLESS"])
email = user_config.get("LINKEDIN_EMAIL", default_config["LINKEDIN_EMAIL"])
password = user_config.get("LINKEDIN_PASSWORD", default_config["LINKEDIN_PASSWORD"])
LinkedinBotProPassword = user_config.get("LINKEDINBOTPROPASSWORD", default_config["LINKEDINBOTPROPASSWORD"])
location = user_config.get("LOCATION", default_config["LOCATION"])
keywords = user_config.get("KEYWORDS", default_config["KEYWORDS"])
experienceLevels = user_config.get("EXPERIENCE_LEVELS", default_config["EXPERIENCE_LEVELS"])
yearsOfExperience = user_config.get("YEARS_OF_EXPERIENCE", default_config["YEARS_OF_EXPERIENCE"])
datePosted = user_config.get("DATE_POSTED", default_config["DATE_POSTED"])
jobType = user_config.get("JOB_TYPE", default_config["JOB_TYPE"])
remote = user_config.get("REMOTE", default_config["REMOTE"])
salary = user_config.get("SALARY", default_config["SALARY"])
sort = user_config.get("SORT", default_config["SORT"])
blacklist = user_config.get("BLACKLIST_COMPANIES", default_config["BLACKLIST_COMPANIES"])
blackListTitles = user_config.get("BLACKLIST_TITLES", default_config["BLACKLIST_TITLES"])
onlyApply = user_config.get("ONLY_APPLY_COMPANIES", default_config["ONLY_APPLY_COMPANIES"])
onlyApplyTitles = user_config.get("ONLY_APPLY_TITLES", default_config["ONLY_APPLY_TITLES"])
followCompanies = user_config.get("FOLLOW_COMPANIES", default_config["FOLLOW_COMPANIES"])
country_code = user_config.get("PHONE_COUNTRY_CODE", default_config["PHONE_COUNTRY_CODE"])
phone_number = user_config.get("PHONE", default_config["PHONE"])
