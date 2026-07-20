from datetime import datetime, timezone

from app.extensions import db


class Producto(db.Model):
    __tablename__ = "productos"

    id = db.Column(db.Integer, primary_key=True)
    cod_producto = db.Column(db.String(20), unique=True, nullable=False, index=True)
    cod_categoria = db.Column(db.String(10))
    cod_color = db.Column(db.String(20))
    nombre_tejido = db.Column(db.String(100), nullable=False, index=True)
    color_general = db.Column(db.String(50))
    color_descripcion = db.Column(db.String(255))
    categoria = db.Column(db.String(50), nullable=False, index=True)
    sub_categoria = db.Column(db.String(50))
    composicion = db.Column(db.String(100))
    ancho_cm = db.Column(db.Float)
    gramaje_gm2 = db.Column(db.Float)
    precio_rollo = db.Column(db.Float)
    precio_media_rollo = db.Column(db.Float)
    precio_corte = db.Column(db.Float)
    unidad_medida = db.Column(db.String(50), default="metro")
    stock_rollos = db.Column(db.Integer, default=0)
    activo = db.Column(db.Boolean, default=True, nullable=False, index=True)
    url_imagen = db.Column(db.String(500))
    descripcion = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    detalles_pedido = db.relationship("PedidoDetalle", back_populates="producto")
    movimientos_stock = db.relationship("StockMovimiento", back_populates="producto")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "cod_producto": self.cod_producto,
            "cod_categoria": self.cod_categoria,
            "cod_color": self.cod_color,
            "nombre_tejido": self.nombre_tejido,
            "color_general": self.color_general,
            "color_descripcion": self.color_descripcion,
            "categoria": self.categoria,
            "sub_categoria": self.sub_categoria,
            "composicion": self.composicion,
            "ancho_cm": self.ancho_cm,
            "gramaje_gm2": self.gramaje_gm2,
            "precio_rollo": self.precio_rollo,
            "precio_media_rollo": self.precio_media_rollo,
            "precio_corte": self.precio_corte,
            "unidad_medida": self.unidad_medida,
            "stock_rollos": self.stock_rollos,
            "activo": self.activo,
            "url_imagen": self.url_imagen,
            "descripcion": self.descripcion,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
