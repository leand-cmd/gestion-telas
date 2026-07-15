from datetime import datetime, timezone

from app.extensions import db


class Pedido(db.Model):
    __tablename__ = "pedidos"

    id = db.Column(db.Integer, primary_key=True)
    nro_pedido = db.Column(db.String(50), unique=True, nullable=False, index=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey("clientes.id"), nullable=False)
    tipo_compra = db.Column(db.String(50))
    fecha_pedido = db.Column(db.Date)
    fecha_entrega_estimada = db.Column(db.Date)
    total = db.Column(db.Numeric(14, 2), default=0)
    observaciones = db.Column(db.Text)
    estado = db.Column(db.String(50), default="Pendiente", nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    cliente = db.relationship("Cliente", back_populates="pedidos")
    detalles = db.relationship(
        "PedidoDetalle", back_populates="pedido", cascade="all, delete-orphan"
    )
    ventas = db.relationship("Venta", back_populates="pedido")

    def to_dict(self, include_detalles: bool = True) -> dict:
        data = {
            "id": self.id,
            "nro_pedido": self.nro_pedido,
            "cliente_id": self.cliente_id,
            "cliente": self.cliente.to_dict() if self.cliente else None,
            "tipo_compra": self.tipo_compra,
            "fecha_pedido": self.fecha_pedido.isoformat() if self.fecha_pedido else None,
            "fecha_entrega_estimada": (
                self.fecha_entrega_estimada.isoformat() if self.fecha_entrega_estimada else None
            ),
            "total": float(self.total) if self.total is not None else 0,
            "observaciones": self.observaciones,
            "estado": self.estado,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
        if include_detalles:
            data["detalles"] = [d.to_dict() for d in self.detalles]
        return data


class PedidoDetalle(db.Model):
    __tablename__ = "pedido_detalles"

    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey("pedidos.id"), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey("productos.id"), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    metros = db.Column(db.Numeric(10, 3))
    kilogramos = db.Column(db.Numeric(10, 3))
    valor_unitario = db.Column(db.Numeric(12, 2))
    subtotal = db.Column(db.Numeric(14, 2))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    pedido = db.relationship("Pedido", back_populates="detalles")
    producto = db.relationship("Producto", back_populates="detalles_pedido")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "pedido_id": self.pedido_id,
            "producto_id": self.producto_id,
            "producto": self.producto.to_dict() if self.producto else None,
            "cantidad": self.cantidad,
            "metros": float(self.metros) if self.metros is not None else None,
            "kilogramos": float(self.kilogramos) if self.kilogramos is not None else None,
            "valor_unitario": float(self.valor_unitario) if self.valor_unitario is not None else None,
            "subtotal": float(self.subtotal) if self.subtotal is not None else None,
        }
