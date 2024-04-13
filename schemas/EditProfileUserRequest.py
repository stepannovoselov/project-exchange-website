from .RegisterUserRequest import RegisterUserRequest
from marshmallow import fields


class EditProfileUserRequest(RegisterUserRequest):
    vk_link = fields.Str(required=True, allow_none=True)
    telegram_link = fields.Str(required=True, allow_none=True)
    github_link = fields.Str(required=True, allow_none=True)
    email_link = fields.Str(required=True, allow_none=True)
    education = fields.Str(required=True, allow_none=True)
    skills = fields.Str(required=True, allow_none=True)
    hobbies = fields.Str(required=True, allow_none=True)

    password = fields.Str(required=False, allow_none=True)
