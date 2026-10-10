"""Tests for the interactive profile setup wizard."""

from collections.abc import Callable, Mapping
from pathlib import Path

import pytest

from src.bot import profiles, setup_wizard


def scripted(answers: Mapping[str, str | list[str]]) -> Callable[[str], str]:
    """Answer prompts containing a key; a list gives answers for repeated asks.

    Prompts that match no key get an empty answer (accept the default).
    """
    queues = {key: list(value) if isinstance(value, list) else [value] for key, value in answers.items()}

    def ask(prompt: str) -> str:
        for key, queue in queues.items():
            if key.lower() in prompt.lower():
                return queue.pop(0) if len(queue) > 1 else queue[0]
        return ""

    return ask


def run(answers: Mapping[str, str | list[str]], defaults: Mapping[str, object] | None = None) -> dict:
    output: list[str] = []
    settings = setup_wizard.run_wizard(
        defaults,
        ask=scripted(answers),
        ask_secret=scripted(answers),
        say=output.append,
    )
    return settings


@pytest.fixture
def resume(tmp_path: Path) -> Path:
    path = tmp_path / "My CV.pdf"
    path.write_bytes(b"%PDF")
    return path


def test_wizard_collects_typed_settings(resume: Path) -> None:
    settings = run(
        {
            "LinkedIn email": "c@example.com",
            "password": "hunter2",
            "Resume": str(resume),
            "keywords": "Python Developer, Backend Engineer",
            "Locations": "United States, Europe",
            "experience level": "2, 4",
            "visa sponsorship": "yes",
            "Follow companies": "n",
            "Date posted": "4",
        }
    )

    assert settings["LINKEDIN_EMAIL"] == "c@example.com"
    assert settings["LINKEDIN_PASSWORD"] == "hunter2"
    assert settings["RESUME_PATH"] == str(resume)
    assert settings["KEYWORDS"] == ["Python Developer", "Backend Engineer"]
    assert settings["LOCATION"] == ["United States", "Europe"]
    assert settings["EXPERIENCE_LEVELS"] == ["Entry level", "Mid-Senior level"]
    assert settings["SPONSORSHIP"] == "Yes"
    assert settings["WORK_AUTH"] == "Yes"  # default
    assert settings["FOLLOW_COMPANIES"] is False
    assert settings["HEADLESS"] is False
    assert settings["DATE_POSTED"] == ["Past 24 hours"]
    assert settings["SORT"] == ["Recent"]


def test_wizard_requires_email_and_keywords() -> None:
    settings = run({"LinkedIn email": ["", "c@example.com"], "keywords": [" , ", "Python"]})

    assert settings["LINKEDIN_EMAIL"] == "c@example.com"
    assert settings["KEYWORDS"] == ["Python"]


def test_wizard_reasks_for_missing_resume_and_bad_choices(resume: Path) -> None:
    settings = run(
        {
            "LinkedIn email": "c@example.com",
            "keywords": "Python",
            "Resume": ["/no/such/file.pdf", str(resume)],
            "experience level": ["9", "one", "1"],
            "visa sponsorship": ["maybe", "no"],
        }
    )

    assert settings["RESUME_PATH"] == str(resume)
    assert settings["EXPERIENCE_LEVELS"] == ["Internship"]
    assert settings["SPONSORSHIP"] == "No"


def test_wizard_keeps_existing_values_when_answers_are_blank(resume: Path) -> None:
    existing = {
        "LINKEDIN_EMAIL": "old@example.com",
        "LINKEDIN_PASSWORD": "saved",
        "RESUME_PATH": str(resume),
        "KEYWORDS": ["Go"],
        "JOB_TYPE": ["Contract"],
        "WORK_AUTH": True,  # legacy files stored booleans
        "RELOCATE": "false",
        "HEADLESS": "true",
        "SALARY": ["$120,000+"],
    }

    settings = run({}, defaults=existing)

    assert settings["LINKEDIN_EMAIL"] == "old@example.com"
    assert settings["LINKEDIN_PASSWORD"] == "saved"
    assert settings["RESUME_PATH"] == str(resume)
    assert settings["KEYWORDS"] == ["Go"]
    assert settings["JOB_TYPE"] == ["Contract"]
    assert settings["WORK_AUTH"] == "Yes"
    assert settings["RELOCATE"] == "No"
    assert settings["HEADLESS"] is True
    assert settings["SALARY"] == ["$120,000+"]


@pytest.mark.parametrize(
    "raw",
    ["'{path}'", '"{path}"', "  {path}  ", "{escaped}"],
)
def test_clean_path_handles_dragged_in_files(raw: str, resume: Path) -> None:
    escaped = str(resume).replace(" ", "\\ ")
    assert setup_wizard.clean_path(raw.format(path=resume, escaped=escaped)) == str(resume)


def test_clean_path_expands_home(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv("HOME", str(tmp_path))
    assert setup_wizard.clean_path("~/cv.pdf") == str(tmp_path / "cv.pdf")


def test_setup_profile_creates_profile_prefilled_from_legacy(
    app_home: Path, data_root: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(profiles, "legacy_settings", lambda: {"LINKEDIN_EMAIL": "legacy@example.com"})
    output: list[str] = []

    profile = setup_wizard.setup_profile(
        home=app_home,
        data_root=data_root,
        ask=scripted({"Profile name": ["bad name", "chris"], "keywords": "Python"}),
        ask_secret=scripted({}),
        say=output.append,
    )

    assert profile.name == "chris"
    assert profile.load_settings()["LINKEDIN_EMAIL"] == "legacy@example.com"
    assert any("python3 main.py --profile chris" in line for line in output)


def test_setup_profile_updates_existing_profile(app_home: Path, data_root: Path) -> None:
    existing = profiles.Profile.for_name("chris", home=app_home, data_root=data_root)
    profiles.save_profile(existing, {"LINKEDIN_EMAIL": "c@example.com", "KEYWORDS": ["Go"]})

    profile = setup_wizard.setup_profile(
        "chris",
        home=app_home,
        data_root=data_root,
        ask=scripted({"keywords": "Rust"}),
        ask_secret=scripted({}),
        say=lambda _: None,
    )

    settings = profile.load_settings()
    assert settings["LINKEDIN_EMAIL"] == "c@example.com"
    assert settings["KEYWORDS"] == ["Rust"]
