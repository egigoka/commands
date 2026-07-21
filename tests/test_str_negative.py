# Consolidated tests for commands/str.py (negative)

# ---- from test_str_missing_coverage.py ----


#! python3
# -*- coding: utf-8 -*-
from commands.str import Str
from unittest.mock import patch

"""Tests for missing coverage in str.py module"""
import pytest
from commands import Str



    # Note: Lines 227-228 are unreachable dead code because lines 204-206
    # already handle the bytes case before we get to line 226.

class TestStrNewlines:
    """Tests for newline handling methods"""
    def test_newlines_to_strings_invalid_type(self):
        with pytest.raises(TypeError, match="can't be split"):
            Str.newlines_to_strings(123)

class TestStrSplitEvery:
    """Tests for split_every method"""
    def test_split_every_invalid_chars(self):
        with pytest.raises(ValueError):
            Str.split_every("test", 0)
        with pytest.raises(ValueError):
            Str.split_every("test", -1)
    def test_split_every_unsupported_type(self):
        with pytest.raises(ValueError, match="isn't supported"):
            Str.split_every([1, 2, 3], 2)

class TestStrSubstring:
    """Tests for substring method"""
    def test_substring_not_found(self):
        with pytest.raises(KeyError, match="was not found"):
            Str.substring("hello world", "missing", safe=False)
    def test_substring_custom_exception_message(self):
        with pytest.raises(KeyError, match="Custom error"):
            Str.substring("test", "missing", exception_message="Custom error")

class TestStrCoverage:
    """Tests to improve coverage for str9.py"""
    def test_substring_after_not_found_exception(self):
        """Test substring raises exception when after not found (lines 208-212)"""
        with pytest.raises(KeyError, match="that followed"):
            Str.substring("hello world", "hello ", "missing", safe=False)
    def test_guid_by_seed_duplicate_raises(self):
        """Test guid_by_seed raises on duplicate seed (lines 361-363)"""
        Str.seeds.clear()
        Str.guid_by_seed("duplicate_test", uniq_in_process=True)
        with pytest.raises(KeyError, match="already used"):
            Str.guid_by_seed("duplicate_test", uniq_in_process=True)

class TestStrSubstringEdgeCases:
    """Tests for substring method edge cases"""
    def test_substring_after_not_found_with_exception_message(self):
        """Test substring when after string not found to cover line 241"""
        with pytest.raises(KeyError) as exc_info:
            Str.substring("start test", "start", "end", safe=False,
                        exception_message="Custom error")
        assert "Custom error" in str(exc_info.value)

class TestStrInputIntMethod:
    """Tests for input_int method to cover lines 291-320"""

    @patch('builtins.input')
    @patch('builtins.print')
    def test_input_int_empty_no_default(self, mock_print, mock_input):
        """Test input_int with empty input and no default"""
        mock_input.side_effect = ["", "789"]
        with pytest.raises(ValueError):
            Str.input_int(message="Enter number: ", debug=True)

    @patch('builtins.input')
    @patch('builtins.print')
    def test_input_int_with_minimum_invalid(self, mock_print, mock_input):
        """Test input_int with value below minimum"""
        mock_input.side_effect = ["5", "15"]
        with pytest.raises(ValueError):
            Str.input_int(message="Enter number: ", minimum=10, debug=True)

    @patch('builtins.input')
    @patch('builtins.print')
    def test_input_int_with_maximum_invalid(self, mock_print, mock_input):
        """Test input_int with value above maximum"""
        mock_input.side_effect = ["25", "15"]
        with pytest.raises(ValueError):
            Str.input_int(message="Enter number: ", maximum=20, debug=True)

class TestStrGuidBySeed:
    """Tests for guid_by_seed method"""
    def test_guid_by_seed_duplicate_error(self):
        """Test guid_by_seed with duplicate seed"""
        seed = "test_seed_duplicate"
        Str.guid_by_seed(seed)
        with pytest.raises(KeyError, match="already used"):
            Str.guid_by_seed(seed, uniq_in_process=True)
