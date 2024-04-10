from re import match
from marshmallow import Schema, fields, validate


class RegisterUserRequest(Schema):
    surname = fields.Str(required=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    username = fields.Str(required=True, validate=validate.Regexp('^[a-zA-Z0-9_]*$', error='Имя пользователя должно содержать только английские буквы, цифры и нижние подчёркивания'))
    password = fields.Str(required=True)

    unsuccessful_redirect_template = 'register-form.html'
