import datetime
import random
import sqlite3

conn = sqlite3.connect("../db.sqlite3")  # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()

rows = []
now_date = int(datetime.datetime.now().timestamp())
march_3 = 1653166800

for i in range(100):
    random_date = random.randint(march_3, now_date)
    rows.append((random.randint(30, 80), random.randint(15, 30), 12, str(random_date)))

for row in rows:
    cursor.execute(
        "INSERT INTO 'dataDisplay_indications' ('Humidity', 'Temperature', 'Sensor_id','Receiving_data_time') "
        "VALUES (?, ?, ?, ?);", row)
conn.commit()
