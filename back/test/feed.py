import json
import sqlite3

env = None
with open("C:/Users/romain/code/fullstack/metadata_transfer/back/env.json", "r") as fr:
    env = json.loads(fr.read())

with sqlite3.connect(env["database_test"]) as conn:
    conn.execute('PRAGMA foreign_keys = on;')
    with open(env["database_test_feed"], 'r', encoding="utf-8") as fr:
        conn.executescript(fr.read())
        conn.commit()
print("done")