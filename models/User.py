from .alchemy import db


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
    status = db.Column(db.String)
    about = db.Column(db.JSON)

    projects = db.relationship('Project', back_populates='author')

    actions = db.relationship('UserAction', back_populates='user')

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
