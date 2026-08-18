from shared.base_flow import BaseFlow
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from dataloader.checkout_data_loader import load_checkout_info


class CheckoutFlow(BaseFlow):
    def complete_checkout(self, cart_page: CartPage, info_key: str = "default") -> CheckoutPage:
        self.step("Complete checkout from an already-populated cart")
        cart_page.checkout()

        checkout_page = CheckoutPage(self.driver)
        info = load_checkout_info(info_key)
        checkout_page.fill_information(**info)
        checkout_page.finish()
        return checkout_page
