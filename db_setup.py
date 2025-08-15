import sqlite3

# Connect to DB
conn = sqlite3.connect("restaurant.db")
cursor = conn.cursor()

# Create menu table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS menu (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_name TEXT NOT NULL,
        category TEXT,
        price REAL NOT NULL,
        gst REAL
    )
''')

# Create orders table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_type TEXT,
        total_amount REAL,
        gst_amount REAL,
        discount REAL,
        payment_method TEXT,
        order_time TEXT
    )
''')

# Create order_items table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS order_items (
        item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER,
        item_name TEXT,
        quantity INTEGER,
        price REAL,
        FOREIGN KEY(order_id) REFERENCES orders(order_id)
    )
''')

conn.commit()
conn.close()

print("Database and tables created successfully.")
