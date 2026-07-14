from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from app.extensions import db
from app.models.usuario import Usuario
from app.schemas.usuario_schema import usuario_schema, usuario_update_schema
from app.utils.pagination import paginate
from app.utils.roles import require_role

usuarios_bp = Blueprint("usuarios", __name__)


@usuarios_bp.get("")
@require_role("Admin")
def listar_usuarios():
    query = Usuario.query.order_by(Usuario.nombre.asc())
    result = paginate(query)
    return jsonify(
        {
            "items": [u.to_dict() for u in result["items"]],
            "page": result["page"],
            "per_page": result["per_page"],
            "total": result["total"],
            "pages": result["pages"],
        }
    )


@usuarios_bp.get("/asesores")
@jwt_required()
def listar_asesores():
    usuarios = Usuario.query.filter_by(activo=True).order_by(Usuario.nombre.asc()).all()
    return jsonify([u.to_dict() for u in usuarios])


@usuarios_bp.post("")
@require_role("Admin")
def crear_usuario():
    try:
        data = usuario_schema.load(request.get_json(force=True) or {})
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    if Usuario.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Ya existe un usuario con ese email"}), 409

    usuario = Usuario(
        email=data["email"], nombre=data["nombre"], rol=data["rol"], activo=data["activo"]
    )
    usuario.set_password(data["password"])
    db.session.add(usuario)
    db.session.commit()
    return jsonify(usuario.to_dict()), 201


@usuarios_bp.put("/<int:usuario_id>")
@require_role("Admin")
def actualizar_usuario(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)
    try:
        data = usuario_update_schema.load(request.get_json(force=True) or {})
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    if "email" in data and data["email"] != usuario.email:
        if Usuario.query.filter_by(email=data["email"]).first():
            return jsonify({"error": "Ya existe un usuario con ese email"}), 409

    password = data.pop("password", None)
    for key, value in data.items():
        setattr(usuario, key, value)
    if password:
        usuario.set_password(password)

    db.session.commit()
    return jsonify(usuario.to_dict())


@usuarios_bp.patch("/<int:usuario_id>/estado")
@require_role("Admin")
def cambiar_estado_usuario(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)
    activo = (request.get_json(force=True) or {}).get("activo")
    if not isinstance(activo, bool):
        return jsonify({"error": "El campo 'activo' es requerido y debe ser booleano"}), 400

    usuario.activo = activo
    db.session.commit()
    return jsonify(usuario.to_dict())
