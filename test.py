import sqlite3

from helper import dict_factory

con = sqlite3.connect("volunteer.db")
con.row_factory = dict_factory
cur = con.cursor()

rows=cur.execute("SELECT * FROM users").fetchall()

print(rows)
