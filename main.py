from flask import *
from config import *
import uuid
import sqlite3

# Импортируем Flask и библиотеку для генерации UUID

app = Flask(__name__)

connection = sqlite3.connect('itsallgoodman.db')
cursor = connection.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY, mail TEXT, username TEXT, password TEXT, stasus TEXT, loged INTENGER)''')


@app.route('/')
def index():
    token = str(uuid.uuid4())

    # В главной функции мы каждый раз генерируем UUID в формате строки
    # Затем мы показываем пользователю HTML-файл, передавая токен в Jinjia

    # TODO: На релизе убрать порт и заменить url=url, где url - ссылка на нужную страницу
    link = 'http://127.0.0.1:' + str(port) + '/page'
    return render_template('register.html', token=token, link=link)


# Страница /log вызывается тогда, когда пользователь завершил авторизацию


@app.route('/test')
def test():
    return render_template('main.html')


@app.route('/page')
def log():
    result = request.args.get('status')
    mail = request.args.get('mail')

    # status и mail - это аргументы, которые мы получаем из http
    # В них содержится инфомарция о статусе авторизации и о почте пользователя
    cursor.execute('INSERT INTO users (mail) VALUE(?)', (mail))

    return ' '.join([mail, result])

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def reg():
    return render_template('register.html')

@app.route('/register', methods = ['post'])
def register():
    session['username'] = request.form.get('username')
    session['password'] = request.form.get('password')
    cursor.execute("INSERT INTO users VALUES (0, 'loh@gmail.com', session['username'], session['password'], 'loh', 1")
    if session['login'] and session['password']:
        session['loged1'] = 1
        return '<html><body>Boo!</body></html>'



app.run(port=1565, debug=True)
connection.commit()
connection.close()