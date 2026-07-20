from marshmallow import Schema, fields, validate


class ColeccionSchema(Schema):
    id = fields.Integer(dump_only=True)
    nombre = fields.String(required=True, validate=validate.Length(min=1, max=100))
    descripcion = fields.String(allow_none=True, load_default=None)
    imagen_url = fields.String(allow_none=True, load_default=None)
    created_at = fields.String(dump_only=True)
    updated_at = fields.String(dump_only=True)


coleccion_schema = ColeccionSchema()
coleccion_update_schema = ColeccionSchema(partial=True)
