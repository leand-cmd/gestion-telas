from datetime import datetime, timezone

from app.extensions import db

PROPOSITOS = ("Consulta", "Oferta", "Seguimiento", "Cierre")
RESULTADOS = ("Interesado", "No interesado", "Requiere seguimiento")
TIPOS_GESTION = (
    "Solicita Muestras",
    "Entrega de Muestras",
    "Venta Exitosa",
    "Sin Contacto",
    "Visita Cancelada",
    "Visita Reprogramada",
    "Visita de Seguimiento",
    "Visita sin éxito",
)


class Visita(db.Model):
    __tablename__ = "visitas"

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey("clientes.id"), nullable=False)
    asesor_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)
    proposito = db.Column(db.String(50))
    direccion = db.Column(db.String(500))
    notas_previas = db.Column(db.Text)
    estado = db.Column(db.String(50), default="programada", nullable=False)
    duracion_actual = db.Column(db.Integer)
    presente_cliente = db.Column(db.Boolean)
    productos_presentados = db.Column(db.Text)
    resultado = db.Column(db.String(50))
    tipo_gestion = db.Column(db.String(100))
    notas_visita = db.Column(db.Text)
    proxima_accion = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    cliente = db.relationship("Cliente", back_populates="visitas")
    asesor = db.relationship("Usuario", back_populates="visitas")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "cliente_id": self.cliente_id,
            "cliente": self.cliente.to_dict() if self.cliente else None,
            "asesor_id": self.asesor_id,
            "asesor": self.asesor.to_dict() if self.asesor else None,
            "fecha": self.fecha.isoformat() if self.fecha else None,
            "hora": self.hora.isoformat(timespec="minutes") if self.hora else None,
            "proposito": self.proposito,
            "direccion": self.direccion,
            "notas_previas": self.notas_previas,
            "estado": self.estado,
            "duracion_actual": self.duracion_actual,
            "presente_cliente": self.presente_cliente,
            "productos_presentados": self.productos_presentados,
            "resultado": self.resultado,
            "tipo_gestion": self.tipo_gestion,
            "notas_visita": self.notas_visita,
            "proxima_accion": self.proxima_accion,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
