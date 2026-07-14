from marshmallow import Schema, fields, validate

from app.models.usuario import ROLES


class RegisterSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=6))
    nombre = fields.String(required=True, validate=validate.Length(min=1, max=255))
    rol = fields.String(load_default="Vendedor", validate=validate.OneOf(ROLES))


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)


register_schema = RegisterSchema()
login_schema = LoginSchema()
