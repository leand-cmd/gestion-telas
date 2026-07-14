from datetime import datetime, timezone

from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db

ROLES = ("Admin", "Asesor Comercial", "Gerente", "Vendedor")


class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    nombre = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(50), nullable=False, default="Vendedor")
    foto_url = db.Column(db.String(500))
    activo = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    visitas = db.relationship("Visita", back_populates="asesor")

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "email": self.email,
            "nombre": self.nombre,
            "rol": self.rol,
            "foto_url": self.foto_url,
            "activo": self.activo,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
