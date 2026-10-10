"""Interactive terminal wizard that creates or updates a profile.

Run it with ``python3 main.py setup``. Every question shows its current
answer in [brackets]; pressing Enter keeps it.
"""

import getpass
import os
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from . import profiles
from .config import to_bool

Ask = Callable[[str], str]
Say = Callable[[str], None]

EXPERIENCE_LEVELS = ("Internship", "Entry level", "Associate", "Mid-Senior level", "Director", "Executive")
JOB_TYPES = ("Full-time", "Part-time", "Contract", "Temporary", "Volunteer", "Internship", "Other")
WORKPLACES = ("On-site", "Remote", "Hybrid")
DATES_POSTED = ("Any Time", "Past Month", "Past Week", "Past 24 hours")
SALARIES = (
    "Any", "$40,000+", "$60,000+", "$80,000+", "$100,000+", "$120,000+",
    "$140,000+", "$160,000+", "$180,000+", "$200,000+",
)
SORT_ORDERS = ("Recent", "Relevant")

# Older settings files used these spellings.
_CHOICE_ALIASES = {"Intership": "Internship", "Relevent": "Relevant"}


@dataclass(frozen=True)
class Field:
    """One wizard question.

    ``kind`` decides how the answer is read and stored:

    - ``text`` / ``secret`` / ``number`` / ``file``: a string.
    - ``yes_no``: "Yes" or "No" (also used verbatim to answer forms).
    - ``flag``: a bool.
    - ``list``: comma-separated strings.
    - ``choice`` / ``multi_choice``: a list of entries from ``choices``
      (one entry for ``choice``).
    """

    key: str
    prompt: str
    kind: str = "text"
    default: Any = ""
    choices: tuple[str, ...] = ()
    required: bool = False
    hint: str = ""


SECTIONS: tuple[tuple[str, tuple[Field, ...]], ...] = (
    (
        "LinkedIn account",
        (
            Field("LINKEDIN_EMAIL", "LinkedIn email", required=True),
            Field(
                "LINKEDIN_PASSWORD",
                "LinkedIn password (optional)",
                kind="secret",
                hint="Leave blank to sign in yourself in the Chrome window on the first run. "
                "Chrome remembers the login. A typed password is saved in your profile file.",
            ),
        ),
    ),
    (
        "Contact details (used to fill in application forms)",
        (
            Field("PHONE", "Phone number"),
            Field("CITY", "City"),
            Field("STATE", "State / province"),
            Field("ZIP", "ZIP / postal code"),
            Field("COUNTRY", "Country"),
            Field("ADDRESS", "Street address (optional)"),
            Field("PORTFOLIO_URL", "Portfolio or personal website (optional)"),
            Field("GITHUB_URL", "GitHub profile URL (optional)"),
            Field(
                "RESUME_PATH",
                "Resume file (optional)",
                kind="file",
                hint="Tip: drag the file into this window to paste its path.",
            ),
        ),
    ),
    (
        "Work eligibility and experience",
        (
            Field("WORK_AUTH", "Are you legally authorized to work where you're applying?", "yes_no", "Yes"),
            Field("SPONSORSHIP", "Will you now or in the future need visa sponsorship?", "yes_no", "No"),
            Field("RELOCATE", "Are you willing to relocate?", "yes_no", "No"),
            Field("YEARS_EXPERIENCE", "Years of professional experience", "number", "2"),
            Field("EXPECTED_SALARY", "Expected yearly salary, numbers only (optional)", "number"),
            Field("START_DATE", "When can you start? e.g. Immediately, 2 weeks (optional)"),
        ),
    ),
    (
        "Job search",
        (
            Field(
                "KEYWORDS",
                "Job titles or keywords to search, separated by commas",
                "list",
                required=True,
                hint="Each keyword is searched separately, e.g. Python Developer, Data Analyst",
            ),
            Field(
                "LOCATION",
                "Locations to search, separated by commas",
                "list",
                ["United States"],
                required=True,
                hint="Countries or cities, or a region: Europe, Asia, NorthAmerica, SouthAmerica, "
                "Australia, Africa",
            ),
            Field("EXPERIENCE_LEVELS", "Which experience levels?", "multi_choice", ["Entry level", "Mid-Senior level"], EXPERIENCE_LEVELS),
            Field("JOB_TYPE", "Which job types?", "multi_choice", ["Full-time"], JOB_TYPES),
            Field("REMOTE", "Which workplace types?", "multi_choice", ["Remote"], WORKPLACES),
            Field("DATE_POSTED", "Date posted", "choice", ["Past Week"], DATES_POSTED),
            Field("SALARY", "Minimum salary filter (U.S. jobs)", "choice", ["Any"], SALARIES),
            Field("SORT", "Sort results by", "choice", ["Recent"], SORT_ORDERS),
        ),
    ),
    (
        "Bot behavior",
        (
            Field("FOLLOW_COMPANIES", "Follow companies you apply to?", "flag", False),
            Field(
                "HEADLESS",
                "Hide the Chrome window while the bot runs?",
                "flag",
                False,
                hint="Answer No for your first run so you can sign in.",
            ),
        ),
    ),
)

FIELD_KEYS = frozenset(field.key for _, fields in SECTIONS for field in fields)


def clean_path(raw: str) -> str:
    """Turn a typed or dragged-in file path into an absolute path."""
    path = raw.strip()
    if len(path) >= 2 and path[0] == path[-1] and path[0] in "'\"":
        path = path[1:-1]
    path = path.replace("\\ ", " ")
    return os.path.abspath(os.path.expanduser(path))


def _as_list(value: Any) -> list[str]:
    if isinstance(value, str):
        return [item.strip() for item in value.split(",") if item.strip()]
    return [str(item) for item in value or []]


def _normalize_default(field: Field, value: Any) -> Any:
    """Convert a saved or legacy value into the type ``field`` stores."""
    if field.kind == "yes_no":
        return "Yes" if to_bool(value) else "No"
    if field.kind == "flag":
        return to_bool(value)
    if field.kind == "list":
        return _as_list(value)
    if field.kind in ("choice", "multi_choice"):
        chosen = [_CHOICE_ALIASES.get(item, item) for item in _as_list(value)]
        chosen = [item for item in chosen if item in field.choices]
        return chosen or list(field.default)
    return "" if value is None else str(value)


def _describe(field: Field, value: Any) -> str:
    """Show a default in the prompt's [brackets]."""
    if field.kind == "secret":
        return "saved, press Enter to keep" if value else ""
    if field.kind == "flag":
        return "Yes" if value else "No"
    if isinstance(value, list):
        return ", ".join(value)
    return str(value)


def _parse_numbers(answer: str, count: int) -> list[int] | None:
    """Parse '1, 3' into zero-based indexes, or None if any is invalid."""
    indexes = []
    for part in answer.replace(" ", "").split(","):
        if not part.isdigit() or not 1 <= int(part) <= count:
            return None
        indexes.append(int(part) - 1)
    return list(dict.fromkeys(indexes))


def _parse(field: Field, answer: str) -> tuple[Any, str]:
    """Return (value, error message). An empty message means the answer is valid."""
    if field.kind in ("yes_no", "flag"):
        lowered = answer.lower()
        if lowered not in ("y", "yes", "n", "no"):
            return None, "Please answer yes or no."
        is_yes = lowered.startswith("y")
        return (is_yes if field.kind == "flag" else ("Yes" if is_yes else "No")), ""
    if field.kind == "number":
        digits = answer.replace(",", "")
        return (digits, "") if digits.isdigit() else (None, "Please enter a whole number.")
    if field.kind == "file":
        path = clean_path(answer)
        return (path, "") if os.path.isfile(path) else (None, f"No file found at {path}")
    if field.kind == "list":
        items = _as_list(answer)
        return (items, "") if items else (None, "Please enter at least one value.")
    if field.kind in ("choice", "multi_choice"):
        indexes = _parse_numbers(answer, len(field.choices))
        if indexes is None or (field.kind == "choice" and len(indexes) != 1):
            amount = "one number" if field.kind == "choice" else "one or more numbers, separated by commas"
            return None, f"Please enter {amount} from the list."
        return [field.choices[index] for index in indexes], ""
    return answer, ""


def ask_field(field: Field, default: Any, ask: Ask, ask_secret: Ask, say: Say) -> Any:
    """Ask one question until it gets a valid answer; Enter keeps ``default``."""
    if field.hint:
        say(f"  ({field.hint})")
    if field.kind in ("choice", "multi_choice"):
        for number, choice in enumerate(field.choices, start=1):
            say(f"    {number}) {choice}")
        how = "pick a number" if field.kind == "choice" else "pick numbers, e.g. 1, 3"
        prompt = f"{field.prompt} - {how}"
    elif field.kind in ("yes_no", "flag"):
        prompt = f"{field.prompt} (yes/no)"
    else:
        prompt = field.prompt
    shown = _describe(field, default)
    prompt = f"{prompt} [{shown}]: " if shown else f"{prompt}: "

    while True:
        answer = (ask_secret if field.kind == "secret" else ask)(prompt).strip()
        if not answer:
            if field.required and not default:
                say("  This one is required.")
                continue
            return default
        value, error = _parse(field, answer)
        if not error:
            return value
        say(f"  {error}")


def run_wizard(
    defaults: Mapping[str, Any] | None = None,
    *,
    ask: Ask = input,
    ask_secret: Ask = getpass.getpass,
    say: Say = print,
) -> dict[str, Any]:
    """Ask every question and return the answers as profile settings."""
    defaults = defaults or {}
    settings: dict[str, Any] = {}
    for title, fields in SECTIONS:
        say(f"\n== {title} ==")
        for field in fields:
            default = _normalize_default(field, defaults.get(field.key, field.default))
            settings[field.key] = ask_field(field, default, ask, ask_secret, say)
    return settings


def _ask_name(ask: Ask, say: Say) -> str:
    while True:
        name = ask("Profile name, e.g. your first name: ").strip()
        try:
            return profiles.validate_name(name)
        except profiles.ProfileError as error:
            say(f"  {error}")


def setup_profile(
    name: str | None = None,
    *,
    home: Path | None = None,
    data_root: Path | None = None,
    ask: Ask = input,
    ask_secret: Ask = getpass.getpass,
    say: Say = print,
) -> profiles.Profile:
    """Create a new profile, or update ``name`` if it already exists.

    A brand-new first profile is prefilled from any pre-profiles settings
    (``.env`` or ``~/.config/LinkedIn_Apply_Profile/credentials.json``).
    """
    say("Set up a LinkedIn Apply profile. Press Enter to keep the answer in [brackets].\n")
    if name is None:
        name = _ask_name(ask, say)
    profile = profiles.Profile.for_name(name, home=home, data_root=data_root)

    if profile.exists:
        say(f"Updating profile '{name}'.")
        defaults = profile.load_settings()
    elif not profiles.list_profiles(home=home):
        defaults = profiles.legacy_settings()
        if defaults:
            say("Found settings from an earlier setup; they are filled in as the defaults.")
    else:
        defaults = {}

    settings = {**defaults, **run_wizard(defaults, ask=ask, ask_secret=ask_secret, say=say)}
    profiles.save_profile(profile, settings)

    say(f"\nSaved profile '{name}' to {profile.settings_path}")
    say(f"Start the bot with:  python3 main.py --profile {name}")
    say(f"Change answers with: python3 main.py setup {name}")
    return profile
