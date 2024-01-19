from flask import *
from config import *
import uuid
import sqlite3

# Импортируем Flask и библиотеку для генерации UUID

app = Flask(__name__)

connection = sqlite3.connect('itsallgoodman.db')
cursor = connection.cursor()
cursor.execute('''CREATE TABLE users
             (id INTEGER PRIMARY KEY, mail TEXT)''')
@app.route('/')
def index():
    token = str(uuid.uuid4())

    # В главной функции мы каждый раз генерируем UUID в формате строки
    # Затем мы показываем пользователю HTML-файл, передавая токен в Jinjia

    # TODO: На релизе убрать порт и заменить url=url, где url - ссылка на нужную страницу
    return render_template('index.html', token=token, port=port)


# Страница /log вызывается тогда, когда пользователь завершил авторизацию

@app.route('/page')
def log():
    result = request.args.get('status')
    mail = request.args.get('mail')

    # status и mail - это аргументы, которые мы получаем из http
    # В них содержится инфомарция о статусе авторизации и о почте пользователя
    cursor.execute('INSERT INTO users (mail) VALUE(?)', (mail))

    return ''.join([mail, result])


app.run(port=port)
connection.commit()
connection.close()