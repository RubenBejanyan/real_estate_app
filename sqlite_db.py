import sqlite3

conn = sqlite3.connect("real_estate.db", isolation_level=None)
c = conn.cursor()

c.execute("PRAGMA foreign_keys = ON")


c.execute("""CREATE TABLE IF NOT EXISTS currency(
            currency_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            ISO INTEGER NOT NULL UNIQUE
            )""")

c.execute("""CREATE TABLE IF NOT EXISTS city(
            city_id INTEGER PRIMARY KEY,
            english_name TEXT NOT NULL,
            armenian_name TEXT NOT NULL

            )""")

c.execute("""CREATE TABLE IF NOT EXISTS apartment(
             apt_id INTEGER PRIMARY KEY,
             ad_number INTEGER NOT NULL,
             ad_add_date TEXT,
             street TEXT,
             city_id INTEGER REFERENCES city (city_id),
             currency_id INTEGER REFERENCES currency (currency_id),
             price REAL,
             photo NULL,
             construction type TEXT,
             number_of_rooms INTEGER,
             area  INTEGER,
             new_building INTEGER,
             floor INTEGER,
             max_floors INTEGER,
             ceiling_height INTEGER,
             renovation TEXT,
             ad_info TEXT,
             update_date TEXT
            
         )""")

try:
    c.execute("INSERT INTO currency(name, ISO) VALUES ('USD', 1234)")
    
except sqlite3.DatabaseError as dbex:
    conn.rollback()
    print('[ERROR]', str(dbex))
conn.commit()

conn.close()