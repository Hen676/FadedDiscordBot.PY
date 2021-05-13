import os
import sqlite3
from sqlite3 import Error, Connection

import appdirs

_sql_create_user_table = """

"""
_sql_create_shard_table = """

"""


# Add test in memory
def create_connection(db_file, debug: bool = False):
    conn = None
    try:
        if not debug:
            conn = sqlite3.connect(db_file)
        else:
            conn = sqlite3.connect(':memory:')
        return conn
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def conn_execute(conn: Connection, sql: str):
    """
    Creates a Table in conn database

    :param conn: Connection to SQL Database
    :param string sql: SQL to Execute
    """
    try:
        c = conn.cursor()
        c.execute(sql)
    except Error as e:
        print(e)


if __name__ == '__main__':
    path = appdirs.user_log_dir('FadedBotApp', 'Hen676')
    if not os.path.isdir(path):
        os.makedirs(path)
    create_connection(os.path.join(path, "Faded_sqlite.db"))
