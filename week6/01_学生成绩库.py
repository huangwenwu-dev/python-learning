import sqlite3

conn = sqlite3.connect("student_scores.db")
cursor = conn.cursor()

#cursor.execute("""
#    CREATE TABLE scores (
#    id INTEGER PRIMARY KEY,
#    name TEXT,
#    score REAL
#)""")

# cursor.execute("INSERT INTO scores (name, score) VALUES (?, ?)", ("老八", 95))
# cursor.execute("INSERT INTO scores (name, score) VALUES (?, ?)", ("老六", 90))
# cursor.execute("INSERT INTO scores (name, score) VALUES (?, ?)", ("老三", 66))

cursor.execute("SELECT name, score FROM scores")
rows = cursor.fetchall()
for row in rows:
    print(row)

cursor.execute("UPDATE scores SET score = ? WHERE name = ?", (88, "老三"))
conn.commit()
cursor.execute("DELETE FROM scores WHERE name = ?", ("老六",))
conn.commit()

cursor.execute("SELECT AVG(score) FROM scores")
result = cursor.fetchone()
print(result[0])

search_name = input("请输入要查询的学生姓名: ")
cursor.execute("SELECT name, score FROM scores WHERE name = ?", (search_name,))
result = cursor.fetchall()
print(result)

conn.close()