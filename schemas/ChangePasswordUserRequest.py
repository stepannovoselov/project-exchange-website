from marshmallow import Schema, fields


class ChangePasswordUserRequest(Schema):
    oldPassword = fields.Str(required=True)
    newPassword = fields.Str(required=True)
