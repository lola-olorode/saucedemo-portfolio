"""Base Page Object.

All page objects inherit from this class. It centralizes the Selenium
wait/interaction logic so individual page classes stay declarative
(locators + actions) instead of repeating boilerplate WebDriverWait code.
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException

DEFAULT_TIMEOUT = 10

_CLICK_INSTRUMENT_JS = """
arguments[0].__wd_clicked = false;
arguments[0].addEventListener("click", function () {
    this.__wd_clicked = true;
}, { once: true });
"""

_SET_REACT_VALUE_JS = """
var input = arguments[0];
var value = arguments[1];
var setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value").set;
setter.call(input, value);
input.dispatchEvent(new Event("input", { bubbles: true }));
input.dispatchEvent(new Event("change", { bubbles: true }));
"""


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

    # A plain WebDriver click occasionally lands on the element (confirmed
    # by coordinates and elementFromPoint) but never actually fires the
    # page's click handler — observed against saucedemo.com's "Add to
    # cart" buttons on current Chrome/W3C Actions. Rather than switch
    # every click to a JS-dispatched one (which can "click" things a real
    # user couldn't, e.g. a covered or disabled element), this instruments
    # the element with a one-shot listener, does the normal native click,
    # and only falls back to a JS click if the native one demonstrably
    # never reached the element.
    def click(self, locator):
        el = self.wait.until(EC.element_to_be_clickable(locator))
        self.driver.execute_script(_CLICK_INSTRUMENT_JS, el)

        el.click()
        if not self._click_registered(el):
            self.driver.execute_script("arguments[0].click();", el)
        return self

    def _click_registered(self, el) -> bool:
        try:
            return bool(self.driver.execute_script("return !!arguments[0].__wd_clicked;", el))
        except StaleElementReferenceException:
            # The click legitimately navigated or re-rendered the page —
            # that's evidence it worked, not that it failed.
            return True

    # Same class of problem as click(), on the input side: native
    # send_keys occasionally leaves a React-controlled field's DOM value
    # unchanged (observed on the checkout form) even though no error is
    # raised. This verifies the value actually landed and, if not, sets
    # it through React's own native input setter plus a real
    # "input"/"change" event — the standard way to update a
    # React-controlled field from outside React — so the app's own state
    # updates exactly as it would for a user typing.
    def type_text(self, locator, text: str):
        el = self.find(locator)
        el.clear()
        el.send_keys(text)
        if self.driver.execute_script("return arguments[0].value;", el) != text:
            self.driver.execute_script(_SET_REACT_VALUE_JS, el, text)
        return self

    def get_text(self, locator) -> str:
        return self.find(locator).text

    def is_visible(self, locator, timeout: int = DEFAULT_TIMEOUT) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def select_by_value(self, locator, value: str):
        from selenium.webdriver.support.ui import Select

        Select(self.find(locator)).select_by_value(value)
        return self
