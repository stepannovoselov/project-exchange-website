from flask import session, redirect, request, render_template, jsonify
from flask.templating import TemplateNotFound
from functools import wraps
from marshmallow.schema import SchemaMeta
from datetime import datetime, timezone
from os import urandom
from hashlib import pbkdf2_hmac
from random import randint
import json
from g4f.Provider import *
from g4f.client import Client

from models import db, User, UserAction
from schemas import *
from config import DEFAULT_SESSION_TIME, LONG_SESSION_TIME


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session['expiry_time'] < datetime.now(timezone.utc):
            return redirect(f'/login')

        user_id = session['user_id']
        user = User.query.filter_by(id=user_id).first()
        return f(user, *args, **kwargs)
    return decorated_function


def anonymous_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' in session and session['expiry_time'] >= datetime.now(timezone.utc):
            return redirect('/')
        return f(*args, **kwargs)
    return decorated_function


def validate_request_data(schema: SchemaMeta):
    def validate_schema(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            data = {key: None if value.strip() == '' else value for key, value in request.form.items()}
            errors = schema().validate(data)

            if schema == RegisterUserRequest:
                if data.get('username', None) is not None:
                    user = User.query.filter_by(username=data['username']).first()
                    if user:
                        if errors.get('username', None) is None:
                            errors['username'] = []
                        errors['username'].append('Пользователь с таким именем пользователя уже существует.')

                if data.get('email', None) is not None:
                    user = User.query.filter_by(email=data['email']).first()
                    if user:
                        if errors.get('email', None) is None:
                            errors['email'] = []
                        errors['email'].append('Пользователь с такой почтой уже существует.')

            elif schema == LoginUserRequest:
                if data.get('username_or_email', None) is not None:
                    username_or_email = data['username_or_email']
                    if "@" in username_or_email:
                        user = User.query.filter_by(email=username_or_email).first()
                    else:
                        user = User.query.filter_by(username=username_or_email).first()

                    if user:
                        hashed_password, salt, iterations = hash_password(
                            data['password'],
                            user.salt,
                            user.iterations
                        )

                        if hashed_password != user.password:
                            if errors.get('password', None) is None:
                                errors['password'] = []
                            errors['password'].append('Неверный пароль.')
                    else:
                        if errors.get('username_or_email', None) is None:
                            errors['username_or_email'] = []
                        errors['username_or_email'].append('Пользователь с такими данными не существует.')

            elif schema == EditProfileUserRequest:
                if len(errors) > 0:
                    errors = translate_errors(errors)
                    user = User.query.filter_by(id=session['user_id']).first()
                    return jsonify({'status': 'error', 'errors': errors,
                                    'current_values': user.json_editable_except_password()}), 404
            elif schema == ChangePasswordUserRequest:
                user = User.query.filter_by(id=session['user_id']).first()
                if errors.get('oldPassword', None) is None and errors.get('newPassword', None) is None:
                    if hash_password(data['oldPassword'], salt=user.salt, iterations=user.iterations)[0] != user.password:
                        errors['oldPassword'] = ['Неверный пароль.']

                if len(errors) > 0:
                    return jsonify({'status': 'error', 'errors': errors}), 404

            if len(errors) == 0:
                return f(*args, **kwargs)

            errors = translate_errors(errors)

            try:
                if session.get('user_id', None) is not None:
                    user = User.query.filter_by(id=session['user_id']).first()
                    return render_template(schema.unsuccessful_redirect_template, errors=errors, values=request.form, current_user=user)

                return render_template(schema.unsuccessful_redirect_template, errors=errors, values=request.form)

            except (AttributeError, TemplateNotFound):
                return render_template('/')

        return decorated_function

    return validate_schema


def translate_errors(errors_dict: dict) -> dict:
    for field, error_list in errors_dict.items():
        for i, error in enumerate(error_list):
            if error == 'Field may not be null.':
                errors_dict[field][i] = 'Поле не должно быть пустым.'

            elif error == 'Not a valid email address.':
                errors_dict[field][i] = 'Неправильный формат адреса электронной почты.'

            elif error == 'Missing data for required field.':
                errors_dict[field][i] = 'Не удалось получить данные для этого поля.'

            elif error == 'Invalid value.':
                errors_dict[field][i] = 'Неверное значение поля.'

    return errors_dict


def transaction(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        result = f(*args, **kwargs)
        db.session.commit()
        return result

    return decorated_function


def hash_password(password, salt=None, iterations=None):
    if salt is None:
        salt = urandom(32)
    if iterations is None:
        iterations = randint(10000, 100000)

    hashed_password = pbkdf2_hmac(
        hash_name='sha256',
        password=password.encode('UTF-8'),
        salt=salt,
        iterations=iterations
    )

    return hashed_password, salt, iterations


def login_user(user_id: int, long_session: bool = False) -> None:
    session['user_id'] = user_id

    if long_session:
        session['expiry_time'] = datetime.utcnow() + LONG_SESSION_TIME
    else:
        session['expiry_time'] = datetime.utcnow() + DEFAULT_SESSION_TIME


def logout_user() -> None:
    session.pop('user_id', None)
    session.pop('expiry_time', None)


def get_project_actions_count(project, one_project=True) -> dict:
    if not one_project:
        return {
            project.id: {
                'likes': UserAction.query.filter_by(project=project, action='like').count(),
                'dislikes': UserAction.query.filter_by(project=project, action='dislike').count(),
                'mark': UserAction.query.filter_by(project=project, action='mark').count()
            } for project in project
        }

    return {
                'likes': UserAction.query.filter_by(project=project, action='like').count(),
                'dislikes': UserAction.query.filter_by(project=project, action='dislike').count(),
                'mark': UserAction.query.filter_by(project=project, action='mark').count()
            }


def ask_gpt(prompt):
    client = Client(
        provider=RetryProvider(providers=[
            Aura, ChatForAi, ChatgptAi, ChatgptFree, ChatgptNext, ChatgptX, DeepInfra, FlowGpt,
            FreeChatgpt, FreeGpt, GeminiProChat, GptTalkRu, HuggingChat, HuggingFace, Koala, Liaobots,
            Llama2, PerplexityLabs, Pi, Vercel, You,
        ]), shuffle=True,
    )

    response = client.chat.completions.create(
        model="",
        messages=[{"role": "user", "content": 'ВНИМАНИЕ, ЭТО АВТОМАТИЧЕСКОЕ СООБЩЕНИЕ КОТОРОЕ БУДЕТ ПАРСИТЬ РОБОТ, ОТВЕЧАЙ СТРОГО В ФОРМАТЕ JSON НАЧИНАЯ с { и ЗАКАНЧИВАЯ }. ПИШИ ОТВЕТ ТОЛЬКО НА РУССКОМ ЯЗЫКЕ ВКЛЮЧАЯ КЛЮЧИ В СЛОВАРЕ JSON. ЗАПРОС: ' + str(prompt)}],
    )

    return response.choices[0].message.content


def process_gpt_prompt(prompt):
    times = 0
    while True:
        try:
            answer = json.loads(ask_gpt(prompt))
            break
        except json.decoder.JSONDecodeError:
            if times > 3:
                return jsonify({'status': 'error'}), 504
            times += 1

    answer['status'] = 'ok'
    return jsonify(answer), 200

