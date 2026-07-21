# Consolidated tests for commands/tsql.py (negative)

# ---- from test_tsql_negative.py ----

# Placeholder for future tests.
import pytest
from commands.tsql import TSQL
import sys
import types

class DummyPrint:
    def __call__(self, *_args, **_kwargs):
        return None

def test_tsql_run_import_error(monkeypatch):
    monkeypatch.setattr("commands.tsql.pyodbc", None, raising=False)
    t = TSQL("srv", "sa", "pwd", "db")
    with pytest.raises(ImportError):
        t.run("select 1")

def test_tsql_run_connection_error(monkeypatch):
    class DummyPyodbc:
        class InterfaceError(Exception):
            pass

        class ProgrammingError(Exception):
            pass

        def connect(self, conn):
            raise self.InterfaceError("bad connect")
    monkeypatch.setattr("commands.tsql.pyodbc", DummyPyodbc(), raising=False)
    t = TSQL("srv", "sa", "pwd", "db")
    with pytest.raises(DummyPyodbc.ProgrammingError, match="bad connect"):
        t.run("select 1")

def test_tsql_run_importerror(monkeypatch):
    monkeypatch.setitem(sys.modules, "pyodbc", None)
    with pytest.raises(ModuleNotFoundError):
        TSQL("srv", "user", "pwd", "db").run("SELECT 1")

def test_tsql_run_programming_error(monkeypatch):
    class DummyCur:
        def execute(self, q):
            raise DummyPyodbc.ProgrammingError("bad")
        def close(self): pass
    class DummyCon:
        def cursor(self): return DummyCur()
        def commit(self): pass
        def close(self): pass
    class DummyPyodbc:
        class ProgrammingError(Exception): ...
        class InterfaceError(Exception): ...
    DummyPyodbc.connect = staticmethod(lambda *a, **k: DummyCon())
    monkeypatch.setitem(sys.modules, "pyodbc", DummyPyodbc)
    import pyodbc  # now refers to dummy
    # Patch commands.print module used inside tsql
    dummy_print_module = type("PMod", (), {"Print": DummyPrint()})
    monkeypatch.setitem(sys.modules, "commands.print", dummy_print_module)
    with pytest.raises(pyodbc.ProgrammingError):
        TSQL("srv", "user", "pwd", "db").run("bad")

def test_tsql_run_interface_error_wrapped(monkeypatch):
    class DummyPyodbc:
        class InterfaceError(Exception):
            pass

        class ProgrammingError(Exception):
            pass

        @staticmethod
        def connect(_conn_str, **_kwargs):
            raise DummyPyodbc.InterfaceError("bad connect")

    monkeypatch.setitem(sys.modules, "pyodbc", DummyPyodbc)
    t = TSQL("srv", "sa", "pwd", "db")
    with pytest.raises(DummyPyodbc.ProgrammingError) as exc:
        t.run("select 1")
    msg = str(exc.value)
    assert "self.connect_to_sql_string" in msg
    assert "query:select 1" in msg

def test_tsql_run_programming_error_wrapped(monkeypatch):
    class DummyPyodbc:
        class InterfaceError(Exception):
            pass

        class ProgrammingError(Exception):
            pass

    class DummyCursor:
        def execute(self, _q):
            raise DummyPyodbc.ProgrammingError("bad query")

        def close(self):
            pass

    class DummyCon:
        def cursor(self):
            return DummyCursor()

        def commit(self):
            pass

        def close(self):
            pass

    DummyPyodbc.connect = staticmethod(lambda *_a, **_k: DummyCon())
    monkeypatch.setitem(sys.modules, "pyodbc", DummyPyodbc)
    t = TSQL("srv", "sa", "pwd", "db")
    with pytest.raises(DummyPyodbc.ProgrammingError) as exc:
        t.run("select 1")
    assert "query:select 1" in str(exc.value)

def test_tsql_run_without_transaction_programming_error_wrapped(monkeypatch):
    class DummyPyodbc:
        class ProgrammingError(Exception):
            pass

    class DummyCursor:
        def execute(self, _q):
            raise DummyPyodbc.ProgrammingError("bad query")

        def close(self):
            return None

        def nextset(self):
            return False

    class DummyCon:
        def cursor(self):
            return DummyCursor()

        def close(self):
            return None

    DummyPyodbc.connect = staticmethod(lambda *_a, **_k: DummyCon())
    monkeypatch.setitem(sys.modules, "pyodbc", DummyPyodbc)

    t = TSQL("srv", "sa", "pwd", "db")
    with pytest.raises(DummyPyodbc.ProgrammingError) as exc:
        t.run_without_transaction("select 1")
    assert "query:select 1" in str(exc.value)

def test_tsql_query_import_error_prints_message(monkeypatch, capsys):
    sys.modules.pop("pyodbc", None)
    with pytest.raises(ModuleNotFoundError):
        TSQL("srv", "sa", "pwd", "db").query("select 1")
    assert "please, install pyodbc" in capsys.readouterr().out.lower()

def test_tsql_query_programming_error(monkeypatch):
    import sys

    class DummyPyodbc:
        class ProgrammingError(Exception):
            pass

        class InterfaceError(Exception):
            pass

    class DummyCursor:
        def execute(self, query):
            raise DummyPyodbc.ProgrammingError("bad query")

        def close(self):
            pass

    class DummyCon:
        def cursor(self):
            return DummyCursor()

        def close(self):
            pass

    DummyPyodbc.connect = staticmethod(lambda *a, **k: DummyCon())
    monkeypatch.setitem(sys.modules, "pyodbc", DummyPyodbc)
    monkeypatch.setattr("commands.tsql.pyodbc", DummyPyodbc(), raising=False)
    monkeypatch.setattr("commands.tsql.Print", DummyPrint(), raising=False)
    with pytest.raises(DummyPyodbc.ProgrammingError):
        TSQL("srv", "sa", "pwd", "db").query("bad query")

def test_tsql_run_without_transaction_import_error(monkeypatch):
    monkeypatch.setattr("commands.tsql.pyodbc", None, raising=False)
    t = TSQL("srv", "sa", "pwd", "db")
    with pytest.raises(ImportError):
        t.run_without_transaction("select 1")
