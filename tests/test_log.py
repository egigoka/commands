# Consolidated tests for commands/log.py (unit)

# ---- from test_log9.py ----


import pytest
from commands.log import Logger


def test_logger_exists():
    logger = Logger()
    assert logger is not None


def test_logger_is_class():
    assert isinstance(Logger, type)
