from flask import *
from config import *
import uuid
import sqlite3
from random import *
import json
import datetime

# Импортируем Flask и библиотеку для генерации UUID

app = Flask(__name__)
app.secret_key = 'secret_key'

connection = sqlite3.connect('itsallgoodman.db', check_same_thread=False)
cursor = connection.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY, login TEXT, auth_type TEXT, username TEXT, password TEXT, status TEXT, about TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS projects
(id INTEGER PRIMARY KEY, name TEXT, description TEXT, status TEXT, rank REAL, theme TEXT, deadline TEXT, who_needs TEXT, public_date TEXT, likes TEXT, dislikes TEXT, author TEXT)''')
connection.commit()


@app.route('/')
def index():
    token = str(uuid.uuid4())
    if session.get('loged', False):
        return render_template('main.html', login=session.get('login'))
    elif not session:
        return render_template('register.html')
    elif not session.get('loged', False):
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
            password) + "', '', '') ")
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
        userdata = cursor.execute(f"SELECT * FROM users WHERE login='{session.get('login')}'").fetchall()[0]
        print(userdata)
        return render_template('account.html', description=userdata[6], status=userdata[5], username=userdata[1],
                               projects=[])
    else:
        return redirect('/login')


@app.route('/account', methods=['post'])
def account_me():
    opt = request.form.get('status')
    about = request.form.get('about')

    print(1, opt, about)

    if opt == "1":
        cursor.execute('update users set status = ? where login = ?', ("Ищу команду", session['login']))
    elif opt == "2":
        cursor.execute('update users set status = ? where login = ?', ("Ищу Проект", session['login']))
    cursor.execute('update users set about = ? where login = ?', (str(about), session['login']))

    connection.commit()
    return redirect('/account')


@app.route('/search-projects')
def projects():
    projects = cursor.execute('''SELECT * FROM projects''').fetchall()
    print(projects)
    return render_template('find-projects.html', projects=projects, l=len(projects))


@app.route('/search-users')
def teammates():
    cursor.execute('SELECT login, status FROM users')
    maslog = cursor.fetchall()
    print(maslog)
    return render_template('find-teammates.html', maslog=maslog, login=session.get('login'))


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


@app.route('/create-project', methods=['post'])
def create_project():
    project_name = request.form.get('name')
    project_status = "Ищу команду" if request.form.get('status') == '1' else "Команда набрана"
    project_theme = request.form.get('theme')
    project_deadline = request.form.get('deadline')
    project_who_needs = request.form.get('search-to')
    project_description = request.form.get('description')
    project_description = request.form.get('description')
    project_id = randint(1, 18446744073)
    project_rank = 0.0
    project_public_date = datetime.datetime.now().date().strftime("%Y-%m-%d")
    project_likes = json.dumps([])
    project_dislikes = json.dumps([])
    project_author = session['login']

    project_author = cursor.execute('''SELECT id FROM users WHERE login = ?''', (project_author,)).fetchone()[0]

    cursor.execute('''INSERT INTO projects (id, name, description, status, rank, theme, deadline, who_needs, public_date, likes, dislikes, author)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                   (project_id, project_name, project_description, project_status, project_rank, project_theme,
                    project_deadline, project_who_needs, project_public_date, project_likes, project_dislikes,
                    project_author))
    connection.commit()
    return redirect('/account')


@app.route('/create-project', methods=['get'])
def create_project_page():
    return render_template('create-project.html')


@app.route('/ideas-generator')
def ideas_generator():
    return redirect('/')


app.run(port=port + 5, debug=debug)
connection.commit()
connection.close()

# json.dumps([1, 2, 3])
# json.loads('[1, 2, 3]')
