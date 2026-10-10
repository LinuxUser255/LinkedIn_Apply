"""Job-search and bot settings shared by the URL generator and the bot.

Values start from the built-in defaults, overlaid by the legacy
``~/.config/LinkedIn_Apply_Profile/credentials.json`` if it exists.
Activating a profile replaces them via :func:`apply_settings`, so read
them as ``config.<name>`` at call time rather than importing the names.
"""

import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any

LEGACY_CONFIG_PATH = Path.home() / ".config" / "LinkedIn_Apply_Profile" / "credentials.json"

default_config: dict[str, Any] = {
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
    "PHONE": "",
}

# Module attribute name -> settings key. Attribute names predate the
# project's naming rules and are part of the package's public exports.
_SETTING_KEYS = {
    "browser": "BROWSER",
    "headless": "HEADLESS",
    "email": "LINKEDIN_EMAIL",
    "password": "LINKEDIN_PASSWORD",
    "LinkedinBotProPassword": "LINKEDINBOTPROPASSWORD",
    "location": "LOCATION",
    "keywords": "KEYWORDS",
    "experienceLevels": "EXPERIENCE_LEVELS",
    "yearsOfExperience": "YEARS_OF_EXPERIENCE",
    "datePosted": "DATE_POSTED",
    "jobType": "JOB_TYPE",
    "remote": "REMOTE",
    "salary": "SALARY",
    "sort": "SORT",
    "blacklist": "BLACKLIST_COMPANIES",
    "blackListTitles": "BLACKLIST_TITLES",
    "onlyApply": "ONLY_APPLY_COMPANIES",
    "onlyApplyTitles": "ONLY_APPLY_TITLES",
    "followCompanies": "FOLLOW_COMPANIES",
    "country_code": "PHONE_COUNTRY_CODE",
    "phone_number": "PHONE",
}
_BOOLEAN_SETTINGS = {"HEADLESS", "FOLLOW_COMPANIES"}

SETTING_NAMES = tuple(_SETTING_KEYS)
"""Names of the module attributes that :func:`apply_settings` replaces."""

browser: list[str]
headless: bool
email: str
password: str
LinkedinBotProPassword: str
location: list[str]
keywords: list[str]
experienceLevels: list[str]
yearsOfExperience: list[str]
datePosted: list[str]
jobType: list[str]
remote: list[str]
salary: list[str]
sort: list[str]
blacklist: list[str]
blackListTitles: list[str]
onlyApply: list[str]
onlyApplyTitles: list[str]
followCompanies: bool
country_code: str
phone_number: str


def to_bool(value: Any) -> bool:
    """Interpret a JSON boolean or a yes/no/true/false string."""
    if isinstance(value, str):
        return value.strip().lower() in ("1", "true", "yes", "y")
    return bool(value)


def apply_settings(settings: Mapping[str, Any]) -> None:
    """Replace the module settings with the defaults overlaid by ``settings``."""
    merged = {**default_config, **settings}
    for name, key in _SETTING_KEYS.items():
        value = merged[key]
        globals()[name] = to_bool(value) if key in _BOOLEAN_SETTINGS else value


def _load_legacy_settings() -> dict[str, Any]:
    """Read the pre-profiles settings file, or return {} if there isn't one."""
    if not LEGACY_CONFIG_PATH.exists():
        return {}
    try:
        with LEGACY_CONFIG_PATH.open(encoding="utf-8") as file:
            return json.load(file)
    except (OSError, json.JSONDecodeError) as error:
        print(f"Warning: could not read {LEGACY_CONFIG_PATH}: {error}")
        return {}


apply_settings(_load_legacy_settings())
