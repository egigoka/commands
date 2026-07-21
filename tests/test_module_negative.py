# Consolidated tests for commands/module.py (negative)

# ---- from test_module_negative.py ----

# Placeholder for future tests.
import math
import types
import pytest
from commands.module import LazyModule, LazyProperty

def test_lazy_module_optional_missing():
    lazy = LazyModule("module_that_does_not_exist_12345", optional=True)
    assert bool(lazy) is False
    with pytest.raises(ImportError, match="Optional module"):
        _ = lazy.anything
