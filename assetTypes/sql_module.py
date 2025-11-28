import sqlite3 as sql
import time
from config import dirDB


def main(short_name, price):
    time_now = int(time.time())
    with sql.connect(dirDB) as connect:
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
    """, (time_now, short_name, price))