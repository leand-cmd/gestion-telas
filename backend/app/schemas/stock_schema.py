from marshmallow import Schema, fields, validate

TIPOS_MOVIMIENTO = ("entrada", "salida", "ajuste")


class StockMovimientoSchema(Schema):
    id = fields.Integer(dump_only=True)
    producto_id = fields.Integer(required=True)
    tipo = fields.String(required=True, validate=validate.OneOf(TIPOS_MOVIMIENTO))
    cantidad = fields.Integer(required=True, validate=validate.Range(min=1))
    motivo = fields.String(allow_none=True, load_default=None)
    created_at = fields.String(dump_only=True)


stock_movimiento_schema = StockMovimientoSchema()
