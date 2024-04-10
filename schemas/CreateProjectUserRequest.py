from marshmallow import Schema, fields


class CreateProjectUserRequest(Schema):
    name = fields.Str(required=True)
    theme = fields.Str(allow_none=True)
    goal = fields.Str(allow_none=True)
    description = fields.Str(allow_none=True)

    unsuccessful_redirect_template = 'create-project-form.html'
