from marshmallow import Schema, fields, validate

from app.models.usuario import ROLES


class UsuarioSchema(Schema):
    id = fields.Integer(dump_only=True)
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=6), load_only=True)
    nombre = fields.String(required=True, validate=validate.Length(min=1, max=255))
    rol = fields.String(load_default="Vendedor", validate=validate.OneOf(ROLES))
    activo = fields.Boolean(load_default=True)


class UsuarioUpdateSchema(Schema):
    email = fields.Email()
    password = fields.String(validate=validate.Length(min=6), load_only=True)
    nombre = fields.String(validate=validate.Length(min=1, max=255))
    rol = fields.String(validate=validate.OneOf(ROLES))


usuario_schema = UsuarioSchema()
usuario_update_schema = UsuarioUpdateSchema(partial=True)
