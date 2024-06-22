import sqlite3


def create_db_and_table():
    # Создаем подключение к базе данных (файл my_database.db будет создан)
    connection = sqlite3.connect('db_cities.db')
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Cites (
    name TEXT NOT NULL,
    link TEXT NOT NULL
    )
    ''')
    connection.close()
    default_city()


def default_city():
    connection = sqlite3.connect('db_cities.db')
    cursor = connection.cursor()

    # Добавляем нового пользователя
    cursor.execute('INSERT INTO Cites (name, link) VALUES (?, ?)', ('Челябинск', 'https://t.me/+fUYi5TIQZudkNjli'))
    cursor.execute('INSERT INTO Cites (name, link) VALUES (?, ?)', ('Екатеринбург', 'https://t.me/+i1n2u7yTb0cwZjVi'))
    cursor.execute('INSERT INTO Cites (name, link) VALUES (?, ?)', ('Пермь', 'https://t.me/+seLoCbBb_3o0OTgy'))

    # Сохраняем изменения и закрываем соединение
    connection.commit()
    connection.close()


def get_cities():
    connection = sqlite3.connect('db_cities.db')
    cursor = connection.cursor()
    cursor.execute('SELECT name FROM Cites')
    cities = cursor.fetchall()
    return cities


def get_link(city):
    connection = sqlite3.connect('db_cities.db')
    cursor = connection.cursor()
    cursor.execute("SELECT link FROM Cites WHERE name = ?", (city,))
    link = cursor.fetchall()
    return link[0][0]


def update_link_city(city, link):
    try:
        connection = sqlite3.connect('db_cities.db')
        cursor = connection.cursor()

        cursor.execute('UPDATE Cites SET link = ? WHERE name = ?', (link, city))

        connection.commit()
        connection.close()
        return True
    except:
        return False