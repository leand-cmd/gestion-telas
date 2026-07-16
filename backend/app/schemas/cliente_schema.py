from marshmallow import Schema, fields, pre_load, validate

from app.models.cliente import CANALES, TIPOS_COMPRA

CAMPOS_OPCIONALES_NORMALIZABLES = (
    "codigo_cliente",
    "ruc",
    "localidad",
    "barrio",
    "direccion",
    "telefono",
    "email",
    "canal",
    "sub_canal",
    "tipo_compra",
)


class ClienteSchema(Schema):
    id = fields.Integer(dump_only=True)
    codigo_cliente = fields.String(allow_none=True, load_default=None, validate=validate.Length(max=50))
    ruc = fields.String(allow_none=True, load_default=None, validate=validate.Length(max=50))
    razon_social = fields.String(required=True, validate=validate.Length(min=1, max=255))
    localidad = fields.String(allow_none=True, load_default=None)
    barrio = fields.String(allow_none=True, load_default=None)
    direccion = fields.String(allow_none=True, load_default=None)
    telefono = fields.String(allow_none=True, load_default=None, validate=validate.Length(max=20))
    email = fields.Email(allow_none=True, load_default=None)
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

    @pre_load
    def normalizar_vacios(self, data, **kwargs):
        if not isinstance(data, dict):
            return data
        data = dict(data)
        for campo in CAMPOS_OPCIONALES_NORMALIZABLES:
            if data.get(campo) == "":
                data[campo] = None
        return data


cliente_schema = ClienteSchema()
cliente_update_schema = ClienteSchema(partial=True)
