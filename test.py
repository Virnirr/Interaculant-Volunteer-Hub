import sqlite3
from helper import dict_factory


con = sqlite3.connect("volunteer.db")
con.row_factory = dict_factory
db = con.cursor()

services_created = db.execute("SELECT id, title, date, start_time, end_time, location, total_volunteer, available FROM services WHERE user_id = ?", [1]).fetchall()
volunteer = db.execute("SELECT services_id, volunteer_username, volunteer_email FROM volunteers WHERE user_id = ?", [1]).fetchall()

print(services_created)

con.commit()
con.close()
