"""Find the browser and ChromeDriver the bot should use.

Two browsers are supported:

- Chrome for Testing, from https://googlechromelabs.github.io/chrome-for-testing/,
  unzipped into the project folder (``chrome-mac-arm64/``,
  ``chromedriver-mac-arm64/``, ...).
- Chromium, from https://www.chromium.org/, either installed on the system
  or unzipped into the project folder (``chrome-mac/``, ``chromedriver_mac64/``).
"""

import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Chrome for Testing first, then Chromium snapshot downloads.
_CHROME_PATTERNS = (
    "chrome-mac-*/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing",
    "chrome-linux64/chrome",
    "chrome-win64/chrome.exe",
    "chrome-win32/chrome.exe",
    "chrome-mac/Chromium.app/Contents/MacOS/Chromium",
    "chrome-linux/chrome",
    "chrome-win/chrome.exe",
)
_CHROMEDRIVER_PATTERNS = (
    "chromedriver",
    "chromedriver-*/chromedriver",
    "chromedriver-*/chromedriver.exe",
    "chromedriver_*/chromedriver",
    "chromedriver_*/chromedriver.exe",
    "chrome-linux64/chromedriver",
)

INSTALLED_CHROMIUM_PATHS: tuple[Path, ...] = (
    Path("/usr/bin/chromium"),
    Path("/usr/bin/chromium-browser"),
    Path("/snap/bin/chromium"),
    Path("/Applications/Chromium.app/Contents/MacOS/Chromium"),
    Path.home() / "Applications/Chromium.app/Contents/MacOS/Chromium",
    Path(os.environ.get("LOCALAPPDATA", "")) / "Chromium/Application/chrome.exe",
)


def _first_file(root: Path, patterns: tuple[str, ...]) -> str | None:
    for pattern in patterns:
        for path in sorted(root.glob(pattern)):
            if path.is_file():
                return str(path)
    return None


def find_local_chrome(root: Path = PROJECT_ROOT) -> str | None:
    """Return Chrome for Testing or Chromium, if one was unzipped into ``root``."""
    return _first_file(root, _CHROME_PATTERNS)


def find_local_chromedriver(root: Path = PROJECT_ROOT) -> str | None:
    """Return the ChromeDriver in ``root``, if one was unzipped there."""
    return _first_file(root, _CHROMEDRIVER_PATTERNS)


def find_installed_chromium(candidates: tuple[Path, ...] | None = None) -> str | None:
    """Return a Chromium installed on the system (apt, snap, Homebrew, installer)."""
    for path in INSTALLED_CHROMIUM_PATHS if candidates is None else candidates:
        if path.is_file():
            return str(path)
    return None


def find_browser(root: Path = PROJECT_ROOT) -> str | None:
    """Return the browser to launch, or None to let Selenium choose.

    Order: ``CHROME_BINARY``, a browser unzipped into ``root``, then an
    installed Chromium.
    """
    return (
        os.environ.get("CHROME_BINARY", "").strip()
        or find_local_chrome(root)
        or find_installed_chromium()
    )
