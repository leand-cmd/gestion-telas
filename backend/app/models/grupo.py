from app.extensions import db


class Grupo(db.Model):
    __tablename__ = "grupos"

    id = db.Column(db.Integer, primary_key=True)
    cod_grupo = db.Column(db.String(10), unique=True, nullable=False, index=True)
    nombre = db.Column(db.String(100), nullable=False)

    colecciones = db.relationship("Coleccion", back_populates="grupo")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "cod_grupo": self.cod_grupo,
            "nombre": self.nombre,
        }
