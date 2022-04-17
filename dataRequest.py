import sqlite3
conn = sqlite3.connect("funcAndClass.db")
cursor = conn.cursor ()
sql = "SELECT * FROM GlobalObjects WHERE type=?"
cursor.execute(sql, [("Class")])

print ('Classes')
print(cursor.fetchall())

sql = "SELECT * FROM GlobalObjects WHERE type=?"
cursor.execute(sql, [("Function")])

print ('Functions')
print(cursor.fetchall())
