"""Smoke sweep.

A full end-to-end journey through the app in one test — login through to
order confirmation — run on every commit as a fast "is anything
fundamentally broken" gate, distinct from the feature-level tests in
tests/core/ which check individual behaviors in isolation.
"""

import pytest
from flows.auth_flow import AuthFlow
from flows.shopping_flow import ShoppingFlow
from flows.checkout_flow import CheckoutFlow


@pytest.mark.smoke
def test_smoke_full_purchase_journey(driver):
    AuthFlow(driver).login_and_reach_inventory("standard")
    cart = ShoppingFlow(driver).add_backpack_and_view_cart()
    checkout = CheckoutFlow(driver).complete_checkout(cart)

    assert "thank you" in checkout.get_completion_header().lower()
