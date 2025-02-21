import sqlite3
from faker import Faker
import os
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
    """Create tables for storing fake data and user credentials."""
    create_orders_table_sql = """
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY,
        delivery_agent TEXT NOT NULL,
        order_time TEXT NOT NULL,
        delivery_time TEXT NOT NULL,
        cost REAL NOT NULL,
        status TEXT NOT NULL
    );
    """
    create_users_table_sql = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        is_admin INTEGER DEFAULT 0
    );
    """
    try:
        c = conn.cursor()
        c.execute(create_orders_table_sql)
        c.execute(create_users_table_sql)
        # Insert default admin user
        c.execute("INSERT OR IGNORE INTO users (username, password, is_admin) VALUES (?, ?, ?)", 
                 ("admin", "admin123", 1))
        conn.commit()
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

def initialize_database(db_file):
    """Initialize the database if it doesn't exist."""
    print("Trying to initialize the database....")
    db_dir = os.path.dirname(db_file)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
    if not os.path.exists(db_file):
        fake = Faker()
        print("Database creation in progress....")
        conn = create_connection(db_file)
        if conn is not None:
            print("users creation in progress....")
            create_table(conn)
            insert_fake_data(conn, fake)
            conn.close()
        else:
            print("Error! Cannot create the database connection.")
    else:
        print("Database already exists.")

if __name__ == '__main__':
    database = "../data/food_delivery.db"
    initialize_database(database)