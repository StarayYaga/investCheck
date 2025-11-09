import sqlite3 as sql
import datetime 


def main(short_name, price):
    time = datetime.datetime.now().strftime("%s")
    with sql.connect("weather_history.db") as connect:
            cursor = connect.cursor()

            # cursor.execute("""DROP TABLE IF EXISTS data""")
            cursor.execute('''CREATE TABLE IF NOT EXISTS data (
	"id"	INTEGER NOT NULL UNIQUE,
	"date"	TEXT NOT NULL,
    "short_name" TEXT NOT NULL,
	"price"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);''')

            cursor.execute("""
INSERT INTO data (date, short_name, price) VALUES (?, ?, ?)    
    """, (time, short_name, price))