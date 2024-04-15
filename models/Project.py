import hashlib
from datetime import datetime

from .alchemy import db
from config import SALT_FOR_PROJECTS_COLOR_GENERATOR


class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=False)
    theme = db.Column(db.String)
    goal = db.Column(db.String)
    description = db.Column(db.String)
    status = db.Column(db.String, default='open')
    vacancies = db.Column(db.JSON)
    public_date = db.Column(db.DateTime, default=datetime.utcnow)
    tags = db.Column(db.String)

    actions = db.relationship('UserAction', back_populates='project')

    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = db.relationship('User', back_populates='projects')

    @staticmethod
    def string_to_color(string):
        salt = SALT_FOR_PROJECTS_COLOR_GENERATOR

        salted_string = salt + string

        hash_code = hashlib.sha256(salted_string.encode()).hexdigest()

        hex_color = '#' + hash_code[:6]
        return hex_color
