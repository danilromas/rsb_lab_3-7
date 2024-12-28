import sqlite3

# Подключение к базе данных
connection = sqlite3.connect('books.db')
cursor = connection.cursor()

# Выполнение запроса
cursor.execute("SELECT * FROM book")
rows = cursor.fetchall()

# Вывод данных
for row in rows:
    print(row)

# Закрытие соединения
connection.close()
