# Consolidated tests for commands/network.py (integration_negative)

# ---- from test_network_integration_negative.py ----

# Placeholder for future tests.
import pytest
from commands.network import Network
import types

def test_network_get_ip_invalid_domain():
    """Should return 'not found' for invalid domain"""
    result = Network.get_ip("this-domain-definitely-does-not-exist-123456789.invalid")
    assert result == "not found"
