"""Tests for profile storage and activation."""

import json
import os
import stat
from pathlib import Path

import pytest

from src.bot import config, profiles, utils


def make_profile(name: str, app_home: Path, data_root: Path) -> profiles.Profile:
    return profiles.Profile.for_name(name, home=app_home, data_root=data_root)


@pytest.mark.parametrize("name", ["chris", "chris-dev", "Alex_2", "a" * 40])
def test_validate_name_accepts_simple_names(name: str) -> None:
    assert profiles.validate_name(name) == name


@pytest.mark.parametrize("name", ["", " ", "../evil", "a b", "-lead", "a/b", "a" * 41])
def test_validate_name_rejects_unsafe_names(name: str) -> None:
    with pytest.raises(profiles.ProfileError):
        profiles.validate_name(name)


def test_profile_paths(app_home: Path, data_root: Path) -> None:
    profile = make_profile("chris", app_home, data_root)

    assert profile.home == app_home / "profiles" / "chris"
    assert profile.settings_path == profile.home / "profile.json"
    assert profile.questions_path == profile.home / "dynamic_questions.json"
    assert profile.chrome_dir == profile.home / "chrome"
    assert profile.data_dir == data_root / "chris"
    assert not profile.exists


def test_save_profile_writes_private_settings_and_question_template(
    app_home: Path, data_root: Path
) -> None:
    profile = make_profile("chris", app_home, data_root)

    profiles.save_profile(profile, {"LINKEDIN_EMAIL": "c@example.com"})

    assert profile.exists
    assert profile.load_settings() == {"LINKEDIN_EMAIL": "c@example.com"}
    assert stat.S_IMODE(profile.settings_path.stat().st_mode) == 0o600
    template = json.loads(profiles.QUESTIONS_TEMPLATE.read_text(encoding="utf-8"))
    assert json.loads(profile.questions_path.read_text(encoding="utf-8")) == template


def test_save_profile_keeps_edited_question_file(app_home: Path, data_root: Path) -> None:
    profile = make_profile("chris", app_home, data_root)
    profiles.save_profile(profile, {})
    profile.questions_path.write_text('{"question_patterns": {}}', encoding="utf-8")

    profiles.save_profile(profile, {"PHONE": "555"})

    assert profile.questions_path.read_text(encoding="utf-8") == '{"question_patterns": {}}'


def test_list_profiles_returns_saved_names_sorted(app_home: Path, data_root: Path) -> None:
    assert profiles.list_profiles(home=app_home) == []
    for name in ("zoe", "alex"):
        profiles.save_profile(make_profile(name, app_home, data_root), {})
    (app_home / "profiles" / "not-a-profile").mkdir()

    assert profiles.list_profiles(home=app_home) == ["alex", "zoe"]


def test_load_profile_requires_existing_profile(app_home: Path, data_root: Path) -> None:
    with pytest.raises(profiles.ProfileError, match="setup"):
        profiles.load_profile("ghost", home=app_home, data_root=data_root)

    profiles.save_profile(make_profile("chris", app_home, data_root), {})
    assert profiles.load_profile("chris", home=app_home, data_root=data_root).name == "chris"


def test_activate_exposes_settings_to_the_bot(app_home: Path, data_root: Path) -> None:
    profile = make_profile("chris", app_home, data_root)
    profiles.save_profile(
        profile,
        {
            "LINKEDIN_EMAIL": "c@example.com",
            "WORK_AUTH": "Yes",
            "FOLLOW_COMPANIES": False,
            "HEADLESS": True,
            "KEYWORDS": ["Python"],
            "LOCATION": ["Europe"],
        },
    )

    settings = profiles.activate(profile)

    assert settings["LINKEDIN_EMAIL"] == "c@example.com"
    assert os.environ["LINKEDIN_EMAIL"] == "c@example.com"
    assert os.environ["WORK_AUTH"] == "Yes"
    assert os.environ["FOLLOW_COMPANIES"] == "false"
    assert os.environ["CHROME_PROFILE_PATH"] == str(profile.chrome_dir)
    assert os.environ["CHROME_PROFILE_DIR"] == "Default"
    assert "KEYWORDS" not in os.environ
    assert config.keywords == ["Python"]
    assert config.location == ["Europe"]
    assert config.followCompanies is False
    assert config.headless is True
    assert utils.data_path("failed_jobs.txt") == str(profile.data_dir / "failed_jobs.txt")
    assert profile.chrome_dir.is_dir()
    assert profile.data_dir.is_dir()


def test_legacy_settings_prefers_credentials_json_over_env_file(tmp_path: Path) -> None:
    legacy_dir = tmp_path / "legacy"
    legacy_dir.mkdir()
    (legacy_dir / "credentials.json").write_text(
        json.dumps({"LINKEDIN_EMAIL": "json@example.com", "CITY": ""}), encoding="utf-8"
    )
    env_file = tmp_path / ".env"
    env_file.write_text("LINKEDIN_EMAIL=env@example.com\nCITY=Austin\nUNRELATED=x\n", encoding="utf-8")

    settings = profiles.legacy_settings(legacy_dir=legacy_dir, env_file=env_file)

    assert settings["LINKEDIN_EMAIL"] == "json@example.com"
    assert settings["CITY"] == "Austin"  # empty JSON value doesn't hide the .env value
    assert "UNRELATED" not in settings


def test_legacy_settings_empty_when_nothing_exists(tmp_path: Path) -> None:
    assert profiles.legacy_settings(legacy_dir=tmp_path / "x", env_file=tmp_path / ".env") == {}
