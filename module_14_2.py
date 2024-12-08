import sqlite3
from consoleTextStyle import ConsoleTextStyle as CoTeSt


db = sqlite3.connect("not_telegram.db")
cursor = db.cursor()

# Удаление из базы данных not_telegram.db запись с id = 6.
cursor.execute("DELETE FROM Users WHERE id = ?", (6,))

# Подсчёт общего количества записей.
cursor.execute("SELECT COUNT(*) FROM Users")
total_users_count: int = cursor.fetchone()[0]

# Посчёт суммы всех балансов.
cursor.execute("SELECT SUM(balance) FROM Users")
total_users_balance: int = cursor.fetchone()[0]

# Вывод в консоль средний баланс всех пользователей.
cursor.execute("SELECT AVG(balance) FROM Users")
print(f"Средний баланс всех пользователей, найдённый с помощью функции SQL: "
      f"{CoTeSt.colorful_str(str(cursor.fetchone()[0]), CoTeSt.Color.CYAN)}")
print(f"Средний баланс всех пользователей, расчитанный из общего количества записей и суммы всех балансов: "
      f"{CoTeSt.colorful_str(str(total_users_balance/total_users_count), CoTeSt.Color.CYAN)}")

db.commit()
db.close()