import sqlite3

connection = sqlite3.connect("real_estate.db")

cursor = connection.cursor()

command1 = """"Create Table IF NOT EXISTS
apartements(apartement_id INTEGER PRIMARY KEY,
            number_of_rooms INTEGER,
            ceiling_height INTEGER,
            picture TEXT,
            price INTEGER,
            currency_id INTEGER PRIMARY KEY,
            ad_add_date DATE,
            update_date DATE,
            floor INTEGER,
            max_floors INTEGER,
            renovation TEXT,
            new_building BOOLEAN,
            building_type TEXT,
            street TEXT,
            building TEXT,
            flat ,
            city_id INTEGER PRIMARY KEY
                                       )"""

cursor.execute(command1)

command2 =""""Create Table IF NOT EXISTS
currencies(currency_id INTEGER PRIMARY KEY,
           name TEXT,
           iso_code INTEGER
                                     )"""

cursor.execute(command2)


command3 =""""Create Table IF NOT EXISTS
cities(city_id INTEGER PRIMARY KEY,
           name_in_English TEXT,
           name_in_Armenian TEXT
                                     )"""

cursor.execute(command3)


cursor.execute("INSERT INTO apartements VALUES ()")


cursor.execute("INSERT INTO currencies VALUES (1, "Armenian dram", 051))
cursor.execute("INSERT INTO currencies VALUES (2, "United States dollar", 840))


cursor.execute("INSERT INTO cities VALUES ()")

cursor.execute("SELECT*FROM apartements")

results = cursor.fetchall()
print(results)

cursor.execute("UPDATE apartements SET .... WHERE .....")

cursor.execute("DELETE FROM apartements WHERE ....")
