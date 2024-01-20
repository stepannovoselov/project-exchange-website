from flask import *
from config import *
import uuid
import sqlite3
from random import *

# Импортируем Flask и библиотеку для генерации UUID

app = Flask(__name__)
app.secret_key = 'secret_key'

connection = sqlite3.connect('itsallgoodman.db', check_same_thread=False)
cursor = connection.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY, login TEXT, auth_type TEXT, username TEXT, password TEXT, status TEXT, about TEXT)''')


@app.route('/')
def index():
    token = str(uuid.uuid4())
    if session.get('loged', False) == True:
        return render_template('main.html', login=session.get('login'))
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
    return render_template('create-project.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login', methods=['post'])
def login1():
    username = request.form.get('username')
    password = request.form.get('password')
    cursor.execute('SELECT login, password FROM users')
    a = cursor.execute(
        'SELECT * from users where login = "' + username + '" and password = "' + password + '"').fetchall()
    if a:
        session['loged'] = True
        session['login'] = username
        session['password'] = password
        return redirect('/')
    if not a:
        session['loged'] = False
        return redirect('/')


@app.route('/register')
def reg():
    return render_template('register.html')


@app.route('/register', methods=['post'])
def register():
    login = request.form.get('username')
    password = request.form.get('password')
    # cursor.execute('SELECT login FROM users')
    # a = len(cursor.fetchall())
    b = randint(1, 18446744073)
    cursor.execute(
        "INSERT INTO users VALUES ('" + str(b) + "','" + str(login) + "', 'our', '" + str(login) + "', '" + str(
            password) + "', '', '', '') ")
    connection.commit()
    session['login'] = login
    session['password'] = password
    # TODO:сделать потом с помощью вопросов а также сделать проверку нет ли такого же логина
    if session.get('login') and session.get('password'):
        session['loged'] = True
        cursor.execute('SELECT login, password FROM users')
        maslog = cursor.fetchall()
        print(maslog)
        return redirect('/')
    else:
        return redirect('/test')


@app.route('/account')
def account():
    if session['loged']:
        cursor.execute('SELECT login, password FROM users')
        userdata = cursor.execute(f"SELECT * FROM users WHERE login='{session.get('login')}'").fetchall()
        print(userdata)
        return render_template('account.html', userdata=userdata)
    else:
        return redirect('/login')


@app.route('/account', methods=['post'])
def account_me():
    opt = request.form.get('inlineFormSelectPref')
    id = request.form.get('about')
    if opt == "1" and id:
        cursor.execute('insert into users (status, about) values(?,?)', ("Ищу команду", id))
    elif opt == "2" and id:
        cursor.execute('insert into users (status, about) values(?,?)', ("Ищу проект", id))
    return redirect('/account')


@app.route('/search-projects')
def projects():
    return render_template('find-projects.html')


@app.route('/search-users')
def teammates():
    return render_template('find-teammates.html')


@app.route('/bookmarks')
def marks():
    return render_template('bookmarks.html')


@app.route('/logout')
def logout():
    if session['loged'] == True:
        session['loged'] = False
        del session['login']
        del session['password']
        return redirect('/')
    else:
        return redirect('/')


# ID
# Login
# Auth_type
# Username
# Password (в соответствии с auth_type)
# Status
# Рейтинг
# Описание профиля
# Список id принадлежащих проектов

app.run(port=port + 5, debug=debug)
connection.commit()
connection.close()
