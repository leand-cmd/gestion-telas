from datetime import datetime, timezone

from app.extensions import db

CANALES = ("Mayorista", "Minorista", "Distribuidora", "Fabricante")
TIPOS_COMPRA = ("Contado", "Credito", "Cheque")


class Cliente(db.Model):
    __tablename__ = "clientes"

    id = db.Column(db.Integer, primary_key=True)
    codigo_cliente = db.Column(db.String(50), unique=True, index=True, nullable=True)
    ruc = db.Column(db.String(50), unique=True, nullable=False, index=True)
    razon_social = db.Column(db.String(255), nullable=False, index=True)
    localidad = db.Column(db.String(255), index=True)
    barrio = db.Column(db.String(255))
    direccion = db.Column(db.String(500))
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(120))
    canal = db.Column(db.String(50))
    sub_canal = db.Column(db.String(100))
    tipo_compra = db.Column(db.String(50))
    latitude = db.Column(db.Numeric(10, 7))
    longitude = db.Column(db.Numeric(10, 7))
    lista_precios_id = db.Column(db.Integer)
    estado = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    pedidos = db.relationship("Pedido", back_populates="cliente")
    ventas = db.relationship("Venta", back_populates="cliente")
    visitas = db.relationship("Visita", back_populates="cliente")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "codigo_cliente": self.codigo_cliente,
            "ruc": self.ruc,
            "razon_social": self.razon_social,
            "localidad": self.localidad,
            "barrio": self.barrio,
            "direccion": self.direccion,
            "telefono": self.telefono,
            "email": self.email,
            "canal": self.canal,
            "sub_canal": self.sub_canal,
            "tipo_compra": self.tipo_compra,
            "latitude": float(self.latitude) if self.latitude is not None else None,
            "longitude": float(self.longitude) if self.longitude is not None else None,
            "lista_precios_id": self.lista_precios_id,
            "estado": self.estado,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
