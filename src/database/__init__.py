import src.database.database as db

if __name__ == '__main__':
    database = db.database()
    for table in db.tables:
        database.execute(table)
    database.close()
