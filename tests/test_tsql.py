# Consolidated tests for commands/tsql.py (unit)

# ---- from test_tsql9.py ----


import pytest


def test_tsql9_import():
    from commands import TSQL
    assert TSQL is not None


# ---- from test_tsql_extra.py ----


import pytest

from commands.tsql import TSQL






# ---- from test_tsql_instance.py ----


import sys
import pytest
from commands.tsql import TSQL


class DummyPrint:
    @staticmethod
    def __call__(*args, **kwargs):
        pass
    debug = __call__
    def __getattr__(self, item):
        return self.__call__






# ---- from test_tsql_more.py ----


import sys
import types

import pytest

from commands.tsql import TSQL


class _DummyPrint:
    def __init__(self):
        self.calls = []

    def __call__(self, *args, **kwargs):
        self.calls.append(("call", args, kwargs))

    def debug(self, *args, **kwargs):
        self.calls.append(("debug", args, kwargs))


def test_tsql_call_delegates_to_run(monkeypatch):
    calls = {}

    def fake_run(self, query, debug=False):
        calls["query"] = query
        calls["debug"] = debug
        return "ok"

    monkeypatch.setattr(TSQL, "run", fake_run)
    t = TSQL("srv", "sa", "pwd", "db")
    assert t("select 1", debug=True) == "ok"
    assert calls == {"query": "select 1", "debug": True}


def test_tsql_run_debug_success_commits_and_closes(monkeypatch):
    printed = _DummyPrint()
    monkeypatch.setattr("commands.print.Print", printed)

    class DummyCursor:
        def __init__(self):
            self.closed = False
            self.executed = None

        def execute(self, q):
            self.executed = q

        def close(self):
            self.closed = True

    class DummyCon:
        def __init__(self):
            self.cur = DummyCursor()
            self.commits = 0
            self.closed = False

        def cursor(self):
            return self.cur

        def commit(self):
            self.commits += 1

        def close(self):
            self.closed = True

    dummy_con = DummyCon()

    class DummyPyodbc:
        class InterfaceError(Exception):
            pass

        class ProgrammingError(Exception):
            pass

        @staticmethod
        def connect(_conn_str, **_kwargs):
            return dummy_con

    monkeypatch.setitem(sys.modules, "pyodbc", DummyPyodbc)
    t = TSQL("srv", "sa", "pwd", "db")
    t.run("select 1", debug=True)

    assert dummy_con.cur.executed == "select 1"
    assert dummy_con.cur.closed is True
    assert dummy_con.commits == 2
    assert dummy_con.closed is True
    assert any("Trying connect to SQL" in a[0] for kind, a, _k in printed.calls if kind == "call")
    assert any("Close connection finished" in a[0] for kind, a, _k in printed.calls if kind == "call")






def test_tsql_run_without_transaction_debug_nextset_loop(monkeypatch):
    printed = _DummyPrint()
    monkeypatch.setattr("commands.print.Print", printed)

    class DummyCursor:
        def __init__(self):
            self._next_cnt = 0

        def execute(self, _q):
            return None

        def nextset(self):
            self._next_cnt += 1
            return self._next_cnt == 1

        def close(self):
            return None

    class DummyCon:
        def cursor(self):
            return DummyCursor()

        def close(self):
            return None

    dummy_pyodbc = types.SimpleNamespace(
        connect=lambda *_a, **_k: DummyCon(),
        ProgrammingError=Exception,
    )
    monkeypatch.setitem(sys.modules, "pyodbc", dummy_pyodbc)

    TSQL("srv", "sa", "pwd", "db").run_without_transaction("select 1", debug=True)
    assert any("Run without transaction" in a[0] for kind, a, _k in printed.calls if kind == "call")




def test_tsql_query_single_result_returns_flat_list(monkeypatch):
    class DummyCursor:
        def execute(self, _q):
            return None

        def fetchall(self):
            return [("row",)]

        def nextset(self):
            return False

        def close(self):
            return None

    class DummyCon:
        def cursor(self):
            return DummyCursor()

        def close(self):
            return None

    dummy_pyodbc = types.SimpleNamespace(
        connect=lambda *_a, **_k: DummyCon(),
        ProgrammingError=Exception,
    )
    monkeypatch.setitem(sys.modules, "pyodbc", dummy_pyodbc)

    out = TSQL("srv", "sa", "pwd", "db").query("select 1")
    assert out == [("row",)]




def test_tsql_drop_table_force_adds_alter(monkeypatch):
    captured = {}

    def fake_run_wo_tx(self, command, debug=False):
        captured["command"] = command

    monkeypatch.setattr(TSQL, "run_without_transaction", fake_run_wo_tx)
    TSQL("srv", "sa", "pwd", "db").drop_table("tbl", force=True)
    assert "ALTER DATABASE [tbl]" in captured["command"]
    assert "DROP TABLE [tbl]" in captured["command"]


# ---- from test_tsql_query_and_utils.py ----


import pytest

from commands.tsql import TSQL


class DummyPrint:
    def __call__(self, *args, **kwargs):
        pass

    debug = __call__

    def __getattr__(self, item):
        return self.__call__


def test_tsql_query_success_with_debug(monkeypatch):
    calls = {}
    import sys

    class DummyCursor:
        def __init__(self):
            self._next_called = 0

        def execute(self, query):
            calls["executed"] = query

        def fetchall(self):
            return [("row",)]

        def nextset(self):
            self._next_called += 1
            return self._next_called == 1

        def close(self):
            calls["closed"] = True

    class DummyCon:
        def __init__(self):
            self.cur = DummyCursor()

        def cursor(self):
            return self.cur

        def close(self):
            calls["con_closed"] = True

    class DummyPyodbc:
        ProgrammingError = Exception

        def connect(self, conn, autocommit=True):
            calls["conn"] = conn
            return DummyCon()

    dummy_pyodbc = DummyPyodbc()
    monkeypatch.setitem(sys.modules, "pyodbc", dummy_pyodbc)
    monkeypatch.setattr("commands.tsql.pyodbc", dummy_pyodbc, raising=False)
    monkeypatch.setattr("commands.tsql.Print", DummyPrint(), raising=False)
    t = TSQL("srv", "sa", "pwd", "db")
    result = t.query("select 1", debug=True)
    assert result == [[("row",)], [("row",)]]
    assert calls["closed"] and calls["con_closed"]
    assert "srv" in calls["conn"]




def test_tsql_drop_helpers(monkeypatch):
    captured = []

    def capture(self, command):
        captured.append(command)

    monkeypatch.setattr("commands.tsql.TSQL.run_without_transaction", capture)
    t = TSQL("srv", "sa", "pwd", "db")
    t.drop_database("db_name", force=True)
    assert "DROP DATABASE [db_name]" in captured[0]
    assert "ALTER DATABASE [db_name]" in captured[0]
    t.drop_table("tbl")
    assert any("DROP TABLE [tbl]" in cmd for cmd in captured)


def test_tsql_backup_database_paths(monkeypatch):
    calls = {}
    monkeypatch.setattr("commands.path.Path.combine", staticmethod(lambda *parts: "/fake/path.bak"))
    def fake_exist(path):
        calls["checked"] = path
        return False
    monkeypatch.setattr("commands.file.File.exist", staticmethod(fake_exist))
    monkeypatch.setattr("commands.file.File.create",
                        lambda path: calls.setdefault("created", path))
    monkeypatch.setattr("commands.file.File.delete",
                        lambda path, verbose=True: calls.setdefault("deleted", (path, verbose)))
    monkeypatch.setattr("commands.file.File.wipe",
                        lambda path: calls.setdefault("wiped", path))
    monkeypatch.setattr("commands.tsql.TSQL.run_without_transaction",
                        lambda self, command: calls.setdefault("command", command))
    res = TSQL("srv", "sa", "pwd", "db").backup_database_to_disk("main_db")
    assert res == "/fake/path.bak"
    assert calls["created"] == "/fake/path.bak"
    assert calls["deleted"][0] == "/fake/path.bak"
    assert "BACKUP DATABASE [main_db]" in calls["command"]


def test_tsql_backup_database_existing_file(monkeypatch):
    calls = {}
    monkeypatch.setattr("commands.path.Path.combine", staticmethod(lambda *parts: "/fake/path.bak"))
    monkeypatch.setattr("commands.file.File.exist", staticmethod(lambda path: True))
    monkeypatch.setattr("commands.file.File.wipe", lambda path: calls.setdefault("wiped", path))
    monkeypatch.setattr("commands.tsql.TSQL.run_without_transaction",
                        lambda self, command: calls.setdefault("command", command))
    TSQL("srv", "sa", "pwd", "db").backup_database_to_disk("main_db")
    assert calls["wiped"] == "/fake/path.bak"


def test_tsql_get_file_sizes_and_space(monkeypatch):
    t = TSQL("srv", "sa", "pwd", "db")
    monkeypatch.setattr(t, "query", lambda query, debug=False: [["rows"], [("size", "data 123 kb")]])
    class DummyStr:
        @staticmethod
        def get_integers(text):
            return [321]
    monkeypatch.setattr("commands.str.Str", DummyStr)
    sizes = t.get_file_sizes()
    used = t.get_used_space()
    assert sizes[0][0] == "rows"
    assert used == 321 * 1024


# ---- from test_tsql_run_without_transaction.py ----


import pytest

from commands.tsql import TSQL


def test_tsql_run_without_transaction_success(monkeypatch):
    class DummyCursor:
        def __init__(self):
            self.executed = None
            self.closed = False
        def execute(self, q):
            self.executed = q
        def close(self):
            self.closed = True
        def nextset(self):
            return False
    class DummyCon:
        def __init__(self):
            self.cur = DummyCursor()
            self.closed = False
        def cursor(self):
            return self.cur
        def close(self):
            self.closed = True
    class DummyPyodbc:
        ProgrammingError = Exception
        def __init__(self, connection):
            self.connection = connection
            self.connect_calls = []
        def connect(self, conn, autocommit=False):
            self.connect_calls.append((conn, autocommit))
            return self.connection
    import sys
    connection = DummyCon()
    pyodbc = DummyPyodbc(connection)
    monkeypatch.setitem(sys.modules, "pyodbc", pyodbc)
    monkeypatch.setattr("commands.tsql.pyodbc", pyodbc, raising=False)
    t = TSQL("srv", "sa", "pwd", "db")
    t.run_without_transaction("select 1", debug=False)
    assert pyodbc.connect_calls == [(t.connect_to_sql_string, True)]
    assert connection.cur.executed == "select 1"
    assert connection.cur.closed is True
    assert connection.closed is True
