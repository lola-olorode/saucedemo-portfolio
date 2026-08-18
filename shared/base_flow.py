"""Base Flow.

A "flow" sits above the page layer: it orchestrates several page objects
together into one business journey (e.g. "log in and land on inventory",
"add an item and complete checkout"), the same way a real user's task
usually spans more than one screen. Specs call flows for journeys and
call pages directly only for single-screen assertions — that split keeps
journey logic in one reusable place instead of copy-pasted across specs.
"""

from shared.utils.logger import get_logger


class BaseFlow:
    def __init__(self, driver):
        self.driver = driver
        self.log = get_logger(self.__class__.__name__)

    def step(self, description: str):
        """Lightweight step logger — call at the start of each flow method
        so a failure's log output reads as a narrative, not just a stack
        trace."""
        self.log.info("STEP: %s", description)
