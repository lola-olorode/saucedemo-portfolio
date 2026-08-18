"""User dataloader.

Loads account fixtures from dataloader/fixtures/users.json rather than
hardcoding credentials in test files. Keeping test data as data (not
code) means new accounts/environments can be added without touching any
spec, and mirrors how a larger suite typically separates "what data are
we testing with" from "what are we testing."
"""

import json
from pathlib import Path

FIXTURE_PATH = Path(__file__).parent / "fixtures" / "users.json"


def load_users() -> dict:
    with open(FIXTURE_PATH) as f:
        return json.load(f)


def get_user(key: str) -> dict:
    users = load_users()
    if key not in users:
        raise KeyError(f"No fixture user named '{key}'. Available: {list(users)}")
    return users[key]
