import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from config.test_data import USERS, PASSWORD
from config.environments import get_environment
from utils.logger import get_logger
from utils.screenshot import capture_screenshot

log = get_logger(__name__)


def _build_driver():
    options = Options()
    # CI runs headless; set HEADED=1 locally if you want to watch the browser
    if os.getenv("HEADED") != "1":
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1400,1000")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


@pytest.fixture
def driver():
    env = get_environment()
    log.info("Starting browser | environment=%s | base_url=%s", env.name, env.base_url)
    drv = _build_driver()
    drv.implicitly_wait(1)
    yield drv
    log.info("Quitting browser")
    drv.quit()


@pytest.fixture
def logged_in_driver(driver):
    """Returns a driver already authenticated as the standard user,
    landed on the inventory page. Saves every test that needs a logged-in
    session from repeating the login steps."""
    log.info("Logging in as standard_user")
    login_page = LoginPage(driver)
    login_page.load()
    login_page.login(USERS["standard"], PASSWORD)
    InventoryPage(driver).is_loaded()
    return driver


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """On failure, grab a screenshot from any 'driver' or 'logged_in_driver'
    fixture the failing test used, and log it clearly for CI triage."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver") or item.funcargs.get("logged_in_driver")
        if driver is not None:
            path = capture_screenshot(driver, item.nodeid)
            log.error("Test failed: %s | screenshot saved to %s", item.nodeid, path)
