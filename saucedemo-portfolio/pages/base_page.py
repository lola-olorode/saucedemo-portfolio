"""Base Page Object.

All page objects inherit from this class. It centralizes the Selenium
wait/interaction logic so individual page classes stay declarative
(locators + actions) instead of repeating boilerplate WebDriverWait code.
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

DEFAULT_TIMEOUT = 10


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, DEFAULT_TIMEOUT)

    def open(self, url: str):
        self.driver.get(url)
        return self

    def find(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_all(self, locator):
        self.wait.until(EC.presence_of_element_located(locator))
        return self.driver.find_elements(*locator)

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()
        return self

    def type_text(self, locator, text: str):
        el = self.find(locator)
        el.clear()
        el.send_keys(text)
        return self

    def get_text(self, locator) -> str:
        return self.find(locator).text

    def is_visible(self, locator, timeout: int = DEFAULT_TIMEOUT) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def select_by_value(self, locator, value: str):
        from selenium.webdriver.support.ui import Select

        Select(self.find(locator)).select_by_value(value)
        return self
