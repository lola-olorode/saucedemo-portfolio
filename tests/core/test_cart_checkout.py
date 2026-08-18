import pytest
from pages.checkout_page import CheckoutPage
from flows.shopping_flow import ShoppingFlow
from flows.checkout_flow import CheckoutFlow
from dataloader.checkout_data_loader import load_checkout_info


class TestCartAndCheckout:
    @pytest.mark.regression
    def test_remove_item_from_cart(self, logged_in_driver):
        cart = ShoppingFlow(logged_in_driver).add_backpack_and_view_cart()
        assert cart.get_item_count() == 1

        cart.remove_backpack()
        assert cart.get_item_count() == 0

    @pytest.mark.smoke
    @pytest.mark.critical_path
    def test_full_checkout_happy_path(self, logged_in_driver):
        cart = ShoppingFlow(logged_in_driver).add_backpack_and_view_cart()
        checkout = CheckoutFlow(logged_in_driver).complete_checkout(cart)

        assert "thank you" in checkout.get_completion_header().lower()

    @pytest.mark.regression
    def test_checkout_requires_first_name(self, logged_in_driver):
        cart = ShoppingFlow(logged_in_driver).add_backpack_and_view_cart()
        cart.checkout()

        checkout = CheckoutPage(logged_in_driver)
        info = load_checkout_info("default")
        checkout.fill_information(first_name="", last_name=info["last_name"], postal_code=info["postal_code"])

        assert "first name is required" in checkout.get_error_message().lower()
