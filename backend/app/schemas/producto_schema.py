from marshmallow import Schema, fields, validate


class ProductoSchema(Schema):
    id = fields.Integer(dump_only=True)
    cod_producto = fields.String(required=True, validate=validate.Length(min=1, max=20))
    proveedor = fields.String(allow_none=True, load_default=None)
    marca = fields.String(allow_none=True, load_default=None)
    coleccion = fields.String(allow_none=True, load_default=None)
    coleccion_id = fields.Integer(allow_none=True, load_default=None)
    nombre_tejido = fields.String(required=True, validate=validate.Length(min=1, max=100))
    cod_color = fields.String(allow_none=True, load_default=None)
    color_general = fields.String(allow_none=True, load_default=None)
    color_descripcion = fields.String(allow_none=True, load_default=None)
    categoria = fields.String(required=True, validate=validate.Length(min=1, max=50))
    sub_categoria = fields.String(allow_none=True, load_default=None)
    tipo_diseno = fields.String(allow_none=True, load_default=None)
    composicion = fields.String(allow_none=True, load_default=None)
    linea_sugerida = fields.String(allow_none=True, load_default=None)
    ancho_cm = fields.Float(allow_none=True, load_default=None)
    gramaje_gm2 = fields.Float(allow_none=True, load_default=None)
    precio_rollo = fields.Float(allow_none=True, load_default=None)
    precio_media_rollo = fields.Float(allow_none=True, load_default=None)
    precio_corte = fields.Float(allow_none=True, load_default=None)
    stock_rollos = fields.Integer(allow_none=True, load_default=0)
    activo = fields.Boolean(load_default=True)
    url_imagen = fields.String(allow_none=True, load_default=None)
    descripcion = fields.String(allow_none=True, load_default=None)
    fecha_creacion = fields.Date(allow_none=True, load_default=None)
    notas = fields.String(allow_none=True, load_default=None)
    created_at = fields.String(dump_only=True)
    updated_at = fields.String(dump_only=True)


class PreciosSchema(Schema):
    """Representa una fila de la lista de precios Karretel (PDF), usada para
    completar precio_rollo/media_rollo/corte de un producto por nombre_tejido."""

    nombre_tejido = fields.String(required=True)
    precio_rollo = fields.Float(required=True)
    precio_media_rollo = fields.Float(allow_none=True, load_default=None)
    precio_corte = fields.Float(allow_none=True, load_default=None)


producto_schema = ProductoSchema()
producto_update_schema = ProductoSchema(partial=True)
precios_schema = PreciosSchema()
