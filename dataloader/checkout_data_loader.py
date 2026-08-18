"""Checkout info dataloader — same pattern as user_loader.py, kept
separate because checkout data and account data change independently
and are owned by different parts of a real test suite in practice."""

import json
from pathlib import Path

FIXTURE_PATH = Path(__file__).parent / "fixtures" / "checkout_info.json"


def load_checkout_info(key: str = "default") -> dict:
    with open(FIXTURE_PATH) as f:
        data = json.load(f)
    if key not in data:
        raise KeyError(f"No fixture checkout info named '{key}'. Available: {list(data)}")
    return data[key]
