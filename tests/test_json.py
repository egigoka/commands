# Consolidated tests for commands/json.py (unit)

# ---- from test_json9.py ----


import pytest
import tempfile
import os
from commands.json import Json, JsonDict, JsonList
































# Negative tests








# Coverage improvement tests


























# ---- from test_json_coverage.py ----


import pytest
from commands.json import Json, JsonDict, JsonList
import tempfile
import os


class TestJsonCoverage:
    """Tests to improve JSON module coverage"""

    def test_json_call_without_args_returns_string(self):
        """Test Json.__call__() without args returns self.string (line 26)"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write('{"test": "data"}')
            temp_file = f.name

        try:
            j = Json(temp_file)
            # Call without any arguments should return self.string
            result = j()
            assert result == {"test": "data"}
        finally:
            os.unlink(temp_file)

    def test_jsondict_call_without_args_returns_string(self):
        """Test JsonDict.__call__() without args returns self.string (line 112)"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write('{"key": "value"}')
            temp_file = f.name

        try:
            j = JsonDict(temp_file)
            # Call without any arguments should return self.string
            result = j()
            assert result == {"key": "value"}
        finally:
            os.unlink(temp_file)

    def test_jsonlist_call_without_args_returns_string(self):
        """Test JsonList.__call__() without args returns self.string (line 170)"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write('[1, 2, 3]')
            temp_file = f.name

        try:
            j = JsonList(temp_file)
            # Call without any arguments should return self.string
            result = j()
            assert result == [1, 2, 3]
        finally:
            os.unlink(temp_file)

    def test_jsonlist_call_with_value_appends(self, tmp_path):
        target = tmp_path / "list.json"
        target.write_text("[]")

        j = JsonList(str(target))
        result = j(value="x")
        assert result == ["x"]
        assert j.string == ["x"]

    def test_jsondict_file_exists_error_during_create(self, monkeypatch):
        """Test JsonDict handles FileExistsError during file creation (lines 86-87)"""
        from commands.file import File

        # Create temp file path (doesn't exist yet)
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=True) as f:
            temp_file = f.name
        # File is now deleted

        # Mock File.create to raise FileExistsError simulating a race condition
        def mock_create(path, *args, **kwargs):
            # Simulate race: file gets created between check and create
            # Write the file ourselves
            with open(path, 'w') as f:
                f.write('{"existing": "data"}')
            # Then raise FileExistsError as File.create would
            raise FileExistsError(f"File {path} already exists")

        monkeypatch.setattr(File, "create", mock_create)

        try:
            # This should:
            # 1. Check file doesn't exist (passes)
            # 2. Try to create it (raises FileExistsError)
            # 3. Catch the error and continue (lines 86-87)
            # 4. Open and read the existing file
            j = JsonDict(temp_file)
            # Should read the file that "appeared" during race condition
            assert j.string == {"existing": "data"}
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
