port = 1900
debug = True

if __name__ == '__main__':
    import sqlite3

    connection = sqlite3.connect('itsallgoodman.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, login TEXT, auth_type TEXT, username TEXT, password TEXT, status TEXT, rank REAL, about TEXT)''')
    login = 'patriot228'
    password = '961413'
    a = cursor.execute('SELECT * from users where login = "' + login + '" and password = "' + str(password) + '"')
    print(a.fetchall())