from marshmallow import Schema, fields


class LoginUserRequest(Schema):
    username_or_email = fields.Str(required=True)
    password = fields.Str(required=True)
    remember_me = fields.Str()

    unsuccessful_redirect_template = 'login-form.html'
