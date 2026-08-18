from shared.base_flow import BaseFlow
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from dataloader.user_loader import get_user


class AuthFlow(BaseFlow):
    def login_as(self, user_key: str = "standard"):
        self.step(f"Log in as fixture user '{user_key}'")
        user = get_user(user_key)

        login_page = LoginPage(self.driver)
        login_page.load()
        login_page.login(user["username"], user["password"])
        return login_page

    def login_and_reach_inventory(self, user_key: str = "standard") -> InventoryPage:
        self.login_as(user_key)
        inventory_page = InventoryPage(self.driver)
        inventory_page.is_loaded()
        return inventory_page
