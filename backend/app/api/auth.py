from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from marshmallow import ValidationError

from app.extensions import db
from app.models.usuario import Usuario
from app.schemas.auth_schema import login_schema, register_schema

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/register")
def register():
    try:
        data = register_schema.load(request.get_json(force=True) or {})
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    if Usuario.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Ya existe un usuario con ese email"}), 409

    usuario = Usuario(email=data["email"], nombre=data["nombre"], rol=data["rol"])
    usuario.set_password(data["password"])
    db.session.add(usuario)
    db.session.commit()

    token = create_access_token(
        identity=str(usuario.id), additional_claims={"rol": usuario.rol}
    )
    return jsonify({"token": token, "usuario": usuario.to_dict()}), 201


@auth_bp.post("/login")
def login():
    try:
        data = login_schema.load(request.get_json(force=True) or {})
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    usuario = Usuario.query.filter_by(email=data["email"]).first()
    if not usuario or not usuario.check_password(data["password"]):
        return jsonify({"error": "Credenciales invalidas"}), 401

    if not usuario.activo:
        return jsonify({"error": "Usuario desactivado"}), 403

    token = create_access_token(
        identity=str(usuario.id), additional_claims={"rol": usuario.rol}
    )
    return jsonify({"token": token, "usuario": usuario.to_dict()})


@auth_bp.get("/me")
@jwt_required()
def me():
    usuario = Usuario.query.get_or_404(int(get_jwt_identity()))
    return jsonify(usuario.to_dict())
