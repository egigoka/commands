#! python3
# -*- coding: utf-8 -*-
"""Internal module to interact with transact sql."""
from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Any, List, Optional, Sequence, Union, cast
else:
    def cast(_type, value):
        """Return value unchanged for runtime typing fallback."""
        return value

from .module import LazyModule, LazyProperty
__version__ = "0.6.6"

pyodbc = LazyModule("pyodbc", optional=True)
newline = LazyProperty(".const", "newline")
FileModule = LazyModule(".file")
PathModule = LazyModule(".path")
Print = LazyProperty(".print", "Print")
StrModule = LazyModule(".str")
TimeModule = LazyModule(".time")


class TSQL:
    """Transact-SQL helper for SQL Server connections."""

    @staticmethod
    def _get_pyodbc() -> Any:
        """Resolve the pyodbc module or raise appropriate error."""
        if pyodbc is None:
            print("please, install pyodbc")
            raise ImportError("pyodbc")
        if hasattr(pyodbc, "_load"):
            sys = __import__("sys")
            cached = getattr(pyodbc, "_module", None)
            if cached is not None and "pyodbc" not in sys.modules:
                print("please, install pyodbc")
                raise ModuleNotFoundError("pyodbc")
            module = pyodbc._load()
        else:
            module = pyodbc
        if module is None:
            print("please, install pyodbc")
            raise ModuleNotFoundError("pyodbc")
        return module

    def __init__(
        self,
        server: str,
        sa_user: str,
        sa_password: str,
        database: str,
        driver: str = "{SQL Server}"
    ) -> None:
        self.sql_driver = driver
        self.sql_server = server
        self.sql_sa_user = sa_user
        self.sql_sa_password = sa_password
        self.sql_database = database

        self.connect_to_sql_string = f'DRIVER={self.sql_driver};SERVER={self.sql_server};UID={self.sql_sa_user};' \
                                     f'PWD={self.sql_sa_password};DATABASE={self.sql_database}'

    def __call__(self, query: str, debug: bool = False) -> None:
        """Shortcut to run queries with transaction."""
        return self.run(query, debug=debug)

    def run(self, query: str, debug: bool = False) -> None:
        """Run a query within a transaction."""
        pyodbc = self._get_pyodbc()

        if debug:
            Print('SQL settings:"' + self.connect_to_sql_string + '"')
            Print("Trying connect to SQL")
        try:
            con = pyodbc.connect(self.connect_to_sql_string)
        except pyodbc.InterfaceError as e:
            raise pyodbc.ProgrammingError(f"self.connect_to_sql_string:'{self.connect_to_sql_string}{newline}"
                                                 f"query:{query}{newline}{e}")
        cur = con.cursor()
        if debug:
            Print("Successful connection to SQL")
            Print(f"Run with transaction: '{query}'")

        try:
            cur.execute(query)
        except pyodbc.ProgrammingError as e:
            raise pyodbc.ProgrammingError(f"self.connect_to_sql_string:'{self.connect_to_sql_string}{newline}"
                                                 f"query:{query}{newline}{e}")
        con.commit()

        if debug:
            Print(f"End '{query}'")
            Print("Try to close connection")
        cur.close()

        con.commit()
        con.close()
        if debug:
            Print("Close connection finished")

    def run_without_transaction(self, query: str, debug: bool = False) -> None:
        """Run a query without a transaction."""
        pyodbc = self._get_pyodbc()

        if debug:
            Print('SQL settings:"' + self.connect_to_sql_string + '"')
            Print("Trying connect to SQL")
        con = pyodbc.connect(self.connect_to_sql_string, autocommit=True)
        cur = con.cursor()
        if debug:
            Print("Successful connection to SQL")
            Print(f"Run without transaction: '{query}'")

        try:
            cur.execute(query)
        except pyodbc.ProgrammingError as e:
            raise pyodbc.ProgrammingError(f"self.connect_to_sql_string:'{self.connect_to_sql_string}{newline}"
                                                 f"query:{query}{newline}{e}")
        while cur.nextset():
            pass

        if debug:
            Print(f"End '{query}'")
            Print("Try to close connection")
        cur.close()
        con.close()
        if debug:
            Print("Close connection finished")

    def query(self, query: str, debug: bool = False) -> Union[List[Any], List[List[Any]]]:
        """Run a query and return result rows."""
        pyodbc = self._get_pyodbc()

        if debug:
            Print('SQL settings:"' + self.connect_to_sql_string + '"')
            Print("Trying connect to SQL")
        con = pyodbc.connect(self.connect_to_sql_string, autocommit=True)
        cur = con.cursor()
        if debug:
            Print("Successful connection to SQL")
            Print(f"Run query: '{query}'")

        out = []

        def get_rows(cursor: Any) -> List[Any]:
            output: List[Any] = []
            for row in cursor.fetchall():
                output.append(row)
            return output

        try:
            cur.execute(query)
        except pyodbc.ProgrammingError as e:
            raise pyodbc.ProgrammingError(f"self.connect_to_sql_string:'{self.connect_to_sql_string}{newline}"
                                                 f"query:{query}{newline}{e}")

        out.append(get_rows(cur))
        while cur.nextset():
            out.append(get_rows(cur))

        if debug:
            Print(f"End '{query}'")
            Print("Try to close connection")
        cur.close()
        con.close()
        if debug:
            Print("Close connection finished")

        if len(out) == 1:
            return out[0]
        return out

    def drop_database(self, sql_database: str, force: bool = False) -> None:
        """Drop a database, optionally forcing disconnects."""
        command = ""
        if force:
            command += f"""USE master;
                               ALTER DATABASE [{sql_database}] SET SINGLE_USER WITH ROLLBACK IMMEDIATE;"""
        command += f"""DROP DATABASE [{sql_database}]"""
        self.run_without_transaction(command)

    def drop_table(self, sql_table: str, force: bool = False) -> None:
        """Drop a table, optionally forcing disconnects."""
        command = ""
        if force:
            command += f"""USE master;
                               ALTER DATABASE [{sql_table}] SET SINGLE_USER WITH ROLLBACK IMMEDIATE;"""
        command += f"""DROP TABLE [{sql_table}]"""
        self.run_without_transaction(command)

    def backup_database_to_disk(self, sql_database: str) -> str:
        """Back up a database to a .bak file on disk."""
        Path = PathModule.Path
        File = FileModule.File
        Time = TimeModule.Time
        backup_path = Path.combine("C:", "Users", "Public", "mssql-bak",
                                      f"{sql_database}_{Time.dotted()}.bak")
        if not File.exist(backup_path):
            File.create(backup_path)
            File.delete(backup_path, verbose=False)
        else:
            File.wipe(backup_path)

        command = f"""BACKUP DATABASE [{sql_database}]
                          TO DISK = '{backup_path}'"""
        self.run_without_transaction(command)

        return str(backup_path)

    def get_file_sizes(self, debug: bool = False) -> Union[List[Any], List[List[Any]]]:
        """Get database file sizes."""
        query = fr'''SELECT
                         CONVERT(bigint, [size])*8*1024,
                         [filename]
                     FROM sysfiles'''
        return self.query(query, debug=debug)

    def get_used_space(self, debug: bool = False) -> int:
        """Get used database space in bytes."""
        Str = StrModule.Str
        query = "EXEC sp_spaceused"
        answer = self.query(query, debug=debug)
        data = answer[1][0][1]
        bytes_ = int(Str.get_integers(data)[0]) * 1024
        return bytes_
