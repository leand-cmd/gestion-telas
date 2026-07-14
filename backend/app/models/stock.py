from datetime import datetime, timezone

from app.extensions import db


class Stock(db.Model):
    __tablename__ = "stock"

    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey("productos.id"), nullable=False)
    cantidad_actual = db.Column(db.Integer, default=0)
    stock_minimo = db.Column(db.Integer, default=0)
    last_updated = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    producto = db.relationship("Producto")


class StockMovimiento(db.Model):
    __tablename__ = "stock_movimientos"

    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey("productos.id"), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # entrada, salida, ajuste
    cantidad = db.Column(db.Integer, nullable=False)
    motivo = db.Column(db.String(255))
    venta_id = db.Column(db.Integer, db.ForeignKey("ventas.id"))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    producto = db.relationship("Producto", back_populates="movimientos_stock")
    venta = db.relationship("Venta", back_populates="movimientos_stock")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "producto_id": self.producto_id,
            "producto": self.producto.to_dict() if self.producto else None,
            "tipo": self.tipo,
            "cantidad": self.cantidad,
            "motivo": self.motivo,
            "venta_id": self.venta_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
