"""Centralized test data.

saucedemo.com exposes a fixed set of demo accounts, all sharing the same
password. Keeping them here (instead of hardcoding in tests) makes it a
single place to update if the site ever changes credentials, and keeps
tests readable.
"""

PASSWORD = "secret_sauce"

USERS = {
    "standard": "standard_user",
    "locked_out": "locked_out_user",
    "problem": "problem_user",
    "performance_glitch": "performance_glitch_user",
    "error": "error_user",
    "visual": "visual_user",
}

CHECKOUT_INFO = {
    "first_name": "Funmilola",
    "last_name": "Olorode",
    "postal_code": "EC1A 1BB",
}
