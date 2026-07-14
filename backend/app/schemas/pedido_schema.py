from marshmallow import Schema, fields, validate


class PedidoDetalleSchema(Schema):
    id = fields.Integer(dump_only=True)
    producto_id = fields.Integer(required=True)
    cantidad = fields.Integer(required=True, validate=validate.Range(min=1))
    valor_unitario = fields.Float(allow_none=True, load_default=None)


class PedidoSchema(Schema):
    id = fields.Integer(dump_only=True)
    nro_pedido = fields.String(dump_only=True)
    cliente_id = fields.Integer(required=True)
    tipo_compra = fields.String(allow_none=True, load_default=None)
    fecha_pedido = fields.Date(allow_none=True, load_default=None)
    fecha_entrega_estimada = fields.Date(allow_none=True, load_default=None)
    observaciones = fields.String(allow_none=True, load_default=None)
    estado = fields.String(dump_only=True)
    total = fields.Float(dump_only=True)
    detalles = fields.List(fields.Nested(PedidoDetalleSchema), required=True)
    created_at = fields.String(dump_only=True)
    updated_at = fields.String(dump_only=True)


class PedidoUpdateSchema(Schema):
    cliente_id = fields.Integer()
    tipo_compra = fields.String(allow_none=True)
    fecha_pedido = fields.Date(allow_none=True)
    fecha_entrega_estimada = fields.Date(allow_none=True)
    observaciones = fields.String(allow_none=True)
    detalles = fields.List(fields.Nested(PedidoDetalleSchema))


pedido_schema = PedidoSchema()
pedido_update_schema = PedidoUpdateSchema(partial=True)
