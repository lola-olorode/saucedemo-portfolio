# SauceDemo Test Automation Framework

A Selenium + pytest UI automation suite for [saucedemo.com](https://www.saucedemo.com/),
built using the **Page Object Model (POM)** to keep locators/actions separate
from test logic and to make the suite maintainable as the app under test grows.

## Why this project

This started as a way to demonstrate hands-on automation framework design —
not just writing individual test scripts, but structuring a suite the way
you'd maintain one on a real product: reusable page objects, shared fixtures,
parametrized data-driven tests, CI integration, and HTML reporting.

## Architecture

```
saucedemo-automation/
├── pages/                   # Page Object Model — one class per screen
│   ├── base_page.py         # Shared wait/interaction helpers
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── cart_page.py
│   └── checkout_page.py
├── tests/                   # UI test suites, grouped by feature
│   ├── test_login.py
│   ├── test_inventory.py
│   └── test_cart_checkout.py
├── api_tests/                # API-layer suite (independent of the UI)
│   ├── api_client.py         # Thin requests wrapper
│   └── test_users_api.py
├── config/
│   ├── environments.py       # dev/staging/prod-style env layering
│   └── test_data.py          # Accounts, checkout data
├── utils/
│   ├── logger.py             # Run-scoped file + console logging
│   └── screenshot.py         # Screenshot-on-failure capture
├── conftest.py                # Fixtures + screenshot-on-failure hook
├── .github/workflows/         # CI: runs the full suite on every push
└── pytest.ini                 # Marker registration, report config
```

**Design decisions:**
- **Page Object Model** — locators and page interactions live in `pages/`,
  so if the UI changes, only one file needs updating, not every test.
- **Fixtures over setup/teardown boilerplate** — `conftest.py` provides a
  `driver` fixture (handles browser lifecycle) and a `logged_in_driver`
  fixture (skips repeating login steps across tests that need an
  authenticated session).
- **Environment layering** — `config/environments.py` selects base URL and
  timeouts via an `ENV` variable, so the same suite can target different
  deployments without editing test code.
- **Structured logging** — every run writes a timestamped log file
  (`reports/logs/`) alongside console output, so CI failures are debuggable
  after the fact, not just in the moment.
- **Screenshot-on-failure** — a `pytest_runtest_makereport` hook in
  `conftest.py` automatically captures a screenshot the instant any UI
  test fails, saved to `reports/screenshots/`.
- **Test tagging** — `smoke`, `regression`, `critical_path`, and `api`
  markers let you run a fast subset (`pytest -m smoke`) on every commit
  and the full suite before a release.
- **API + UI hybrid** — `api_tests/` validates a REST API directly
  (status codes, response shape, CRUD behavior), independent of and much
  faster than driving a browser, using the same pytest/CI setup.
- **Data-driven tests** — `@pytest.mark.parametrize` covers multiple invalid
  login combinations without duplicating test code.
- **CI-first** — GitHub Actions runs the full suite headless on every push
  and uploads the HTML report as a build artifact.

## Coverage

| Area | Scenarios |
|---|---|
| Login (UI) | Valid login, locked-out user, empty/invalid credentials |
| Inventory (UI) | Sort by price (asc/desc), sort by name, add-to-cart badge count |
| Cart & Checkout (UI) | Remove item, full happy-path checkout, required-field validation |
| Users (API) | Get single/list, 404 handling, create, update, delete, auth/header validation |

Manual regression coverage — including exploratory and edge-case scenarios
not (yet) automated, plus a requirement-to-test traceability matrix — is
tracked in [`REGRESSION_SUITE.md`](./REGRESSION_SUITE.md).

## Running locally

```bash
pip install -r requirements.txt
pytest                     # full suite, headless by default
pytest -m smoke             # fast critical-path subset only
pytest -m "regression and not api"   # UI regression suite only
HEADED=1 pytest tests/       # watch UI tests run in a visible browser
ENV=staging pytest           # target a different environment
```

An HTML report is generated at `reports/report.html`, logs at
`reports/logs/`, and failure screenshots at `reports/screenshots/`.

## Tech stack

Python · Selenium WebDriver · pytest · requests · webdriver-manager · GitHub Actions
