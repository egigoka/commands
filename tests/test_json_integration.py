# Consolidated tests for commands/json.py (integration)

# ---- from test_json_integration.py ----

# Placeholder for future tests.
import pytest
import tempfile
import os
from commands.json import Json, JsonDict, JsonList

def test_json_create_new_file():
    with tempfile.TemporaryDirectory() as tmpdir:
        filename = os.path.join(tmpdir, "test.json")
        j = Json(filename, verbose=False)
        assert os.path.exists(filename)
        assert j.string == {}

def test_json_save_and_load():
    with tempfile.TemporaryDirectory() as tmpdir:
        filename = os.path.join(tmpdir, "test.json")
        j = Json(filename, verbose=False)
        j.string = {"key": "value", "number": 42}
        j.save(verbose=False)

        j2 = Json(filename, verbose=False)
        assert j2.string == {"key": "value", "number": 42}

def test_json_len():
    with tempfile.TemporaryDirectory() as tmpdir:
        filename = os.path.join(tmpdir, "test.json")
        j = Json(filename, verbose=False)
        j.string = {"a": 1, "b": 2}
        assert len(j) == 2

def test_json_contains():
    with tempfile.TemporaryDirectory() as tmpdir:
        filename = os.path.join(tmpdir, "test.json")
        j = Json(filename, verbose=False)
        j.string = {"key": "value"}
        assert "key" in j

def test_jsondict_getitem_setitem():
    with tempfile.TemporaryDirectory() as tmpdir:
        filename = os.path.join(tmpdir, "test.json")
        jd = JsonDict(filename, verbose=False)
        jd["key1"] = "value1"
        assert jd["key1"] == "value1"

def test_jsondict_items_keys_values():
    with tempfile.TemporaryDirectory() as tmpdir:
        filename = os.path.join(tmpdir, "test.json")
        jd = JsonDict(filename, verbose=False)
        jd["a"] = 1
        jd["b"] = 2
        assert list(jd.keys()) == ["a", "b"]
        assert list(jd.values()) == [1, 2]
        assert list(jd.items()) == [("a", 1), ("b", 2)]

def test_jsondict_clear():
    with tempfile.TemporaryDirectory() as tmpdir:
        filename = os.path.join(tmpdir, "test.json")
        jd = JsonDict(filename, verbose=False)
        jd["key"] = "value"
        jd.clear()
        assert len(jd) == 0

def test_jsonlist_append():
    with tempfile.TemporaryDirectory() as tmpdir:
        filename = os.path.join(tmpdir, "test.json")
        jl = JsonList(filename, verbose=False)
        jl.append("item1")
        jl.append("item2")
        assert jl.string == ["item1", "item2"]

def test_jsonlist_getitem_setitem():
    with tempfile.TemporaryDirectory() as tmpdir:
        filename = os.path.join(tmpdir, "test.json")
        jl = JsonList(filename, verbose=False)
        jl.append("item1")
        jl.append("item2")
        assert jl[0] == "item1"
        jl[1] = "modified"
        assert jl[1] == "modified"

def test_jsonlist_index():
    with tempfile.TemporaryDirectory() as tmpdir:
        filename = os.path.join(tmpdir, "test.json")
        jl = JsonList(filename, verbose=False)
        jl.append("a")
        jl.append("b")
        jl.append("c")
        assert jl.index("b") == 1

def test_jsonlist_sort():
    with tempfile.TemporaryDirectory() as tmpdir:
        filename = os.path.join(tmpdir, "test.json")
        jl = JsonList(filename, verbose=False)
        jl.append(3)
        jl.append(1)
        jl.append(2)
        jl.sort()
        assert jl.string == [1, 2, 3]

def test_jsonlist_clear():
    with tempfile.TemporaryDirectory() as tmpdir:
        filename = os.path.join(tmpdir, "test.json")
        jl = JsonList(filename, verbose=False)
        jl.append("item")
        jl.clear()
        assert jl.string == []

def test_json_unicode():
    with tempfile.TemporaryDirectory() as tmpdir:
        filename = os.path.join(tmpdir, "test.json")
        j = Json(filename, verbose=False, ensure_ascii=False)
        j.string = {"text": "Привет, мир! 你好世界"}
        j.save(verbose=False)

        j2 = Json(filename, verbose=False)
        assert j2.string["text"] == "Привет, мир! 你好世界"

def test_json_repr():
    """Test __repr__ method (lines 27-29)"""
    with tempfile.TemporaryDirectory() as tmpdir:
        filename = os.path.join(tmpdir, "test.json")
        j = Json(filename, verbose=False)
        j.string = {"key": "value"}
        repr_str = repr(j)
        assert "JSON" in repr_str
        assert filename in repr_str

def test_json_pop():
    """Test pop method (lines 34-35)"""
    with tempfile.TemporaryDirectory() as tmpdir:
        filename = os.path.join(tmpdir, "test.json")
        j = Json(filename, verbose=False)
        j.string = {"a": 1, "b": 2, "c": 3}
        value = j.pop("b")
        assert value == 2
        assert "b" not in j.string

def test_json_save_debug(capsys):
    """Test save with debug=True (line 46)"""
    with tempfile.TemporaryDirectory() as tmpdir:
        filename = os.path.join(tmpdir, "test.json")
        j = Json(filename, verbose=False)
        j.string = {"key": "value"}
        j.save(verbose=False, debug=True)
        captured = capsys.readouterr()
        assert "key" in captured.out

def test_json_save_not_quiet(capsys):
    """Test save with verbose=True (lines 57-58)"""
    with tempfile.TemporaryDirectory() as tmpdir:
        filename = os.path.join(tmpdir, "test.json")
        j = Json(filename, verbose=False)
        j.string = {"key": "value"}
        j.save(verbose=True)
        captured = capsys.readouterr()
        assert "successfully saved" in captured.out

def test_json_callable_save_and_get():
    with tempfile.TemporaryDirectory() as tmpdir:
        filename = os.path.join(tmpdir, "test.json")
        j = Json(filename, verbose=False)
        j.string = {"a": 1}
        j(save=True)
        assert j("a") == 1
        assert j("missing", default="x") == "x"

def test_json_load_empty_file():
    """Test load with empty file (line 82)"""
    with tempfile.TemporaryDirectory() as tmpdir:
        filename = os.path.join(tmpdir, "test.json")
        # Create an empty file
        with open(filename, "w") as f:
            f.write("")
        j = Json(filename, verbose=False)
        assert j.string == {}

def test_json_load_not_quiet(capsys):
    """Test load with verbose=True (line 86)"""
    with tempfile.TemporaryDirectory() as tmpdir:
        filename = os.path.join(tmpdir, "test.json")
        j = Json(filename, verbose=False)
        j.string = {"key": "value"}
        j.save(verbose=False)

        j2 = Json(filename, verbose=True)
        captured = capsys.readouterr()
        assert "successfully loaded" in captured.out

def test_json_load_debug(capsys):
    """Test load with debug=True (line 88)"""
    with tempfile.TemporaryDirectory() as tmpdir:
        filename = os.path.join(tmpdir, "test.json")
        j = Json(filename, verbose=False)
        j.string = {"test": "data"}
        j.save(verbose=False)

        # Call load() explicitly with debug=True
        j.load(verbose=False, debug=True)
        captured = capsys.readouterr()
        assert "test" in captured.out

def test_jsondict_iter():
    """Test __iter__ method (line 112)"""
    with tempfile.TemporaryDirectory() as tmpdir:
        filename = os.path.join(tmpdir, "test.json")
        jd = JsonDict(filename, verbose=False)
        jd["a"] = 1
        jd["b"] = 2
        jd["c"] = 3
        keys = list(jd)
        assert keys == ["a", "b", "c"]

def test_jsondict_str():
    """Test __str__ method for JsonDict"""
    with tempfile.TemporaryDirectory() as tmpdir:
        filename = os.path.join(tmpdir, "test.json")
        jd = JsonDict(filename, verbose=False)
        jd["key"] = "value"
        str_repr = str(jd)
        assert "key" in str_repr

def test_jsondict_callable_set_get_save():
    with tempfile.TemporaryDirectory() as tmpdir:
        filename = os.path.join(tmpdir, "test.json")
        jd = JsonDict(filename, verbose=False)
        jd("a", 1, save=True)
        assert jd("a") == 1
        assert jd("missing", default="x") == "x"

def test_jsonlist_str():
    """Test __str__ method for JsonList (lines 144-145)"""
    with tempfile.TemporaryDirectory() as tmpdir:
        filename = os.path.join(tmpdir, "test.json")
        jl = JsonList(filename, verbose=False)
        jl.append("item1")
        jl.append("item2")
        str_repr = str(jl)
        assert "item1" in str_repr
        assert "item2" in str_repr

def test_jsonlist_callable_append_save():
    with tempfile.TemporaryDirectory() as tmpdir:
        filename = os.path.join(tmpdir, "test.json")
        jl = JsonList(filename, verbose=False)
        jl("x", save=True)
        assert jl.string == ["x"]
