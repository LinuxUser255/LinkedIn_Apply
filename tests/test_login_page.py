"""Tests for locating LinkedIn sign-in page elements."""

from dataclasses import dataclass, field

from src.bot import login_page


@dataclass
class FakeElement:
    css: str
    displayed: bool = True
    text: str = ""
    attributes: dict[str, str] = field(default_factory=dict)

    def is_displayed(self) -> bool:
        return self.displayed

    def get_attribute(self, name: str) -> str | None:
        return self.attributes.get(name)


class FakePage:
    """Answers find_elements(By.CSS_SELECTOR, css) from a fixed element list."""

    def __init__(self, *elements: FakeElement) -> None:
        self.elements = elements

    def find_elements(self, by: str, css: str) -> list[FakeElement]:
        return [element for element in self.elements if element.css == css]


def test_finds_visible_copy_of_current_form() -> None:
    hidden_email = FakeElement("input[type='email']", displayed=False)
    email = FakeElement("input[type='email']")
    hidden_password = FakeElement("input[type='password']", displayed=False)
    password = FakeElement("input[type='password']")
    page = FakePage(hidden_email, email, hidden_password, password)

    assert login_page.find_email_field(page) is email
    assert login_page.find_password_field(page) is password


def test_falls_back_to_old_page_ids() -> None:
    email = FakeElement("#username")
    password = FakeElement("#password")
    page = FakePage(email, password)

    assert login_page.find_email_field(page) is email
    assert login_page.find_password_field(page) is password


def test_missing_fields_return_none() -> None:
    page = FakePage(FakeElement("input[type='email']", displayed=False))

    assert login_page.find_email_field(page) is None
    assert login_page.find_password_field(page) is None


def test_sign_in_button_ignores_other_sign_in_options() -> None:
    apple = FakeElement("button", text="Sign in with Apple")
    hidden = FakeElement("button", displayed=False, text="Sign in")
    show_password = FakeElement("button", attributes={"aria-label": "Show password"})
    sign_in = FakeElement("button", text="  Sign in \n")
    page = FakePage(apple, hidden, show_password, sign_in)

    assert login_page.find_sign_in_button(page) is sign_in


def test_sign_in_button_falls_back_to_submit_button() -> None:
    submit = FakeElement("button[type='submit']", text="Continue")
    page = FakePage(FakeElement("button", text="Sign in with Apple"), submit)

    assert login_page.find_sign_in_button(page) is submit


def test_sign_in_button_none_when_absent() -> None:
    assert login_page.find_sign_in_button(FakePage()) is None


def test_keep_signed_in_checkboxes_include_hidden_ones() -> None:
    current = FakeElement(
        "input[type='checkbox']", displayed=False, attributes={"aria-label": "Keep me signed in"}
    )
    other = FakeElement("input[type='checkbox']", attributes={"aria-label": "Subscribe"})
    old = FakeElement("#remember-me-checkbox", displayed=False)
    page = FakePage(current, other, old)

    assert login_page.find_keep_signed_in_checkboxes(page) == [current, old]
