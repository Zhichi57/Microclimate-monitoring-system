import random
import sqlite3

conn = sqlite3.connect("../db.sqlite3")  # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()

cursor.execute("DELETE FROM 'dataDisplay_indications' WHERE 'id'>0")
conn.commit()
