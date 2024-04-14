import hashlib
from datetime import datetime

from .alchemy import db


class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=False)
    theme = db.Column(db.String)
    goal = db.Column(db.String)
    description = db.Column(db.String)
    status = db.Column(db.String)
    rank = db.Column(db.FLOAT, default=0)
    vacancies = db.Column(db.JSON)
    public_date = db.Column(db.DateTime, default=datetime.utcnow)
    tags = db.Column(db.String)

    actions = db.relationship('UserAction', back_populates='project')

    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = db.relationship('User', back_populates='projects')

    @staticmethod
    def string_to_color(string):
        salt = "pull"  # 1 m 156 rct get

        salted_string = salt + string

        hash_code = hashlib.sha256(salted_string.encode()).hexdigest()

        hex_color = '#' + hash_code[:6]
        return hex_color
