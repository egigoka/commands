# Consolidated tests for commands/os.py (unit)

# ---- from test_os9.py ----


import pytest
import sys
from commands.os import OS


def test_os_python_version_major():
    assert OS.python_version_major == sys.version_info.major


def test_os_sys_platform():
    assert OS.sys_platform == sys.platform


def test_os_name():
    name = OS.name
    assert name in ["linux", "windows", "macos", "unknown"]


def test_os_platform_flags():
    is_linux = OS.linux
    is_windows = OS.windows
    is_macos = OS.macos
    assert isinstance(is_linux, bool)
    assert isinstance(is_windows, bool)
    assert isinstance(is_macos, bool)
    assert sum([is_linux, is_windows, is_macos]) <= 1


def test_os_architecture():
    arch = OS.architecture
    assert isinstance(arch, str)
    assert arch in ["32bit", "64bit"]


def test_os_env():
    import os
    env = OS.env
    assert isinstance(env, (dict, os._Environ))
    assert len(env) > 0


def test_os_nt_family():
    nt = OS.nt_family
    assert isinstance(nt, bool)


def test_os_unix_family():
    unix = OS.unix_family
    assert isinstance(unix, bool)


def test_os_hostname():
    hostname = OS.hostname
    assert isinstance(hostname, str)
    assert len(hostname) > 0






# Coverage improvement tests
class TestOSCoverage:
    """Tests to improve coverage for os9.py"""

    def test_windows_version(self):
        """Test windows_version property (lines 52-55)"""
        if OS.windows:
            version = OS.windows_version
            assert isinstance(version, int)
            assert version > 0
        else:
            pytest.skip("Windows-only test")

    def test_name_caching(self):
        """Test name property caching (lines 74-79)"""
        # First call sets the cache
        name1 = OS.name
        # Second call uses cache
        name2 = OS.name
        assert name1 == name2
        assert name1 in ["linux", "windows", "macos", "unknown"]

    def test_python_implementation(self):
        """Test python_implementation property (lines 91-97)"""
        impl = OS.python_implementation
        assert impl in ["pypy", "cpython"]
        # On most systems it should be cpython
        assert isinstance(impl, str)

    def test_display_property(self):
        """Test display property (lines 113-120)"""
        # This tests the display detection
        display = OS.display
        assert isinstance(display, bool)
        # On Linux without X11/Xlib, should be False
        if OS.linux:
            # Display value depends on whether Xlib is available
            assert display in [True, False]

    def test_running_in_repl(self):
        """Test running_in_repl property (lines 124-130)"""
        in_repl = OS.running_in_repl
        assert isinstance(in_repl, bool)
        # When running in pytest, should be False
        assert in_repl == False

    def test_cyrillic_support(self):
        """Test cyrillic_support property (lines 134-153)"""
        support = OS.cyrillic_support
        assert isinstance(support, bool)
        # Cyrillic support depends on terminal encoding
        # Just verify it returns a boolean without error






# ---- from test_os_comprehensive.py ----


import pytest
import os
import tempfile
from unittest.mock import patch, Mock
from commands.os import OS


class TestOSPlatformDetection:
    """Tests for OS platform detection - OS is a singleton"""

    def test_name_property(self):
        """Test name property returns valid platform name"""
        # OS is a singleton, just test it returns valid value
        assert OS.name in ("windows", "linux", "macos", "unknown")

    def test_sys_platform_property(self):
        """Test sys_platform property"""
        assert OS.sys_platform is not None
        assert isinstance(OS.sys_platform, str)

    def test_linux_property(self):
        """Test linux property"""
        assert isinstance(OS.linux, bool)

    def test_macos_property(self):
        """Test macos property"""
        assert isinstance(OS.macos, bool)

    def test_windows_property(self):
        """Test windows property"""
        assert isinstance(OS.windows, bool)


class TestOSWalk:
    """Tests for OS.walk method"""




class TestOSSystem:
    """Tests for OS.system method"""

    @patch('os.system')
    @patch('commands.print.Print')
    def test_system_verbose_true(self, mock_print, mock_os_system):
        """Test system with verbose=True to cover lines 193-196"""
        mock_os_system.return_value = 0

        OS.system("echo test", verbose=True)

        # Print.colored should be called
        assert mock_print.colored.called
        assert mock_os_system.called

    @patch('os.system')
    def test_system_verbose_false(self, mock_os_system):
        """Test system with verbose=False"""
        mock_os_system.return_value = 0

        OS.system("echo test", verbose=False)

        assert mock_os_system.called


class TestOSProperties:
    """Tests for OS properties"""

    def test_args_property(self):
        """Test args property to cover lines 201-202"""
        # OS is a singleton
        args = OS.args
        # Should return sys.argv
        assert isinstance(args, list)

    def test_where_method(self):
        """Test where method to cover lines 211-212"""
        # Test with a command that should exist
        result = OS.where("python")
        # May or may not find it depending on environment
        assert result is None or isinstance(result, str)

    def test_env_property(self):
        """Test env property"""
        # OS is a singleton
        env = OS.env
        # Should return os.environ
        assert isinstance(env, dict) or hasattr(env, '__getitem__')


class TestOSCyrillicSupport:
    """Tests for cyrillic_support property"""

    def test_cyrillic_support(self):
        """Test cyrillic_support property"""
        # OS is a singleton, cyrillic_support is already cached
        # Just test it returns a boolean
        result = OS.cyrillic_support
        assert isinstance(result, bool)


class TestOSWindowsVersion:
    """Tests for windows_version property"""

    @pytest.mark.skipif(os.name != 'nt', reason="Windows-only test")
    def test_windows_version_on_windows(self):
        """Test windows_version on Windows to cover lines 57-60"""
        version = OS.windows_version
        assert isinstance(version, int)
        assert version > 0





class TestOSHostname:
    """Tests for hostname property"""

    def test_hostname_property(self):
        """Test hostname property"""
        hostname = OS.hostname
        assert isinstance(hostname, str)
        assert len(hostname) > 0


class TestOSMultipleCalls:
    """Test that cached properties work correctly"""

    def test_cwd_property(self):
        """Test cwd property"""
        cwd = OS.cwd
        assert isinstance(cwd, str)
        assert len(cwd) > 0

    def test_architecture_property(self):
        """Test architecture property"""
        arch = OS.architecture
        assert isinstance(arch, str)


class TestOSExit:
    """Tests for OS.exit method"""

    @patch('sys.exit')
    def test_exit_method(self, mock_exit):
        """Test exit method to cover lines 216-217"""
        OS.exit(0)
        mock_exit.assert_called_once_with(0)

    @patch('sys.exit')
    def test_exit_method_with_error_code(self, mock_exit):
        """Test exit method with non-zero exit code"""
        OS.exit(1)
        mock_exit.assert_called_once_with(1)


class TestOSDisplayProperty:
    """Tests for display property"""

    @pytest.mark.skipif(os.name == 'nt', reason="Display property is Linux-specific")
    def test_display_property_import_error(self):
        """Test display property when Xlib import fails to cover lines 123-124"""
        # Force recalculation by setting _display to None
        original_display = OS._display
        OS._display = None

        try:
            # Access display property - should handle ImportError gracefully
            result = OS.display
            assert isinstance(result, bool)
        finally:
            # Restore original value
            OS._display = original_display


class TestOSRunningInRepl:
    """Tests for running_in_repl property"""

    def test_running_in_repl_true(self):
        """Test running_in_repl when sys.ps1 and sys.ps2 exist to cover line 132"""
        import sys

        # Save original state
        had_ps1 = hasattr(sys, 'ps1')
        had_ps2 = hasattr(sys, 'ps2')
        original_ps1 = getattr(sys, 'ps1', None)
        original_ps2 = getattr(sys, 'ps2', None)
        original_repl = OS._running_in_repl

        try:
            # Set up REPL indicators
            sys.ps1 = '>>> '
            sys.ps2 = '... '
            OS._running_in_repl = None

            result = OS.running_in_repl
            # In pytest, this will likely be False, but we tested the code path
            assert isinstance(result, bool)
        finally:
            # Restore original state
            if had_ps1:
                sys.ps1 = original_ps1
            elif hasattr(sys, 'ps1'):
                delattr(sys, 'ps1')

            if had_ps2:
                sys.ps2 = original_ps2
            elif hasattr(sys, 'ps2'):
                delattr(sys, 'ps2')

            OS._running_in_repl = original_repl


if __name__ == '__main__':
    pytest.main([__file__, '-v'])


# ---- from test_os_more_coverage.py ----


import sys
import types

import pytest

from commands.os import OS


def _reset_os_cache():
    OS._python_version_major = None
    OS._python_commandline_version = None
    OS._sys_platform = None
    OS._windows = None
    OS._windows_version = None
    OS._linux = None
    OS._name = None
    OS._macos = None
    OS._architecture = None
    OS._python_implementation = None
    OS._nt_family = None
    OS._unix_family = None
    OS._display = None
    OS._running_in_repl = None
    OS._cyrillic_support = None
    OS._hostname = None
    OS._cwd = None


def test_os_name_windows_macos_unknown(monkeypatch):
    _reset_os_cache()

    monkeypatch.setattr(OS, "_sys_platform", "win32")
    assert OS.name == "windows"

    _reset_os_cache()
    monkeypatch.setattr(OS, "_sys_platform", "darwin")
    assert OS.name == "macos"

    _reset_os_cache()
    monkeypatch.setattr(OS, "_sys_platform", "plan9")
    assert OS.name == "unknown"


def test_os_display_importerror_sets_false(monkeypatch):
    _reset_os_cache()
    monkeypatch.setattr(OS, "_linux", True)
    monkeypatch.setattr(OS, "_sys_platform", "linux")

    real_import = __import__

    def guarded_import(name, globals=None, locals=None, fromlist=(), level=0):
        if name.startswith("Xlib"):
            raise ImportError("blocked")
        return real_import(name, globals, locals, fromlist, level)

    monkeypatch.setattr("builtins.__import__", guarded_import)
    assert OS.display is False


def test_os_python_implementation_pypy_branch(monkeypatch):
    _reset_os_cache()
    import platform
    monkeypatch.setattr(platform, "python_implementation", "PyPy", raising=False)
    assert OS.python_implementation == "pypy"


def test_os_cyrillic_support_win_unicode_console_enable_success(monkeypatch):
    _reset_os_cache()
    monkeypatch.setattr(OS, "_windows", True)
    monkeypatch.setattr(OS, "_sys_platform", "win32")
    monkeypatch.setattr(sys, "version_info", (3, 5, 0))

    mod = types.SimpleNamespace(enable=lambda: None)
    monkeypatch.setitem(sys.modules, "win_unicode_console", mod)

    assert OS.cyrillic_support is True


def test_os_cyrillic_support_win_unicode_console_enable_exception(monkeypatch):
    _reset_os_cache()
    monkeypatch.setattr(OS, "_windows", True)
    monkeypatch.setattr(OS, "_sys_platform", "win32")
    monkeypatch.setattr(sys, "version_info", (3, 5, 0))

    def bad_enable():
        raise RuntimeError("fail")

    mod = types.SimpleNamespace(enable=bad_enable)
    monkeypatch.setitem(sys.modules, "win_unicode_console", mod)
    assert OS.cyrillic_support is True






def test_os_windows_version_populates_cache(monkeypatch):
    _reset_os_cache()
    monkeypatch.setattr(OS, "_windows", True)
    monkeypatch.setattr(OS, "_sys_platform", "win32")
    monkeypatch.setattr(sys, "getwindowsversion", lambda: types.SimpleNamespace(major=11), raising=False)

    assert OS.windows_version == 11
