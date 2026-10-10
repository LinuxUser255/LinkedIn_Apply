"""User profiles: one folder per person with their settings and login.

A profile lives in ``~/.config/LinkedIn_Apply/profiles/<name>/``:

- ``profile.json``: LinkedIn account, form answers and job-search settings.
- ``dynamic_questions.json``: extra form answers (see docs/DYNAMIC_FORMS.md).
- ``chrome/``: the Chrome user-data-dir that keeps the person logged in.

Results (applied jobs, failures, progress) go to ``data/<name>/`` in the
project folder. Set ``LINKEDIN_APPLY_HOME`` to keep profiles elsewhere.
"""

import json
import os
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from dotenv import dotenv_values

from . import config, utils

PROJECT_ROOT = Path(__file__).resolve().parents[2]
QUESTIONS_TEMPLATE = PROJECT_ROOT / "config_forms" / "dynamic_questions.json"
LEGACY_PROFILE_DIR = Path.home() / ".config" / "LinkedIn_Apply_Profile"
SETTINGS_FILE = "profile.json"
QUESTIONS_FILE = "dynamic_questions.json"

_NAME_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{0,39}")


class ProfileError(Exception):
    """Raised for an invalid profile name or a profile that doesn't exist."""


def app_home() -> Path:
    """Return the folder that holds the ``profiles/`` directory."""
    override = os.environ.get("LINKEDIN_APPLY_HOME")
    if override:
        return Path(override).expanduser()
    return Path.home() / ".config" / "LinkedIn_Apply"


def validate_name(name: str) -> str:
    """Return ``name`` if it is safe to use as a folder name.

    Raises:
        ProfileError: If the name is empty, too long or has other characters.
    """
    if not _NAME_PATTERN.fullmatch(name):
        raise ProfileError(
            "Profile names use letters, numbers, '-' or '_' (up to 40 characters), "
            "starting with a letter or number."
        )
    return name


@dataclass(frozen=True)
class Profile:
    """Where one person's settings, Chrome session and results are stored."""

    name: str
    home: Path
    data_dir: Path

    @classmethod
    def for_name(
        cls, name: str, *, home: Path | None = None, data_root: Path | None = None
    ) -> "Profile":
        """Return the profile called ``name`` (which may not exist yet)."""
        validate_name(name)
        return cls(
            name=name,
            home=(home or app_home()) / "profiles" / name,
            data_dir=(data_root or PROJECT_ROOT / "data") / name,
        )

    @property
    def settings_path(self) -> Path:
        return self.home / SETTINGS_FILE

    @property
    def questions_path(self) -> Path:
        return self.home / QUESTIONS_FILE

    @property
    def chrome_dir(self) -> Path:
        return self.home / "chrome"

    @property
    def exists(self) -> bool:
        return self.settings_path.is_file()

    def load_settings(self) -> dict[str, Any]:
        """Read ``profile.json``."""
        with self.settings_path.open(encoding="utf-8") as file:
            return json.load(file)


def list_profiles(*, home: Path | None = None) -> list[str]:
    """Return the names of all saved profiles, sorted."""
    root = (home or app_home()) / "profiles"
    if not root.is_dir():
        return []
    return sorted(path.parent.name for path in root.glob(f"*/{SETTINGS_FILE}"))


def load_profile(
    name: str, *, home: Path | None = None, data_root: Path | None = None
) -> Profile:
    """Return an existing profile.

    Raises:
        ProfileError: If the name is invalid or no such profile was saved.
    """
    profile = Profile.for_name(name, home=home, data_root=data_root)
    if not profile.exists:
        raise ProfileError(
            f"No profile named '{name}'. Create it with: python3 main.py setup {name}"
        )
    return profile


def save_profile(profile: Profile, settings: dict[str, Any]) -> None:
    """Write ``settings`` to the profile, readable only by the current user.

    A copy of the dynamic questions template is added the first time, and
    left alone afterwards so the user's edits are kept.
    """
    profile.home.mkdir(mode=0o700, parents=True, exist_ok=True)
    descriptor = os.open(profile.settings_path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(descriptor, "w", encoding="utf-8") as file:
        json.dump(settings, file, indent=2)
        file.write("\n")
    os.chmod(profile.settings_path, 0o600)
    if not profile.questions_path.exists():
        shutil.copyfile(QUESTIONS_TEMPLATE, profile.questions_path)


def _env_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    return "" if value is None else str(value)


def activate(profile: Profile) -> dict[str, Any]:
    """Point the bot at ``profile`` and return its settings.

    Text settings become environment variables (read by ``LinkedIn``),
    job-search settings go to :mod:`config`, Chrome uses the profile's own
    session folder and results are written to the profile's data folder.
    """
    settings = profile.load_settings()
    for key, value in settings.items():
        if not isinstance(value, (list, dict)):
            os.environ[key] = _env_value(value)
    os.environ["CHROME_PROFILE_PATH"] = str(profile.chrome_dir)
    os.environ["CHROME_PROFILE_DIR"] = "Default"
    config.apply_settings(settings)
    profile.chrome_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
    profile.data_dir.mkdir(parents=True, exist_ok=True)
    utils.set_data_dir(profile.data_dir)
    return settings


def legacy_settings(
    *, legacy_dir: Path | None = None, env_file: Path | None = None
) -> dict[str, Any]:
    """Collect settings from the pre-profiles setup, to prefill the wizard.

    Reads the project ``.env`` and then ``credentials.json`` from the old
    profile folder; non-empty values in the later file win, as they did at
    runtime. Only keys the wizard knows about are returned.
    """
    # Imported here: the wizard imports this module.
    from .setup_wizard import FIELD_KEYS

    sources: list[dict[str, Any]] = []
    env_file = env_file or PROJECT_ROOT / ".env"
    if env_file.is_file():
        sources.append(dict(dotenv_values(env_file)))
    credentials = (legacy_dir or LEGACY_PROFILE_DIR) / "credentials.json"
    if credentials.is_file():
        try:
            sources.append(json.loads(credentials.read_text(encoding="utf-8")))
        except (OSError, json.JSONDecodeError) as error:
            print(f"Warning: could not read {credentials}: {error}")

    settings: dict[str, Any] = {}
    for source in sources:
        for key, value in source.items():
            if key in FIELD_KEYS and value not in (None, "", []):
                settings[key] = value
    return settings
