from datetime import datetime, timezone

from app.extensions import db


class Venta(db.Model):
    __tablename__ = "ventas"

    id = db.Column(db.Integer, primary_key=True)
    nro_factura = db.Column(db.String(50), unique=True, nullable=False, index=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey("pedidos.id"))
    cliente_id = db.Column(db.Integer, db.ForeignKey("clientes.id"), nullable=False)
    fecha_factura = db.Column(db.Date)
    fecha_entrega = db.Column(db.Date)
    total = db.Column(db.Numeric(14, 2), default=0)
    tipo_compra = db.Column(db.String(50))
    estado_pago = db.Column(db.String(50), default="pendiente", nullable=False)
    observaciones = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    pedido = db.relationship("Pedido", back_populates="ventas")
    cliente = db.relationship("Cliente", back_populates="ventas")
    movimientos_stock = db.relationship("StockMovimiento", back_populates="venta")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nro_factura": self.nro_factura,
            "pedido_id": self.pedido_id,
            "cliente_id": self.cliente_id,
            "cliente": self.cliente.to_dict() if self.cliente else None,
            "fecha_factura": self.fecha_factura.isoformat() if self.fecha_factura else None,
            "fecha_entrega": self.fecha_entrega.isoformat() if self.fecha_entrega else None,
            "total": float(self.total) if self.total is not None else 0,
            "tipo_compra": self.tipo_compra,
            "estado_pago": self.estado_pago,
            "observaciones": self.observaciones,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
