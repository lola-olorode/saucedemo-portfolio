import pytest
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from config.test_data import CHECKOUT_INFO


class TestCartAndCheckout:
    @pytest.mark.regression
    def test_remove_item_from_cart(self, logged_in_driver):
        inventory = InventoryPage(logged_in_driver)
        inventory.add_backpack_to_cart()
        inventory.go_to_cart()

        cart = CartPage(logged_in_driver)
        assert cart.get_item_count() == 1

        cart.remove_backpack()
        assert cart.get_item_count() == 0

    @pytest.mark.smoke
    @pytest.mark.critical_path
    def test_full_checkout_happy_path(self, logged_in_driver):
        inventory = InventoryPage(logged_in_driver)
        inventory.add_backpack_to_cart()
        inventory.go_to_cart()

        cart = CartPage(logged_in_driver)
        cart.checkout()

        checkout = CheckoutPage(logged_in_driver)
        checkout.fill_information(**CHECKOUT_INFO)

        total_text = checkout.get_summary_total_text()
        assert "$" in total_text, "Order summary should show a total"

        checkout.finish()
        assert "thank you" in checkout.get_completion_header().lower()

    @pytest.mark.regression
    def test_checkout_requires_first_name(self, logged_in_driver):
        inventory = InventoryPage(logged_in_driver)
        inventory.add_backpack_to_cart()
        inventory.go_to_cart()

        CartPage(logged_in_driver).checkout()

        checkout = CheckoutPage(logged_in_driver)
        checkout.fill_information(first_name="", last_name="Olorode", postal_code="EC1A 1BB")

        assert "first name is required" in checkout.get_error_message().lower()
