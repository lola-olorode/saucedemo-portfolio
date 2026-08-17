"""Screenshot capture helper.

Wired into a pytest hook (see conftest.py) so any failing UI test
automatically saves a screenshot at the moment of failure — the single
most useful thing to have when triaging a red build in CI.
"""

import os
from datetime import datetime


SCREENSHOT_DIR = "reports/screenshots"


def capture_screenshot(driver, test_name: str) -> str:
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = test_name.replace("/", "_").replace("::", "__")
    path = f"{SCREENSHOT_DIR}/{safe_name}_{timestamp}.png"
    driver.save_screenshot(path)
    return path
