# encoding:utf-8
"""
database.py - File that contains database connection interface class
"""

import sqlite3
from archie.utils.decorators import trace_debug

class Database():
    """
    Class to handler a database interface
    """

    @trace_debug("Initializing database interface ...")
    def __init__(self, database) -> None:
        """
        Default constructor
        """
        # Setting database path
        self._database = database

    def _connect(self):
        """
        Function to connect to database
        """        
        self._conn = sqlite3.connect(self._database)

    def _disconnect(self):
        """
        Function to disconnect from the database
        """
        if self._conn:
            self._conn.close()

    def select(self, table, columns, conditions=None):
        """
        Function to perform a select from the database
        """
        data = None
        self._connect()

        if self._conn:
            query = f"SELECT {columns} FROM {table}"
            if conditions:
                query += f" WHERE {conditions}"
            try:
                result = self._conn.execute(query)
                data = result.fetchall()

            except Exception:
                pass
            finally:
                self._disconnect()
        
        return data

    def insert(self, table, values):
        """
        Function to perform an insert in to the database
        """
        result = False
        self._connect()

        try:
            with self._conn:
                self._conn.execute(f"INSERT INTO {table} VALUES ({values})")
            
            result = True

        except Exception:
            pass
        finally:
            self._disconnect()

        return result

    def atomic_update(self, table, column, value, conditions):
        """
        Function to perform an update in to the database
        """
        result = False
        self._connect()

        try:
            with self._conn:
                self._conn.execute(f"UPDATE {table} SET {column} = {value} WHERE {conditions})")
            
            result = True

        except Exception:
            pass
        finally:
            self._disconnect()

        return result

    




