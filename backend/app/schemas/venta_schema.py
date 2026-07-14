from marshmallow import Schema, fields, validate

ESTADOS_PAGO = ("pendiente", "pagado", "vencido")


class VentaSchema(Schema):
    id = fields.Integer(dump_only=True)
    nro_factura = fields.String(dump_only=True)
    pedido_id = fields.Integer(dump_only=True)
    cliente_id = fields.Integer(required=True)
    fecha_factura = fields.Date(allow_none=True, load_default=None)
    fecha_entrega = fields.Date(allow_none=True, load_default=None)
    total = fields.Float(required=True, validate=validate.Range(min=0))
    tipo_compra = fields.String(allow_none=True, load_default=None)
    estado_pago = fields.String(dump_only=True)
    observaciones = fields.String(allow_none=True, load_default=None)
    created_at = fields.String(dump_only=True)
    updated_at = fields.String(dump_only=True)


class VentaUpdateSchema(Schema):
    fecha_factura = fields.Date(allow_none=True)
    fecha_entrega = fields.Date(allow_none=True)
    tipo_compra = fields.String(allow_none=True)
    observaciones = fields.String(allow_none=True)


class VentaEstadoPagoSchema(Schema):
    estado_pago = fields.String(required=True, validate=validate.OneOf(ESTADOS_PAGO))


venta_schema = VentaSchema()
venta_update_schema = VentaUpdateSchema(partial=True)
venta_estado_pago_schema = VentaEstadoPagoSchema()
