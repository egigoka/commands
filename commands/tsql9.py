#! python3
# -*- coding: utf-8 -*-
"""Internal module to interact with transact sql
"""
__version__ = "0.3.1"


class TSQL:
    def __init__(self, server, sa_user, sa_password, database, driver="{SQL Server}"):
        self.sql_driver = driver
        self.sql_server = server
        self.sql_sa_user = sa_user
        self.sql_sa_password = sa_password
        self.sql_database = database

        self.connect_to_sql_string = f'DRIVER={self.sql_driver};SERVER={self.sql_server};UID={self.sql_sa_user};' \
                                     f'PWD={self.sql_sa_password};DATABASE={self.sql_database}'

    def run(self, query, debug=False):
        import pyodbc
        from .print9 import Print

        if debug:
            Print('SQL settings:"' + self.connect_to_sql_string + '"')
            Print("Trying connect to SQL")
        con = pyodbc.connect(self.connect_to_sql_string)
        cur = con.cursor()
        if debug:
            Print("Successful connection to SQL")
            Print(f"Run with transaction: '{query}'")

        cur.execute(query)
        con.commit()

        if debug:
            Print(f"End '{query}'")
            Print("Try to close connection")
        cur.close()
        con.close()
        if debug:
            Print("Close connection done")

    def run_without_transaction(self, query, debug=False):
        import pyodbc
        from .print9 import Print

        if debug:
            Print('SQL settings:"' + self.connect_to_sql_string + '"')
            Print("Trying connect to SQL")
        con = pyodbc.connect(self.connect_to_sql_string, autocommit=True)
        cur = con.cursor()
        if debug:
            Print("Successful connection to SQL")
            Print(f"Run without transaction: '{query}'")

        cur.execute(query)
        while cur.nextset():
            pass

        if debug:
            Print(f"End '{query}'")
            Print("Try to close connection")
        cur.close()
        con.close()
        if debug:
            Print("Close connection done")

    def query(self, query, debug=False):
        import pyodbc
        from .print9 import Print

        if debug:
            Print('SQL settings:"' + self.connect_to_sql_string + '"')
            Print("Trying connect to SQL")
        con = pyodbc.connect(self.connect_to_sql_string, autocommit=True)
        cur = con.cursor()
        if debug:
            Print("Successful connection to SQL")
            Print(f"Run query: '{query}'")

        out = []
        cur.execute(query)
        for row in cur.fetchall():
            out.append(row)

        if debug:
            Print(f"End '{query}'")
            Print("Try to close connection")
        cur.close()
        con.close()
        if debug:
            Print("Close connection done")

        return out

    def drop_database(self, sql_database, force=False):
        command = ""
        if force:
            command += f"""USE master;
                               ALTER DATABASE [{sql_database}] SET SINGLE_USER WITH ROLLBACK IMMEDIATE;"""
        command += f"""DROP DATABASE [{sql_database}]"""
        self.run_without_transaction(command)

    def backup_database_to_disk(self, sql_database):
        from .path9 import Path
        from .file9 import File
        from .time9 import Time

        backup_path = Path.combine("C:", "Users", "Public", "mssqlbak",
                                   f"{sql_database}_{Time.dotted()}.bak")
        if not File.exist(backup_path):
            File.create(backup_path)
            File.delete(backup_path, quiet=True)
        else:
            File.wipe(backup_path)

        command = f"""BACKUP DATABASE [{sql_database}]
                          TO DISK = '{backup_path}'"""
        self.run_without_transaction(command)

        return backup_path

    def get_size(self, debug=False):
        query = fr'''SELECT
                        [size] * 8, 
                        [filename]
                     FROM sysfiles'''
        return self.query(query, debug=debug)