"""Tests for finding Chrome for Testing downloads in the project folder."""

from pathlib import Path

import pytest

from src.bot import chrome_paths


def touch(root: Path, relative: str) -> Path:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"")
    return path


@pytest.mark.parametrize(
    "relative",
    [
        "chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing",
        "chrome-mac-x64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing",
        "chrome-linux64/chrome",
        "chrome-win64/chrome.exe",
    ],
)
def test_finds_unzipped_chrome_for_testing(tmp_path: Path, relative: str) -> None:
    expected = touch(tmp_path, relative)

    assert chrome_paths.find_local_chrome(tmp_path) == str(expected)


@pytest.mark.parametrize(
    "relative",
    [
        "chromedriver-mac-arm64/chromedriver",
        "chromedriver-mac-x64/chromedriver",
        "chromedriver-linux64/chromedriver",
        "chromedriver-win64/chromedriver.exe",
        "chromedriver",
    ],
)
def test_finds_unzipped_chromedriver(tmp_path: Path, relative: str) -> None:
    expected = touch(tmp_path, relative)

    assert chrome_paths.find_local_chromedriver(tmp_path) == str(expected)


def test_returns_none_when_nothing_was_downloaded(tmp_path: Path) -> None:
    (tmp_path / "chromedriver-mac-arm64").mkdir()  # folder without the driver inside

    assert chrome_paths.find_local_chrome(tmp_path) is None
    assert chrome_paths.find_local_chromedriver(tmp_path) is None


@pytest.mark.parametrize(
    "relative",
    [
        "chrome-mac/Chromium.app/Contents/MacOS/Chromium",
        "chrome-linux/chrome",
        "chrome-win/chrome.exe",
    ],
)
def test_finds_unzipped_chromium_snapshot(tmp_path: Path, relative: str) -> None:
    expected = touch(tmp_path, relative)

    assert chrome_paths.find_local_chrome(tmp_path) == str(expected)


@pytest.mark.parametrize(
    "relative",
    ["chromedriver_mac64/chromedriver", "chromedriver_linux64/chromedriver", "chromedriver_win32/chromedriver.exe"],
)
def test_finds_chromium_snapshot_chromedriver(tmp_path: Path, relative: str) -> None:
    expected = touch(tmp_path, relative)

    assert chrome_paths.find_local_chromedriver(tmp_path) == str(expected)


def test_prefers_chrome_for_testing_over_chromium_in_project(tmp_path: Path) -> None:
    touch(tmp_path, "chrome-linux/chrome")
    expected = touch(tmp_path, "chrome-linux64/chrome")

    assert chrome_paths.find_local_chrome(tmp_path) == str(expected)


def test_finds_installed_chromium(tmp_path: Path) -> None:
    missing = tmp_path / "usr/bin/chromium"
    installed = touch(tmp_path, "snap/bin/chromium")

    assert chrome_paths.find_installed_chromium((missing, installed)) == str(installed)
    assert chrome_paths.find_installed_chromium((missing,)) is None


def test_find_browser_order(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    chromium = touch(tmp_path, "usr/bin/chromium")
    monkeypatch.setattr(chrome_paths, "INSTALLED_CHROMIUM_PATHS", (chromium,))
    project = tmp_path / "project"
    project.mkdir()

    monkeypatch.setenv("CHROME_BINARY", "/custom/chrome")
    assert chrome_paths.find_browser(project) == "/custom/chrome"

    monkeypatch.delenv("CHROME_BINARY")
    assert chrome_paths.find_browser(project) == str(chromium)

    local = touch(project, "chrome-linux64/chrome")
    assert chrome_paths.find_browser(project) == str(local)
