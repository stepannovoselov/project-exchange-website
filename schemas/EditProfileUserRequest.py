from .RegisterUserRequest import RegisterUserRequest
from marshmallow import fields


class EditProfileUserRequest(RegisterUserRequest):
    password = fields.Str(required=False, allow_none=True)
