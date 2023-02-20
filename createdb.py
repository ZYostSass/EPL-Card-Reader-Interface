# Script for creating a sample database file using SQLite
# Source:  https://www.digitalocean.com/community/tutorials/how-to-use-an-sqlite-database-in-a-flask-application


import sqlite3

conn = sqlite3.connect("sample.db")

with open('schema.sql') as f:
  conn.executescript(f.read())

cur = conn.cursor()

create_cmd = "INSERT INTO people (id, lname, fname, passwd) VALUES (?, ?, ?, ?)"

cur.execute(create_cmd,
            ('1111', 'Alice', 'Addams', 'pass1')
            )

cur.execute(create_cmd,
            ('2222', 'Bob', 'Barker', 'pass2')
            )

cur.execute(create_cmd,
            ('3333', 'Charlene', 'Cruikshank', 'pass3')
            )

cur.execute(create_cmd,
            ('4444', 'Dale', 'Dagobert', 'pass4')
            )

conn.commit()
conn.close()
