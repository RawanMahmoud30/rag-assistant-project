"""
Centralized logging configuration.

Call `configure_logging()` once, at application startup, so every module
that does `logging.getLogger(__name__)` produces consistent, readable logs.
"""

import logging
import sys


def configure_logging(level: int = logging.INFO) -> None:
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
