from datetime import datetime, timezone

from app.extensions import db


class Coleccion(db.Model):
    __tablename__ = "colecciones"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False, index=True)
    descripcion = db.Column(db.Text)
    imagen_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "imagen_url": self.imagen_url,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
