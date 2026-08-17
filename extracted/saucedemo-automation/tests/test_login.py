import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from config.test_data import USERS, PASSWORD


class TestLogin:
    @pytest.mark.smoke
    @pytest.mark.critical_path
    def test_valid_login_lands_on_inventory(self, driver):
        login_page = LoginPage(driver).load()
        login_page.login(USERS["standard"], PASSWORD)

        inventory_page = InventoryPage(driver)
        assert inventory_page.is_loaded(), "Expected to land on the inventory page after valid login"

    @pytest.mark.regression
    def test_locked_out_user_is_blocked(self, driver):
        login_page = LoginPage(driver).load()
        login_page.login(USERS["locked_out"], PASSWORD)

        assert login_page.has_error()
        assert "locked out" in login_page.get_error_message().lower()

    @pytest.mark.regression
    @pytest.mark.parametrize(
        "username,password,expected_fragment",
        [
            ("", "", "username is required"),
            (USERS["standard"], "", "password is required"),
            ("not_a_real_user", "wrong_password", "do not match"),
        ],
    )
    def test_invalid_credentials_show_error(self, driver, username, password, expected_fragment):
        login_page = LoginPage(driver).load()
        login_page.login(username, password)

        assert login_page.has_error()
        assert expected_fragment in login_page.get_error_message().lower()
