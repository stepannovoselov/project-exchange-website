from .RegisterUserRequest import RegisterUserRequest
from marshmallow import fields, validate
import regex

url_pattern = (
    r'[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&\/\/=]*)'
    r'|^$'
)


class EditProfileUserRequest(RegisterUserRequest):
    vk_link = fields.Str(required=True, validate=validate.Regexp(regex.compile(url_pattern, regex.IGNORECASE), error='Указана неверная ссылка.'), allow_none=True)
    telegram_link = fields.Str(required=True, validate=validate.Regexp(regex.compile(url_pattern, regex.IGNORECASE), error='Указана неверная ссылка.'), allow_none=True)
    github_link = fields.Str(required=True, validate=validate.Regexp(regex.compile(url_pattern, regex.IGNORECASE), error='Указана неверная ссылка.'), allow_none=True)
    email_link = fields.Email(required=True, allow_none=True)
    education = fields.Str(required=True, allow_none=True)
    skills = fields.Str(required=True, allow_none=True)
    hobbies = fields.Str(required=True, allow_none=True)
    tags = fields.Str(required=True, allow_none=True)

    password = fields.Str(required=False, allow_none=True)
