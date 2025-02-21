import sqlite3
from faker import Faker

def create_connection(db_file):
    """Create a database connection to the SQLite database specified by db_file."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

def create_table(conn):
    """Create a table for storing fake data."""
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        address TEXT NOT NULL,
        email TEXT NOT NULL
    );
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)

def insert_fake_data(conn, fake):
    """Insert fake data into the users table."""
    insert_sql = """
    INSERT INTO users (name, address, email)
    VALUES (?, ?, ?)
    """
    cur = conn.cursor()
    for _ in range(100):
        cur.execute(insert_sql, (fake.name(), fake.address(), fake.email()))
    conn.commit()

def main():
    database = "../data/database.db"
    fake = Faker()

    conn = create_connection(database)
    if conn is not None:
        create_table(conn)
        insert_fake_data(conn, fake)
        conn.close()
    else:
        print("Error! Cannot create the database connection.")

if __name__ == '__main__':
    main()