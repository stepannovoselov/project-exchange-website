from marshmallow import Schema, fields


class CreateProjectUserRequest(Schema):
    name = fields.Str(required=True)
    type = fields.Str(required=True, validate=lambda value: value in ['Проект', 'Исследование', 'Идея'])
    theme = fields.Str(allow_none=True)
    goal = fields.Str(allow_none=True)
    description = fields.Str(allow_none=True)
    tags = fields.Str(allow_none=True)
    teammates = fields.Str(allow_none=True)
    vacancies = fields.Str(allow_none=True)

    unsuccessful_redirect_template = 'create-project-form.html'
