"""Menu component.

The burger-menu (logout, reset app state, external links) appears
identically on every logged-in screen in the app. Modeling it as a
component rather than duplicating its locators in every page object
means one update here fixes it everywhere it's used — the same reason
a real app extracts a shared nav/drawer into its own class instead of
copy-pasting it onto each page.
"""

from selenium.webdriver.common.by import By
from shared.base_page import BasePage


class MenuComponent(BasePage):
    MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    CLOSE_BUTTON = (By.ID, "react-burger-cross-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")
    RESET_APP_STATE_LINK = (By.ID, "reset_sidebar_link")
    ALL_ITEMS_LINK = (By.ID, "inventory_sidebar_link")

    def open_menu(self):
        self.click(self.MENU_BUTTON)
        return self

    def close_menu(self):
        self.click(self.CLOSE_BUTTON)
        return self

    def logout(self):
        self.open_menu()
        self.click(self.LOGOUT_LINK)
        return self

    def reset_app_state(self):
        self.open_menu()
        self.click(self.RESET_APP_STATE_LINK)
        self.close_menu()
        return self
