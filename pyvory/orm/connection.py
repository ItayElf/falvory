import os
import sqlite3
import sys

ROOT_PATH = os.path.normpath(os.path.dirname(sys.modules['__main__'].__file__))
DB_PATH = os.path.join(ROOT_PATH, "main.db")


class DBConnect:
    """Context manager for sqlite connection"""

    def __init__(self):
        self.connection = sqlite3.connect(DB_PATH)

    def __enter__(self):
        return self.connection.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.commit()
        self.connection.close()
