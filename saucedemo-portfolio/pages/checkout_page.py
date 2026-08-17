from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CheckoutPage(BasePage):
    # Step One - information form
    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    POSTAL_CODE = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    # Step Two - overview
    FINISH_BUTTON = (By.ID, "finish")
    SUMMARY_TOTAL = (By.CLASS_NAME, "summary_total_label")

    # Step Three - complete
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")

    def fill_information(self, first_name: str, last_name: str, postal_code: str):
        self.type_text(self.FIRST_NAME, first_name)
        self.type_text(self.LAST_NAME, last_name)
        self.type_text(self.POSTAL_CODE, postal_code)
        self.click(self.CONTINUE_BUTTON)
        return self

    def get_error_message(self) -> str:
        return self.get_text(self.ERROR_MESSAGE)

    def get_summary_total_text(self) -> str:
        return self.get_text(self.SUMMARY_TOTAL)

    def finish(self):
        self.click(self.FINISH_BUTTON)
        return self

    def get_completion_header(self) -> str:
        return self.get_text(self.COMPLETE_HEADER)
