# Consolidated tests for commands/json.py (integration_negative)

# ---- from test_json_integration_negative.py ----

# Placeholder for future tests.
import pytest
import tempfile
import os
from commands.json import Json, JsonDict, JsonList

def test_jsondict_raises_on_non_dict():
    with tempfile.TemporaryDirectory() as tmpdir:
        filename = os.path.join(tmpdir, "test.json")
        j = Json(filename, verbose=False)
        j.string = [1, 2, 3]
        j.save(verbose=False)

        with pytest.raises(TypeError):
            JsonDict(filename, verbose=False)

def test_jsonlist_raises_on_non_list():
    with tempfile.TemporaryDirectory() as tmpdir:
        filename = os.path.join(tmpdir, "test.json")
        j = Json(filename, verbose=False)
        j.string = {"key": "value"}
        j.save(verbose=False)

        with pytest.raises(TypeError):
            JsonList(filename, verbose=False)

def test_jsondict_getitem_missing_key():
    """Should raise KeyError for missing key"""
    with tempfile.TemporaryDirectory() as tmpdir:
        filename = os.path.join(tmpdir, "test.json")
        jd = JsonDict(filename, verbose=False)
        with pytest.raises(KeyError):
            _ = jd["nonexistent_key"]

def test_jsonlist_index_not_found():
    """Should raise ValueError when item not in list"""
    with tempfile.TemporaryDirectory() as tmpdir:
        filename = os.path.join(tmpdir, "test.json")
        jl = JsonList(filename, verbose=False)
        jl.append("a")
        with pytest.raises(ValueError):
            jl.index("nonexistent")

def test_jsonlist_index_out_of_range():
    """Should raise IndexError for out of range index"""
    with tempfile.TemporaryDirectory() as tmpdir:
        filename = os.path.join(tmpdir, "test.json")
        jl = JsonList(filename, verbose=False)
        jl.append("item")
        with pytest.raises(IndexError):
            _ = jl[10]

def test_json_corrupted_file():
    """Should raise exception when JSON file is corrupted"""
    with tempfile.TemporaryDirectory() as tmpdir:
        filename = os.path.join(tmpdir, "test.json")
        # Create a file with invalid JSON
        with open(filename, "w") as f:
            f.write("{ invalid json content }")

        with pytest.raises(Exception):
            Json(filename, verbose=False)
