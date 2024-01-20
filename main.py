from flask import *
from config import *
import uuid
import sqlite3

# Импортируем Flask и библиотеку для генерации UUID

app = Flask(__name__)
app.secret_key = 'secret_key'

connection = sqlite3.connect('itsallgoodman.db', check_same_thread=False)
cursor = connection.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY, login TEXT, auth_type TEXT, username TEXT, password TEXT, status TEXT, rank REAL, about TEXT)''')


@app.route('/')
def index():
    token = str(uuid.uuid4())
    if session.get('loged', False) == True:
        return render_template('main.html')
    elif not session:
        return render_template('register.html')
    elif session.get('loged', False) == False:
        return render_template('login.html')

    # В главной функции мы каждый раз генерируем UUID в формате строки
    # Затем мы показываем пользователю HTML-файл, передавая токен в Jinjia

    # TODO: На релизе убрать порт и заменить url=url, где url - ссылка на нужную страницу
    link = 'http://127.0.0.1:' + str(port) + '/page'
    return render_template('register.html', token=token, link=link)


# Страница /log вызывается тогда, когда пользователь завершил авторизацию


@app.route('/test')
def test():
    return render_template('bookmarks.html')


@app.route('/page')
def log():
    result = request.args.get('status')
    mail = request.args.get('mail')

    # status и mail - это аргументы, которые мы получаем из http
    # В них содержится инфомарция о статусе авторизации и о почте пользователя
    # cursor.execute('INSERT INTO users (mail) VALUE(?)', (mail))

    return ' '.join([mail, result])

@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/login', methods = ['post'])
def login1():
    username = request.form.get('username')
    password = request.form.get('password')
    if username == username and password == password:
        session['loged1'] = 1
        return render_template('main.html')
@app.route('/register')
def reg():
    return render_template('register.html')

@app.route('/register', methods = ['post'])
def register():
    login = request.form.get('username')
    password = request.form.get('password')
    a = len()
    cursor.execute("INSERT INTO users VALUES (len(id), 'login', 'our', 'login', 'password', '', '', '') ")
    #TODO:сделать потом с помощью вопросов
    if session.get('login') and session.get('password'):
        session['loged1'] = 1
        return redirect('/')
    else:
        return redirect('/test')

# ID
# Login
# Auth_type
# Username
# Password (в соответствии с auth_type)
# Status
# Рейтинг
# Описание профиля
# Список id принадлежащих проектов

app.run(port=port+1, debug=debug)
connection.commit()
connection.close()