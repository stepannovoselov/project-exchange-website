from .alchemy import *


class UserAction(db.Model):
    __tablename__ = 'userActions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    userId = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    user = db.relationship('User', back_populates='actions')
    projectId = db.Column(db.Integer, db.ForeignKey('projects.id', ondelete='CASCADE'))
    project = db.relationship('Project', back_populates='actions')

    action = db.Column(db.String, nullable=False)
