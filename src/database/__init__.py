#!/usr/bin/env python3.7

import src.database.database as db

if __name__ == '__main__':
    database = db.Database()
    for table in db.tables:
        database.execute(table)
    database.close()
