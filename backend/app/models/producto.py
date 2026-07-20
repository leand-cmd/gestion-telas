from datetime import datetime, timezone

from app.extensions import db


class Producto(db.Model):
    __tablename__ = "productos"

    id = db.Column(db.Integer, primary_key=True)
    cod_producto = db.Column(db.String(20), unique=True, nullable=False, index=True)
    proveedor = db.Column(db.String(50))
    marca = db.Column(db.String(50))
    coleccion = db.Column(db.String(100))
    coleccion_id = db.Column(db.Integer, db.ForeignKey("colecciones.id"), nullable=True, index=True)
    nombre_tejido = db.Column(db.String(100), nullable=False, index=True)
    cod_color = db.Column(db.String(20))
    color_general = db.Column(db.String(50))
    color_descripcion = db.Column(db.String(255))
    categoria = db.Column(db.String(50), nullable=False, index=True)
    sub_categoria = db.Column(db.String(50))
    tipo_diseno = db.Column(db.String(50))
    composicion = db.Column(db.String(100))
    linea_sugerida = db.Column(db.String(100))
    ancho_cm = db.Column(db.Float)
    gramaje_gm2 = db.Column(db.Float)
    precio_rollo = db.Column(db.Float)
    precio_media_rollo = db.Column(db.Float)
    precio_corte = db.Column(db.Float)
    stock_rollos = db.Column(db.Integer, default=0)
    activo = db.Column(db.Boolean, default=True, nullable=False, index=True)
    url_imagen = db.Column(db.String(500))
    descripcion = db.Column(db.Text)
    fecha_creacion = db.Column(db.Date)
    notas = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    detalles_pedido = db.relationship("PedidoDetalle", back_populates="producto")
    movimientos_stock = db.relationship("StockMovimiento", back_populates="producto")
    coleccion_ref = db.relationship("Coleccion")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "cod_producto": self.cod_producto,
            "proveedor": self.proveedor,
            "marca": self.marca,
            "coleccion": self.coleccion,
            "coleccion_id": self.coleccion_id,
            "nombre_tejido": self.nombre_tejido,
            "cod_color": self.cod_color,
            "color_general": self.color_general,
            "color_descripcion": self.color_descripcion,
            "categoria": self.categoria,
            "sub_categoria": self.sub_categoria,
            "tipo_diseno": self.tipo_diseno,
            "composicion": self.composicion,
            "linea_sugerida": self.linea_sugerida,
            "ancho_cm": self.ancho_cm,
            "gramaje_gm2": self.gramaje_gm2,
            "precio_rollo": self.precio_rollo,
            "precio_media_rollo": self.precio_media_rollo,
            "precio_corte": self.precio_corte,
            "stock_rollos": self.stock_rollos,
            "activo": self.activo,
            "url_imagen": self.url_imagen,
            "descripcion": self.descripcion,
            "fecha_creacion": self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            "notas": self.notas,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
