import os
import appdirs
import sqlite3
from sqlite3 import Error


def get_file_path():
    path = appdirs.user_log_dir('FadedBotApp', 'Hen676')
    if not os.path.isdir(path):
        os.makedirs(path)
    return path


class database:
    conn = None
    path = ""
    debug = False

    def __init__(self, debug: bool = False):
        self.path = os.path.join(get_file_path(), "Faded_sqlite.db")
        self.debug = debug
        self.conn = self.create_connection()

    def create_connection(self):
        conn = None
        try:
            if not self.debug:
                conn = sqlite3.connect(self.path)
            else:
                conn = sqlite3.connect(':memory:')
            return conn
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()

    def execute(self, sql: str, dic: dict = None):
        """
        Creates a Table in conn database

        :param string sql: SQL to Execute
        :param dic: Dictionary for SQL cmd
        """
        try:
            c = self.conn.cursor()
            if dic is None:
                c.execute(sql)
            else:
                c.execute(sql, dic)
        except Error as e:
            print(e)

    def dump(self):
        cursor = self.conn.execute("select sql from sqlite_master where type = 'table'")
        print(cursor)

    def commit(self):
        self.conn.commit()

    def close(self):
        self.commit()
        self.conn.close()
