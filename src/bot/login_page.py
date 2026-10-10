"""Locate the parts of LinkedIn's sign-in page.

The current page uses generated element IDs and contains two copies of the
form, only one of them visible, so elements are found by type, label and
visibility. Selectors for the older page are kept as fallbacks.
"""

from typing import Any

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By

# A WebDriver or WebElement; anything with find_elements(by, value).
SearchContext = Any

_EMAIL_SELECTORS = (
    "input[type='email']",
    "input[autocomplete^='username']",
    "#username",
    "input[name='session_key']",
)
_PASSWORD_SELECTORS = (
    "input[type='password']",
    "#password",
    "input[name='session_password']",
)
_KEEP_SIGNED_IN_SELECTORS = ("#remember-me-checkbox", "input[name='rememberMe']")


def _is_visible(element: Any) -> bool:
    try:
        return bool(element.is_displayed())
    except StaleElementReferenceException:
        return False


def _first_visible(context: SearchContext, selectors: tuple[str, ...]) -> Any | None:
    for selector in selectors:
        for element in context.find_elements(By.CSS_SELECTOR, selector):
            if _is_visible(element):
                return element
    return None


def find_email_field(context: SearchContext) -> Any | None:
    """Return the visible email/phone field, or None if the page has none."""
    return _first_visible(context, _EMAIL_SELECTORS)


def find_password_field(context: SearchContext) -> Any | None:
    """Return the visible password field, or None if the page has none."""
    return _first_visible(context, _PASSWORD_SELECTORS)


def find_sign_in_button(context: SearchContext) -> Any | None:
    """Return the visible "Sign in" button (not "Sign in with Apple" etc.)."""
    for button in context.find_elements(By.CSS_SELECTOR, "button"):
        if _is_visible(button) and button.text.strip().casefold() == "sign in":
            return button
    return _first_visible(context, ("button[type='submit']",))


def find_keep_signed_in_checkboxes(context: SearchContext) -> list[Any]:
    """Return every "Keep me signed in" checkbox, including hidden styled ones."""
    boxes = [
        box
        for box in context.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")
        if "keep me signed in" in (box.get_attribute("aria-label") or "").casefold()
    ]
    for selector in _KEEP_SIGNED_IN_SELECTORS:
        boxes.extend(context.find_elements(By.CSS_SELECTOR, selector))
    return boxes
