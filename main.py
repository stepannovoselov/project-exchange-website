from flask import *
from config import *
import uuid
import sqlite3
import random
import json
import datetime
import hashlib
import os

app = Flask(__name__)
# app.permanent_session_lifetime = datetime.timedelta(hours=1)
app.secret_key = 'c996d1f4-870d-420a-94d0-70625aed9f53'

connection = sqlite3.connect('database.db', check_same_thread=False)
cursor = connection.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS users 
(id INTEGER PRIMARY KEY,
login TEXT,
password TEXT,
salt TEXT,
iterations INT,
auth_type TEXT,
username TEXT,
status TEXT,
about TEXT)''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS projects
(id INTEGER PRIMARY KEY,
name TEXT,
description TEXT,
status TEXT,
rank REAL,
theme TEXT,
deadline TEXT,
who_needs TEXT,
public_date TEXT,
likes TEXT,
dislikes TEXT,
author TEXT)
''')
connection.commit()


class User:
    def __init__(self, user_id=None, user_login=None):
        if user_id:
            userdata = cursor.execute('''SELECT * FROM users WHERE id = ?''', (user_id,)).fetchone()
        else:
            userdata = cursor.execute('''SELECT * FROM users WHERE login = ?''', (user_login,)).fetchone()

        if not userdata:
            self._id = None
            self._login = None
            self._password = None
            self._salt = None
            self._iterations = None
            self._auth_type = None
            self._username = None
            self._status = None
            self._about = None
        else:
            self._id = userdata[0]
            self._login = userdata[1]
            self._password = userdata[2]
            self._salt = userdata[3]
            self._iterations = userdata[4]
            self._auth_type = userdata[5]
            self._username = userdata[6]
            self._status = userdata[7]
            self._about = userdata[8]

    def __str__(self):
        return (
            f"User ID: {self._id}, "
            f"Login: {self._login}, "
            f"Password: {self._password}, "
            f"Auth Type: {self._auth_type}, "
            f"Username: {self._username}, "
            f"Status: {self._status}, "
            f"About: {self._about}"
        )

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        raise AttributeError("You can't change user's id")

    @property
    def login(self):
        return self._login

    @login.setter
    def login(self, value):
        cursor.execute('''UPDATE users SET login = ? WHERE id = ?''', (value, self._id))
        connection.commit()
        self._login = value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        cursor.execute('''UPDATE users SET password = ? WHERE id = ?''', (value, self._id))
        connection.commit()
        self._password = value

    @property
    def salt(self):
        return self._salt

    @salt.setter
    def salt(self, value):
        raise AttributeError("You can't change user's salt")

    @property
    def iterations(self):
        return self._iterations

    @iterations.setter
    def iterations(self, value):
        raise AttributeError("You can't change user's iterations")

    @property
    def auth_type(self):
        return self._auth_type

    @auth_type.setter
    def auth_type(self, value):
        raise AttributeError("You can't change user's auth type")

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        cursor.execute('''UPDATE users SET username = ? WHERE id = ?''', (value, self._id))
        connection.commit()
        self._username = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        cursor.execute('''UPDATE users SET status = ? WHERE id = ?''', (value, self._id))
        connection.commit()
        self._status = value

    @property
    def about(self):
        return self._about

    @about.setter
    def about(self, value):
        cursor.execute('''UPDATE users SET about = ? WHERE id = ?''', (value, self._id))
        connection.commit()
        self._about = value

    @staticmethod
    def hash_password(password, salt=None, iterations=None):
        if not salt:
            salt = os.urandom(32)
        if not iterations:
            iterations = 10000

        hashed_password = hashlib.pbkdf2_hmac(
            hash_name='sha256',
            password=password.encode('UTF-8'),
            salt=salt,
            iterations=iterations
        )

        return hashed_password, salt, iterations

    @staticmethod
    def create_user(login, password, auth_type, username, status, about):
        if cursor.execute('SELECT * FROM users WHERE login = ?', (login,)).fetchone():  # Проверка уникальности логина
            raise ValueError('This login already exists')

        while True:  # Проверка уникальности айди
            user_id = random.randint(2 ** 8, 2 ** 32 - 1)
            if not cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone():
                break

        if auth_type == '1561PROJECTS':
            password, salt, iterations = User.hash_password(password)
        else:
            password = ""
            salt = ""
            iterations = ""

        cursor.execute(
            '''
            INSERT INTO users
            (id, login, password, salt, iterations, auth_type, username, status, about)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''',
            (user_id, login, password, salt, iterations, auth_type, username, status, about)
        )

        connection.commit()

        return User(user_id)


@app.route('/')
def index():
    if 'logged_in' not in session:
        session['logged_in'] = False
        return render_template('main.html', user_logged_in=session['logged_in'])
    return render_template('main.html', user_logged_in=session['logged_in'], login=session['login'])


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = User(user_login=request.form.get('login'))

        if user.id:
            hashed_password = User.hash_password(
                password=request.form.get('password'),
                salt=user.salt,
                iterations=user.iterations
            )[0]

            if hashed_password == user.password:
                session['logged_in'] = True
                session['id'] = user.id
                session['login'] = user.login

                return redirect('/')

    return render_template('login.html', token=uuid.uuid4())


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        user = User.create_user(
            login=request.form.get('login'),
            password=request.form.get('password'),
            auth_type='1561PROJECTS',
            username='',
            status='',
            about=''
        )

        session['logged_in'] = True
        session['id'] = user.id
        session['login'] = user.login
        return redirect('/')

    else:
        if request.args:  # В теории - работает
            status = request.args.get('status')
            login = request.args.get('mail')

            if status == 'Success':
                user = User.create_user(
                    login=login,
                    password='',
                    auth_type='1561ID',
                    username='',
                    status='',
                    about=''
                )

                session['logged_in'] = True
                session['id'] = user.id
                session['login'] = user.login
                return redirect('/')

            else:
                return redirect('/register')

    return render_template('register.html', token=uuid.uuid4())


@app.route('/account', methods=['POST', 'GET'])
def account():
    if request.method == 'POST':
        username = request.form.get('name')
        login = request.form.get('login')
        # password = request.form.get('password')
        status = request.form.get('status')
        about = request.form.get('about')

        user = User(user_id=session['id'])
        user.username = username
        user.login = login
        user.status = status
        user.about = about

        return redirect('/account')

    else:  # wait for it...
        if 'logged_in' in session:
            if session['logged_in']:
                user = User(user_id=session['id'])
                id_proj = cursor.execute(f"SELECT * FROM projects WHERE author='{session['id']}'").fetchall()
                print(id_proj)
                return render_template(
                    'account.html',
                    username=user.username,
                    login=user.login,
                    status=user.status,
                    about=user.about
                )

        return redirect('/')


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
def bookmarks():
    return render_template('bookmarks.html')


@app.route('/mark', methods=['post', 'get'])
def mark():
    cursor.execute("ALTER TABLE bookmarks ADD COLUMN bookmark REAL")
    cursor.execute("INSERT INTO bookmarks VALUES ('" + str(session.get('id')) + "')")
    return redirect('/search-projects')


@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session['logged_in'] = False

    return redirect('/')


@app.route('/create-project', methods=['post'])
def create_project():
    project_name = request.form.get('name')
    project_status = "Ищу команду" if request.form.get('status') == '1' else "Команда проект"
    project_theme = request.form.get('theme')
    project_deadline = request.form.get('deadline')
    project_who_needs = request.form.get('search-to')
    project_description = request.form.get('description')
    project_description = request.form.get('description')
    project_id = random.randint(1, 18446744073)
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


@app.route('/projects/<int:project_id>')
def show_project(project_id):
    projectdata = cursor.execute('''SELECT * FROM projects WHERE id = ?''', (project_id,)).fetchone()
    print(projectdata)
    return render_template('project.html', projectdata=projectdata)


@app.route('/users/<int:user_id>')
def show_user(user_id):
    userdata = cursor.execute('''SELECT * FROM users WHERE id = ?''', (user_id,)).fetchone()
    print(userdata)
    return render_template('account.html', userdata=userdata, self_auth=False)


app.run(port=port, debug=debug)
connection.commit()
connection.close()

# json.dumps([1, 2, 3])
# json.loads('[1, 2, 3]')
