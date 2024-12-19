import sqlite3
from pprint import pprint


class DatabaseHandler:
    def __init__(self, name):
        self.database_name = name
        self.database = sqlite3.connect(f"{self.database_name}.db")
        self.cursor = self.database.cursor()

        self.cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {self.database_name.capitalize()}(
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        price INTEGER NOT NULL,
        UNIQUE(title)
        )
        """)

    def get_all_products(self):
        self.cursor.execute(f"SELECT * FROM {self.database_name.capitalize()}")

        return self.cursor.fetchall()

    def get_all_products_as_dicts(self):
        self.cursor.execute(f"SELECT * FROM {self.database_name.capitalize()}")
        list_of_product = self.cursor.fetchall()
        list_of_dict_product = []
        for product in list_of_product:
            dict_product = {"id": product[0]}
            dict_product.update({"title": product[1]})
            dict_product.update({"description": product[2]})
            dict_product.update({"price": product[3]})
            list_of_dict_product.append(dict_product)
        return list_of_dict_product

    def add_product_to_db(self, title, description, price):
        try:
            self.cursor.execute(f"INSERT INTO {self.database_name.capitalize()}(title, description, price)"
                                f" VALUES (?, ?, ?)",(title, description, price))

            self.database.commit()
        except sqlite3.IntegrityError:
            print("Ошибка добавления продукта в базу")

    def delete_product(self, title):
        self.cursor.execute(f"DELETE FROM {self.database_name.capitalize()} WHERE title = ?",
                            (title,))

    def close_database(self):
        self.database.close()

    def open_database(self):
        self.database = sqlite3.connect(f"{self.database_name}.db")
        self.cursor = self.database.cursor()

    def delete(self):
        self.cursor.execute(f"DROP TABLE IF EXISTS {self.database_name.capitalize()}")
        self.database.commit()
        self.database.close()


if __name__ == "__main__":
    dbh = DatabaseHandler("Products")
    dbh.add_product_to_db("Здоровье +1", "Добавляет 1 единицу здоровья, хотя обычно это ловушка", 1)
    dbh.add_product_to_db("Здоровье +10", "Добавляет 10 единиц здоровья", 10)
    dbh.add_product_to_db("Здоровье +25", "Добавляет 25 единиц здоровья", 25)
    dbh.add_product_to_db("Здоровье +50", "Добавляет 50 единиц здоровья", 50)
    dbh.add_product_to_db("Здоровье +100", "Добавляет 100 единиц здоровья", 100)
    dbh.add_product_to_db("Неуязвимость", "Делает на время неуязвимым (на случай косяка перед девушкой)",
                          1000)
    p = dbh.get_all_products_as_dicts()
    pprint(p)