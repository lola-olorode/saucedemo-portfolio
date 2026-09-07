from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from shared.base_page import BasePage


class CartPage(BasePage):
    CART_ITEM = (By.CLASS_NAME, "cart_item")
    REMOVE_BACKPACK = (By.ID, "remove-sauce-labs-backpack")
    CHECKOUT_BUTTON = (By.ID, "checkout")

    def get_item_count(self) -> int:
        # find_all waits for at least one match (presence_of_element_located),
        # so an empty cart — a legitimate state, not a failure — times out
        # rather than returning []. Catch that and report 0.
        try:
            return len(self.find_all(self.CART_ITEM))
        except TimeoutException:
            return 0

    def remove_backpack(self):
        self.click(self.REMOVE_BACKPACK)
        return self

    def checkout(self):
        self.click(self.CHECKOUT_BUTTON)
        return self
