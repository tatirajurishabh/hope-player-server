import sqlite3

def migrate():
    print("Running DB migration")
    sqlite_conn = sqlite3.connect('data.db')

    try:
        print("1. Adding lyrics column (will error if already exists)")
        sqlite_conn.execute(
            "ALTER TABLE song ADD COLUMN lyrics TEXT default ''")
    except Exception as e:
        print(e)

    try:
        print("2. Adding liked column (will error if already exists)")
        sqlite_conn.execute(
            "ALTER TABLE song ADD COLUMN liked INTEGER default 0")
    except:
        print(e)

    sqlite_conn.close()


migrate()