from marshmallow import Schema, fields, validate

from app.models.cliente import CANALES, TIPOS_COMPRA


class ClienteSchema(Schema):
    id = fields.Integer(dump_only=True)
    ruc = fields.String(required=True, validate=validate.Length(min=1, max=50))
    razon_social = fields.String(required=True, validate=validate.Length(min=1, max=255))
    localidad = fields.String(allow_none=True, load_default=None)
    barrio = fields.String(allow_none=True, load_default=None)
    direccion = fields.String(allow_none=True, load_default=None)
    canal = fields.String(allow_none=True, load_default=None, validate=validate.OneOf(CANALES))
    sub_canal = fields.String(allow_none=True, load_default=None)
    tipo_compra = fields.String(
        allow_none=True, load_default=None, validate=validate.OneOf(TIPOS_COMPRA)
    )
    latitude = fields.Float(allow_none=True, load_default=None)
    longitude = fields.Float(allow_none=True, load_default=None)
    lista_precios_id = fields.Integer(allow_none=True, load_default=None)
    estado = fields.Boolean(load_default=True)
    created_at = fields.String(dump_only=True)
    updated_at = fields.String(dump_only=True)


cliente_schema = ClienteSchema()
cliente_update_schema = ClienteSchema(partial=True)
