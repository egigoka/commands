# Consolidated tests for commands/network.py (integration)

# ---- from test_network_integration.py ----

# Placeholder for future tests.
import pytest
from commands.network import Network
import types

def test_network_get_ip():
    ip = Network.get_ip("localhost")
    assert ip in ["127.0.0.1", "::1"]
