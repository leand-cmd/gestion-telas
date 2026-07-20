from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from app.extensions import db
from app.models.coleccion import Coleccion
from app.schemas.coleccion_schema import coleccion_schema, coleccion_update_schema
from app.utils.cloudinary_upload import CloudinaryNotConfiguredError, upload_imagen
from app.utils.pagination import paginate

colecciones_bp = Blueprint("colecciones", __name__)

ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}


@colecciones_bp.get("")
@jwt_required()
def listar_colecciones():
    query = Coleccion.query.order_by(Coleccion.nombre.asc())
    result = paginate(query, default_per_page=100)
    return jsonify(
        {
            "items": [c.to_dict() for c in result["items"]],
            "page": result["page"],
            "per_page": result["per_page"],
            "total": result["total"],
            "pages": result["pages"],
        }
    )


@colecciones_bp.post("")
@jwt_required()
def crear_coleccion():
    try:
        data = coleccion_schema.load(request.get_json(force=True) or {})
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    if Coleccion.query.filter_by(nombre=data["nombre"]).first():
        return jsonify({"error": "Ya existe una colección con ese nombre"}), 409

    coleccion = Coleccion(**data)
    db.session.add(coleccion)
    db.session.commit()
    return jsonify(coleccion.to_dict()), 201


@colecciones_bp.put("/<int:coleccion_id>")
@jwt_required()
def actualizar_coleccion(coleccion_id):
    coleccion = Coleccion.query.get_or_404(coleccion_id)
    try:
        data = coleccion_update_schema.load(request.get_json(force=True) or {})
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    if "nombre" in data and data["nombre"] != coleccion.nombre:
        if Coleccion.query.filter_by(nombre=data["nombre"]).first():
            return jsonify({"error": "Ya existe una colección con ese nombre"}), 409

    for key, value in data.items():
        setattr(coleccion, key, value)

    db.session.commit()
    return jsonify(coleccion.to_dict())


@colecciones_bp.delete("/<int:coleccion_id>")
@jwt_required()
def eliminar_coleccion(coleccion_id):
    coleccion = Coleccion.query.get_or_404(coleccion_id)
    db.session.delete(coleccion)
    db.session.commit()
    return "", 204


@colecciones_bp.post("/upload")
@jwt_required()
def upload_imagen_coleccion():
    file = request.files.get("file")
    if not file or not file.filename:
        return jsonify({"error": "No se envio ninguna imagen"}), 400

    ext = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        return jsonify({"error": "Formato de imagen no soportado"}), 400

    try:
        url = upload_imagen(file, folder="colecciones")
    except CloudinaryNotConfiguredError as err:
        return jsonify({"error": str(err)}), 400

    return jsonify({"url": url})
