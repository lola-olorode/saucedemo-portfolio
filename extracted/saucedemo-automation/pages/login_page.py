from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.environments import get_environment


class LoginPage(BasePage):
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    def load(self):
        return self.open(get_environment().base_url)

    def login(self, username: str, password: str):
        self.type_text(self.USERNAME_INPUT, username)
        self.type_text(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
        return self

    def get_error_message(self) -> str:
        return self.get_text(self.ERROR_MESSAGE)

    def has_error(self) -> bool:
        return self.is_visible(self.ERROR_MESSAGE, timeout=4)
