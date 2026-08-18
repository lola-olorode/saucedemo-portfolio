from selenium.webdriver.common.by import By
from shared.base_page import BasePage


class InventoryPage(BasePage):
    PAGE_TITLE = (By.CLASS_NAME, "title")
    SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")
    INVENTORY_ITEM = (By.CLASS_NAME, "inventory_item")
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    ITEM_PRICE = (By.CLASS_NAME, "inventory_item_price")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    ADD_TO_CART_BACKPACK = (By.ID, "add-to-cart-sauce-labs-backpack")

    def is_loaded(self) -> bool:
        return self.is_visible(self.PAGE_TITLE, timeout=6)

    def sort_by(self, value: str):
        """value examples: 'az', 'za', 'lohi', 'hilo'"""
        self.select_by_value(self.SORT_DROPDOWN, value)
        return self

    def get_item_names(self):
        return [el.text for el in self.find_all(self.ITEM_NAME)]

    def get_item_prices(self):
        raw = [el.text for el in self.find_all(self.ITEM_PRICE)]
        return [float(p.replace("$", "")) for p in raw]

    def add_backpack_to_cart(self):
        self.click(self.ADD_TO_CART_BACKPACK)
        return self

    def get_cart_count(self) -> int:
        if self.is_visible(self.CART_BADGE, timeout=3):
            return int(self.get_text(self.CART_BADGE))
        return 0

    def go_to_cart(self):
        self.click(self.CART_LINK)
        return self
