from marshmallow import Schema, fields, validate

from app.models.visita import PROPOSITOS, RESULTADOS, TIPOS_GESTION


class VisitaSchema(Schema):
    id = fields.Integer(dump_only=True)
    cliente_id = fields.Integer(required=True)
    asesor_id = fields.Integer(required=True)
    fecha = fields.Date(required=True)
    hora = fields.Time(allow_none=True, load_default=None)
    proposito = fields.String(allow_none=True, load_default=None, validate=validate.OneOf(PROPOSITOS))
    direccion = fields.String(allow_none=True, load_default=None)
    notas_previas = fields.String(allow_none=True, load_default=None)
    estado = fields.String(dump_only=True)
    duracion_actual = fields.Integer(dump_only=True)
    presente_cliente = fields.Boolean(dump_only=True)
    productos_presentados = fields.String(dump_only=True)
    resultado = fields.String(dump_only=True)
    tipo_gestion = fields.String(dump_only=True)
    notas_visita = fields.String(dump_only=True)
    proxima_accion = fields.String(dump_only=True)
    created_at = fields.String(dump_only=True)
    updated_at = fields.String(dump_only=True)


class VisitaUpdateSchema(Schema):
    cliente_id = fields.Integer()
    asesor_id = fields.Integer()
    fecha = fields.Date()
    hora = fields.Time()
    proposito = fields.String(allow_none=True, validate=validate.OneOf(PROPOSITOS))
    direccion = fields.String(allow_none=True)
    notas_previas = fields.String(allow_none=True)


class VisitaResultadoSchema(Schema):
    # Campos sin load_default: si no vienen en el request, quedan afuera del
    # dict cargado y el endpoint no los toca (no pisa datos ya guardados).
    duracion_actual = fields.Integer(allow_none=True)
    presente_cliente = fields.Boolean(allow_none=True)
    productos_presentados = fields.String(allow_none=True)
    resultado = fields.String(allow_none=True, validate=validate.OneOf(RESULTADOS))
    tipo_gestion = fields.String(allow_none=True, load_default=None, validate=validate.OneOf(TIPOS_GESTION))
    notas_visita = fields.String(allow_none=True)
    proxima_accion = fields.String(allow_none=True)


visita_schema = VisitaSchema()
visita_update_schema = VisitaUpdateSchema(partial=True)
visita_resultado_schema = VisitaResultadoSchema()
