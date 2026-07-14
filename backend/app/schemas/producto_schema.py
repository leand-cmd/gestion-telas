from marshmallow import Schema, fields, validate


class ProductoSchema(Schema):
    id = fields.Integer(dump_only=True)
    cod_sku = fields.String(required=True, validate=validate.Length(min=1, max=100))
    nro_producto = fields.Integer(allow_none=True, load_default=None)
    descripcion = fields.String(allow_none=True, load_default=None)
    clase = fields.String(allow_none=True, load_default=None)
    categoria = fields.String(allow_none=True, load_default=None)
    origen = fields.String(allow_none=True, load_default=None)
    metros = fields.Float(allow_none=True, load_default=None)
    kilogramos = fields.Float(allow_none=True, load_default=None)
    piezas = fields.Integer(allow_none=True, load_default=None)
    color = fields.String(allow_none=True, load_default=None)
    marca = fields.String(allow_none=True, load_default=None)
    precio = fields.Float(allow_none=True, load_default=None)
    costo = fields.Float(allow_none=True, load_default=None)
    stock_actual = fields.Integer(load_default=0)
    stock_minimo = fields.Integer(load_default=0)
    estado = fields.Boolean(load_default=True)
    imagen_url = fields.String(dump_only=True)
    created_at = fields.String(dump_only=True)
    updated_at = fields.String(dump_only=True)


producto_schema = ProductoSchema()
producto_update_schema = ProductoSchema(partial=True)
