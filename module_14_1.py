import sqlite3


db = sqlite3.connect("not_telegram.db")
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance INTEGER NOT NULL
)
""")


"""for row in range(1,10+1):
    cursor.execute("INSERT INTO Users(username, email, age, balance) VALUES(?,?,?,?)",
                   (f"User{row}", f"example{row}@gmail.com", row * 10, 1000))"""

"""for row in range(1, 10+1, 2):
    cursor.execute("UPDATE Users SET balance = 500 WHERE id = ?",
                   (row,))"""

"""for row in range(1, 10+1, 3):
    cursor.execute("DELETE FROM Users WHERE id = ?",
                   (row,))"""

cursor.execute("SELECT * FROM Users WHERE age != 60")
for user in cursor.fetchall():
    print(f"{user[1]} | Почта: {user[2]} | Возраст: {user[3]} | Баланс: {user[-1]}")

# db.commit()
db.close()
