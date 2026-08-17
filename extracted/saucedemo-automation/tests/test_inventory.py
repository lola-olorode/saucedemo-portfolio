import pytest
from pages.inventory_page import InventoryPage


class TestInventory:
    @pytest.mark.regression
    def test_sort_price_low_to_high(self, logged_in_driver):
        page = InventoryPage(logged_in_driver)
        page.sort_by("lohi")

        prices = page.get_item_prices()
        assert prices == sorted(prices), "Prices should be ascending after low-to-high sort"

    @pytest.mark.regression
    def test_sort_price_high_to_low(self, logged_in_driver):
        page = InventoryPage(logged_in_driver)
        page.sort_by("hilo")

        prices = page.get_item_prices()
        assert prices == sorted(prices, reverse=True), "Prices should be descending after high-to-low sort"

    @pytest.mark.regression
    def test_sort_name_a_to_z(self, logged_in_driver):
        page = InventoryPage(logged_in_driver)
        page.sort_by("az")

        names = page.get_item_names()
        assert names == sorted(names), "Names should be alphabetical after A-Z sort"

    @pytest.mark.smoke
    @pytest.mark.critical_path
    def test_add_to_cart_updates_badge_count(self, logged_in_driver):
        page = InventoryPage(logged_in_driver)
        assert page.get_cart_count() == 0, "Cart should start empty"

        page.add_backpack_to_cart()

        assert page.get_cart_count() == 1, "Cart badge should reflect 1 item after adding"
