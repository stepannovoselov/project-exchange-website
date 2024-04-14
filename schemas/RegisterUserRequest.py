from marshmallow import Schema, fields, validate
import regex


class RegisterUserRequest(Schema):
    surname = fields.Str(required=True, validate=validate.Regexp(regex.compile('^[\p{L}\s]+$'), error='Фамилия должна состоять только из букв.'))
    name = fields.Str(required=True, validate=validate.Regexp(regex.compile('^[\p{L}\s]+$'), error='Имя должно состоять только из букв.'))
    email = fields.Email(required=True)
    username = fields.Str(required=True, validate=validate.Regexp(r'^[a-zA-Z0-9_]*$', error='Имя пользователя должно содержать только английские буквы, цифры и нижние подчёркивания.'))
    password = fields.Str(required=True)

    unsuccessful_redirect_template = 'register-form.html'