from flask import *
import uuid

# Импортируем Flask и библиотеку для генерации UUID

app = Flask(__name__)


@app.route('/')
def index():
    token = str(uuid.uuid4())

    # В главной функции мы каждый раз генерируем UUID в формате строки
    # Затем мы показываем пользователю HTML-файл, передавая токен в Jinjia

    return render_template('index.html', token=token)


# Страница /log вызывается тогда, когда пользователь завершил авторизацию

@app.route('/page')
def log():
    result = request.args.get('status')
    mail = request.args.get('mail')

    # status и mail - это аргументы, которые мы получаем из http
    # В них содержится инфомарция о статусе авторизации и о почте пользователя

    return ''.join([mail, result])


app.run()
