import sqlite3
from faker import Faker
import random
from datetime import datetime, timedelta

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
    """Create tables for storing fake data."""
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY,
        delivery_agent TEXT NOT NULL,
        order_time TEXT NOT NULL,
        delivery_time TEXT NOT NULL,
        cost REAL NOT NULL,
        status TEXT NOT NULL
    );
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)

def insert_fake_data(conn, fake):
    """Insert fake data into the orders table."""
    insert_sql = """
    INSERT INTO orders (delivery_agent, order_time, delivery_time, cost, status)
    VALUES (?, ?, ?, ?, ?)
    """
    cur = conn.cursor()
    agents = [fake.name() for _ in range(10)]
    for _ in range(1000):
        agent = random.choice(agents)
        order_time = fake.date_time_this_year()
        delivery_time = order_time + timedelta(minutes=random.randint(10, 60))
        cost = round(random.uniform(5, 50), 2)
        status = random.choice(['delivered', 'cancelled'])
        cur.execute(insert_sql, (agent, order_time, delivery_time, cost, status))
    conn.commit()

def main():
    database = "../data/food_delivery.db"
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