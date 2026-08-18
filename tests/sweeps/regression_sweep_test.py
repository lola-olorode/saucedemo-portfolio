"""Regression sweep.

Broader than the smoke sweep — exercises the purchase journey across
multiple fixture accounts, the kind of thing run before a release rather
than on every commit. Feature-level edge cases (invalid input, single-page
checks) stay in tests/core/; this file is specifically about coverage
breadth across data variations.
"""

import pytest
from flows.auth_flow import AuthFlow
from flows.shopping_flow import ShoppingFlow
from flows.checkout_flow import CheckoutFlow


@pytest.mark.regression
@pytest.mark.parametrize("user_key", ["standard", "performance_glitch"])
def test_regression_purchase_journey_across_accounts(driver, user_key):
    AuthFlow(driver).login_and_reach_inventory(user_key)
    cart = ShoppingFlow(driver).add_backpack_and_view_cart()
    checkout = CheckoutFlow(driver).complete_checkout(cart)

    assert "thank you" in checkout.get_completion_header().lower()
