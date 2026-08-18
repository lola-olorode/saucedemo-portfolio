# SauceDemo Test Automation Framework (Python)

A Selenium + pytest UI automation suite for [saucedemo.com](https://www.saucedemo.com/),
structured as a layered framework — the same architectural pattern I use
in my day-to-day work, applied here to a public site.

A parallel [Ruby/RSpec version](../saucedemo-ruby-automation) exists too,
using the same layered structure in the stack I actually work in.

## Architecture

```
saucedemo-automation/
├── components/            # Reusable widgets shared across multiple pages
│   └── menu_component.py   # The burger menu appears on every logged-in screen
├── flows/                  # Business-journey layer: orchestrates pages into a task
│   ├── auth_flow.py         # Login journeys
│   ├── shopping_flow.py     # Sort / add-to-cart journeys
│   └── checkout_flow.py     # Full checkout journey
├── pages/                  # Page Object Model — one class per screen
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── cart_page.py
│   └── checkout_page.py
├── shared/
│   ├── base_page.py          # Shared wait/interaction helpers for every page
│   ├── base_flow.py          # Shared step-logging for every flow
│   ├── environments.py       # dev/staging/prod-style env layering
│   └── utils/
│       ├── logger.py          # Run-scoped file + console logging
│       └── screenshot.py      # Screenshot-on-failure capture
├── dataloader/              # Test data as data, not hardcoded in specs
│   ├── fixtures/
│   │   ├── users.json
│   │   └── checkout_info.json
│   ├── user_loader.py
│   └── checkout_data_loader.py
├── api_tests/                # API-layer suite (independent of the UI)
├── tests/
│   ├── core/                  # Feature-level tests, one file per screen/feature
│   └── sweeps/                 # Full-journey smoke + regression sweeps
├── conftest.py                 # Fixtures + screenshot-on-failure hook
├── .github/workflows/           # CI: runs the suite on every push
└── pytest.ini
```

**Why layered like this:**
- **`pages/`** know how to interact with one screen. They don't know
  *why* — that's a level up.
- **`flows/`** know the business journey — "log in", "buy something" —
  by composing multiple page objects. A spec that needs "add an item and
  check out" calls one flow method instead of repeating four page-object
  calls; if the checkout journey changes, one flow file changes, not
  every spec that touches checkout.
- **`components/`** hold UI pieces reused across many pages (here, the
  burger menu), so a shared element's locators live in exactly one place.
- **`shared/`** holds cross-cutting concerns every page/flow needs
  (waits, logging, environment config) — nothing feature-specific.
- **`dataloader/`** treats test data as data: fixtures live in JSON,
  loader functions read them. Adding a new test account means editing a
  fixture file, not code.
- **`tests/core/`** covers individual features and edge cases in
  isolation; **`tests/sweeps/`** covers full end-to-end journeys — smoke
  (fast, every commit) and regression (broader, pre-release) — kept
  separate because they serve different purposes and run at different
  times in a CI pipeline.

## Coverage

| Area | Scenarios |
|---|---|
| Login (core) | Valid login, locked-out user, empty/invalid credentials |
| Inventory (core) | Sort by price (asc/desc), sort by name, add-to-cart badge count |
| Cart & Checkout (core) | Remove item, full happy-path checkout, required-field validation |
| Smoke sweep | One full login → shop → checkout journey |
| Regression sweep | Full journey repeated across multiple fixture accounts |
| Users (API) | Get single/list, 404 handling, create, update, delete, auth/header validation |

Manual regression coverage and a requirement-traceability matrix are
tracked in [`REGRESSION_SUITE.md`](./REGRESSION_SUITE.md).

## Running locally

```bash
pip install -r requirements.txt
pytest                      # full suite, headless by default
pytest -m smoke              # fast critical-path subset only
pytest tests/sweeps           # full-journey sweeps only
HEADED=1 pytest tests/core     # watch UI tests run in a visible browser
ENV=staging pytest              # target a different environment
```

An HTML report is generated at `reports/report.html`, logs at
`reports/logs/`, and failure screenshots at `reports/screenshots/`.

## Tech stack

Python · Selenium WebDriver · pytest · requests · webdriver-manager · GitHub Actions
