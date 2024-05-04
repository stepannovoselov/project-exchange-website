from .alchemy import *


class ProjectTeammate(db.Model):
    __tablename__ = 'project_teammates'

    id = db.Column(db.Integer, primary_key=True)

    userId = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    projectId = db.Column(db.Integer, db.ForeignKey('projects.id', ondelete='CASCADE'))
