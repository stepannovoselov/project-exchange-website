import hashlib

from .alchemy import db
from config import SALT_FOR_USERS_COLOR_GENERATOR


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    surname = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.LargeBinary, nullable=False)
    salt = db.Column(db.LargeBinary, nullable=False)
    iterations = db.Column(db.Integer, nullable=False)

    auth_type = db.Column(db.String, default='1561PROJECTS')
    status = db.Column(db.String, default='active')
    about = db.Column(db.JSON, default={
        "vk_link": "",
        "telegram_link": "",
        "github_link": "",
        "email_link": "",
        "education": "",
        "skills": "",
        "hobbies": "",
        "tags": ""
    })

    projects = db.relationship('Project', back_populates='author')

    actions = db.relationship('UserAction', back_populates='user')

    website_grade = db.Column(db.Integer)

    editable_values_by_user_except_password = ['surname', 'name', 'email', 'username', 'status', 'about']

    def json_editable_except_password(self):
        return {
            'surname': self.surname,
            'name': self.name,
            'email': self.email,
            'username': self.username,
            'status': self.status,
            'about': self.about
        }

    @staticmethod
    def string_to_color(string):
        salt = SALT_FOR_USERS_COLOR_GENERATOR

        salted_string = salt + string

        hash_code = hashlib.sha256(salted_string.encode()).hexdigest()

        hex_color = '#' + hash_code[:6]
        return hex_color

    @staticmethod
    def add_https_if_needed(url):
        if url == '':
            return url

        if url.startswith('http://'):
            return 'https://' + url[7:]
        elif url.startswith('https://'):
            return url
        else:
            return 'https://' + url
