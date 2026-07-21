# Consolidated tests for commands/network.py (negative)

# ---- from test_network_missing_coverage.py ----


#! python3
# -*- coding: utf-8 -*-
from commands.network import Network
import types

"""Tests for missing coverage in network.py module"""
import pytest
from commands import Network


class TestNetworkMissingCoverage:
    """Tests to cover missing lines in network.py"""

    def test_instance_ping_no_target(self):
        """Test instance ping when target is not set (lines 40-42)"""
        net = Network()
        with pytest.raises(ValueError, match="Network target is not set"):
            net.ping()

    def test_instance_get_ip_no_target(self):
        """Test instance get_ip when target is not set (lines 45-47)"""
        net = Network()
        with pytest.raises(ValueError, match="Network target is not set"):
            net.get_ip()

    def test_instance_get_fqdn_no_target(self):
        """Test instance get_fqdn when target is not set (lines 50-52)"""
        net = Network()
        with pytest.raises(ValueError, match="Network target is not set"):
            net.get_fqdn()

    def test_ping_keyboard_interrupt(self, monkeypatch):
        """Test ping with KeyboardInterrupt (lines 133-135)"""
        def mock_ping(*args, **kwargs):
            raise KeyboardInterrupt()

        import commands.os
        monkeypatch.setattr(commands.os.OS, 'ping', staticmethod(mock_ping))

        with pytest.raises(SystemExit):
            Network.ping("127.0.0.1", count=1, verbose=False)

    def test_ping_exception_handling(self, monkeypatch):
        """Test ping with general Exception (lines 136-137)"""
        def mock_ping(*args, **kwargs):
            raise RuntimeError("Network error")

        import commands.os
        monkeypatch.setattr(commands.os.OS, 'ping', staticmethod(mock_ping))

        result = Network.ping("invalid-host", count=1, verbose=False)
        assert result is False

    def test_ping_missing_os_ping(self, monkeypatch):
        """Test ping when OS ping function is unavailable (line 148)."""
        import commands.os
        monkeypatch.setattr(commands.os.OS, "ping", None)

        result = Network.ping("127.0.0.1", count=1, verbose=False)
        assert result is False

    def test_check_response_debug_no_output(self, monkeypatch, capsys):
        """Test check_response with debug=True when output is False (lines 407-408)"""
        import requests

        class MockResponse:
            status_code = 200
            content = b"wrong content"

        def mock_get(*args, **kwargs):
            return MockResponse()

        monkeypatch.setattr(requests, 'get', mock_get)

        result = Network.check_response("http://test.com", "expected", debug=True)

        assert result is False
        captured = capsys.readouterr()
        # Should print debug info
        assert "Status:" in captured.out
        assert "Content:" in captured.out

def test_network_get_protocol_of_url_raises():
    with pytest.raises(KeyError):
        Network.get_protocol_of_url("example.com")

def test_network_get_protocol_of_url_no_protocol():
    """Should raise KeyError when URL has no protocol"""
    with pytest.raises(KeyError):
        Network.get_protocol_of_url("just-a-domain.com")

def test_network_get_protocol_of_url_invalid():
    """Should raise KeyError for malformed URL"""
    with pytest.raises(KeyError):
        Network.get_protocol_of_url("not a url at all")

def test_network_callable_missing_target():
    n = Network()
    with pytest.raises(ValueError):
        n()

def test_network_domain_missing_target():
    n = Network()
    with pytest.raises(ValueError):
        _ = n.domain

def test_network_class_get_ip_requires_domain():
    with pytest.raises(TypeError):
        Network.get_ip()

def test_network_call_requires_target():
    net = Network()
    with pytest.raises(ValueError):
        net()

def test_network_instance_domain_and_ip_require_target():
    net = Network()
    with pytest.raises(ValueError):
        _ = net.domain
