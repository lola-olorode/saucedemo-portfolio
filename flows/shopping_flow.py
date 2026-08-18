from shared.base_flow import BaseFlow
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage


class ShoppingFlow(BaseFlow):
    def add_backpack_and_view_cart(self) -> CartPage:
        self.step("Add backpack to cart and navigate to cart page")
        inventory_page = InventoryPage(self.driver)
        inventory_page.add_backpack_to_cart()
        inventory_page.go_to_cart()
        return CartPage(self.driver)

    def sort_inventory(self, sort_value: str) -> InventoryPage:
        self.step(f"Sort inventory by '{sort_value}'")
        inventory_page = InventoryPage(self.driver)
        inventory_page.sort_by(sort_value)
        return inventory_page
