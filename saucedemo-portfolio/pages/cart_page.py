from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CartPage(BasePage):
    CART_ITEM = (By.CLASS_NAME, "cart_item")
    REMOVE_BACKPACK = (By.ID, "remove-sauce-labs-backpack")
    CHECKOUT_BUTTON = (By.ID, "checkout")

    def get_item_count(self) -> int:
        return len(self.find_all(self.CART_ITEM))

    def remove_backpack(self):
        self.click(self.REMOVE_BACKPACK)
        return self

    def checkout(self):
        self.click(self.CHECKOUT_BUTTON)
        return self
