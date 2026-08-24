# Python RPA with Page Object Model (POM)

## What POM Is and Why It Applies to RPA

Page Object Model is a design pattern originating in the Selenium test-automation community
(documented in Selenium's official design-patterns guide) that encapsulates each UI screen (or
each reusable UI region) as a class: the class exposes locators and actions, callers never touch
raw selectors directly. It applies to RPA for the same reason it applies to test automation — an
RPA bot and a UI test suite both do the same thing structurally (locate elements, act on them,
read results), so the same separation-of-concerns pattern pays off.

**Problem POM solves:** without it, UI selectors and business logic are interleaved throughout the
codebase. When the target application's UI changes, every workflow/script referencing that element
must be found and fixed individually. With POM, the element and the interaction method live in
exactly one place — the page class.

**When to use it:** any web-based (Selenium/Playwright) or desktop (pywinauto) Python automation
project with more than one target screen, more than one automation script reusing the same screen,
or an expected maintenance lifetime beyond a single throwaway run. Skip it for genuinely one-off,
single-page, single-use scripts — the abstraction overhead isn't justified there.

## Project Structure (aligned to `uv` + `pyproject.toml` conventions)

```text
rpa_project/
├── pyproject.toml            # uv-managed, Python 3.12, [tool.ruff] + [tool.mypy] sections
├── README.md
├── .gitignore
├── src/
│   └── rpa_project/
│       ├── __init__.py
│       ├── main.py           # entry point — Producer/Consumer orchestration
│       ├── pages/            # one class per screen/page; locators + actions only
│       │   ├── __init__.py
│       │   ├── base_page.py  # shared wait/interaction helpers, inherited by all pages
│       │   ├── login_page.py
│       │   └── dashboard_page.py
│       ├── components/       # reusable UI regions shared across multiple pages
│       │   ├── __init__.py
│       │   ├── modal_component.py
│       │   └── table_component.py
│       ├── data/              # config + test/reference data, not secrets
│       │   ├── config.yaml
│       │   └── reference_data.json
│       └── utils/
│           ├── __init__.py
│           ├── logger.py     # structured logging setup
│           └── exceptions.py # BusinessException / SystemException classes
└── tests/
    ├── conftest.py           # pytest fixtures (driver/session setup and teardown)
    ├── test_login.py
    └── test_create_user.py
```

Use `src/` layout (not a flat package at repo root) and `pyproject.toml` exclusively — do not
generate `requirements.txt` as the dependency source of truth; if a legacy pipeline step requires
a lockfile format, export it from `uv` rather than hand-maintaining a separate file.

## Layer Responsibilities

| Layer                                                             | Responsibility                                                                                                    | Must NOT contain                                             |
| ----------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| `pages/`                                                          | Locators for one screen + methods that perform actions on that screen (`login(user, pwd)`, `get_error_message()`) | Assertions, business rules, direct references to other pages |
| `components/`                                                     | Locators/actions for a UI region reused across multiple pages (a data table, a modal dialog)                      | Page-specific logic                                          |
| `data/`                                                           | Configuration values, reference/test data                                                                         | Credentials, secrets                                         |
| `utils/`                                                          | Cross-cutting helpers: logging, custom exception classes, retry/wait decorators                                   | Business logic                                               |
| `tests/` (or the Producer/Consumer `main.py` for unattended runs) | Orchestrates pages/components to execute a business flow; makes assertions/decisions                              | Raw selectors                                                |

## Base Page Pattern

```python
"""Base page class providing shared wait and interaction primitives."""
from __future__ import annotations

import logging
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

logger = logging.getLogger(__name__)


class BasePage:
    """Shared behavior for all page objects.

    Attributes:
        driver: Active WebDriver session, injected by the caller (never created
            inside a page object — page objects don't own session lifecycle).
        timeout: Default explicit-wait timeout in seconds, sourced from config.
    """

    def __init__(self, driver: WebDriver, timeout: int = 15) -> None:
        self.driver = driver
        self.timeout = timeout

    def _find(self, locator: tuple[By, str]):
        """Explicit wait for element presence — never use implicit waits or
        fixed `time.sleep()` calls; both are anti-patterns that either race
        the UI or waste time unnecessarily.
        """
        return WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located(locator)
        )
```

```python
"""Login page object: locators and actions for the login screen only."""
from __future__ import annotations

from selenium.webdriver.common.by import By

from rpa_project.pages.base_page import BasePage
from rpa_project.utils.exceptions import BusinessException


class LoginPage(BasePage):
    """Encapsulates the login screen's locators and actions."""

    _USERNAME = (By.ID, "username")
    _PASSWORD = (By.ID, "password")
    _SUBMIT = (By.ID, "login-submit")
    _ERROR_BANNER = (By.CSS_SELECTOR, "[data-testid='login-error']")

    def login(self, username: str, password: str) -> None:
        """Perform login. Raises BusinessException on an expected invalid-credentials
        error; lets any other exception propagate as a system exception."""
        self._find(self._USERNAME).send_keys(username)
        self._find(self._PASSWORD).send_keys(password)
        self._find(self._SUBMIT).click()

        error_elements = self.driver.find_elements(*self._ERROR_BANNER)
        if error_elements:
            raise BusinessException(f"Login rejected: {error_elements[0].text}")
```

Callers (Producer/Consumer `main.py` or a `pytest` test) never construct selectors — they call
`LoginPage(driver).login(user, password)` and handle the resulting `BusinessException`/generic
exception per the same taxonomy used everywhere else in this skill.

## Best Practices

- Descriptive names: `get_invoice_total()`, not `get_val()`.
- Small functions: one action or one logical assertion per method — a page object method that
  performs five unrelated actions defeats the pattern's purpose.
- Never construct or search for a raw selector outside a page/component class.
- `base_page.py` centralizes waiting strategy — explicit waits (`WebDriverWait`) only, never
  `time.sleep()` and never global implicit waits mixed with explicit waits (Selenium explicitly
  documents this combination as producing unpredictable wait times).
- Log at the page-object action level (`logger.info("login.attempt", extra={"username": user})`),
  not just at the orchestration level — this is what makes failures traceable to a specific screen
  interaction during debugging (see the Debugging Methodology section of the main skill).
- Prefer `Playwright` over `Selenium` for new projects where there's no constraint forcing Selenium
  (existing Grid infrastructure, team standardization) — see `references/python-rpa.md`'s tool
  decision table; the POM pattern applies identically to a Playwright-backed page object.

## Relationship to Robot Framework / `rpaframework`

Robot Framework is a separate, keyword-driven automation/test framework; `rpaframework`
(Robocorp) is a library collection built to be consumed either as Robot Framework keywords or
directly as a plain Python API. POM and `rpaframework` are not mutually exclusive: a `pages/`
module can internally use `RPA.Browser.Selenium` (rpaframework's Selenium wrapper) instead of raw
`selenium` if the project already standardizes on `rpaframework` for its retry/logging behavior.
