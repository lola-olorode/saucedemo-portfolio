"""Environment configuration layer.

Lets the same suite target different environments without touching test
code — set the ENV variable and everything (base URL, timeouts, etc.)
switches. This mirrors how a real product usually has separate
dev/staging/prod targets and you don't want environment details scattered
across test files.

Usage:
    ENV=staging pytest          # runs against staging
    pytest                      # defaults to "prod" (public saucedemo.com)
"""

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class EnvironmentConfig:
    name: str
    base_url: str
    default_timeout: int


ENVIRONMENTS = {
    # saucedemo.com only exposes one public target, so "staging" here
    # points at the same host — in a real project each key would point
    # at a genuinely different deployment (e.g. staging.myapp.com).
    "prod": EnvironmentConfig(
        name="prod",
        base_url="https://www.saucedemo.com/",
        default_timeout=10,
    ),
    "staging": EnvironmentConfig(
        name="staging",
        base_url="https://www.saucedemo.com/",
        default_timeout=15,  # staging environments are often slower
    ),
}


def get_environment() -> EnvironmentConfig:
    env_name = os.getenv("ENV", "prod").lower()
    if env_name not in ENVIRONMENTS:
        raise ValueError(
            f"Unknown ENV '{env_name}'. Valid options: {list(ENVIRONMENTS)}"
        )
    return ENVIRONMENTS[env_name]
