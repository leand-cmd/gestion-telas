from datetime import datetime, timezone

from app.extensions import db

CLASES = ("Algodon", "Poliester", "Mezcla", "Lino")
CATEGORIAS = ("Tela", "Hilo", "Accesorios")
ORIGENES = ("Importado", "Nacional")


class Producto(db.Model):
    __tablename__ = "productos"

    id = db.Column(db.Integer, primary_key=True)
    cod_sku = db.Column(db.String(100), unique=True, nullable=False, index=True)
    nro_producto = db.Column(db.Integer, unique=True)
    descripcion = db.Column(db.Text)
    clase = db.Column(db.String(50))
    categoria = db.Column(db.String(50))
    origen = db.Column(db.String(50))
    metros = db.Column(db.Numeric(10, 3))
    kilogramos = db.Column(db.Numeric(10, 3))
    piezas = db.Column(db.Integer)
    color = db.Column(db.String(100))
    marca = db.Column(db.String(255))
    precio = db.Column(db.Numeric(12, 2))
    costo = db.Column(db.Numeric(12, 2))
    stock_actual = db.Column(db.Integer, default=0, nullable=False)
    stock_minimo = db.Column(db.Integer, default=0)
    estado = db.Column(db.Boolean, default=True, nullable=False)
    imagen_url = db.Column(db.String(500))
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
            "cod_sku": self.cod_sku,
            "nro_producto": self.nro_producto,
            "descripcion": self.descripcion,
            "clase": self.clase,
            "categoria": self.categoria,
            "origen": self.origen,
            "metros": float(self.metros) if self.metros is not None else None,
            "kilogramos": float(self.kilogramos) if self.kilogramos is not None else None,
            "piezas": self.piezas,
            "color": self.color,
            "marca": self.marca,
            "precio": float(self.precio) if self.precio is not None else None,
            "costo": float(self.costo) if self.costo is not None else None,
            "stock_actual": self.stock_actual,
            "stock_minimo": self.stock_minimo,
            "estado": self.estado,
            "imagen_url": self.imagen_url,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
