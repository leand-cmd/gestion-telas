from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from app.extensions import db
from app.models.cliente import Cliente
from app.models.usuario import Usuario
from app.models.visita import Visita
from app.schemas.visita_schema import (
    visita_resultado_schema,
    visita_schema,
    visita_update_schema,
)
from app.utils.pagination import paginate

visitas_bp = Blueprint("visitas", __name__)


@visitas_bp.get("")
@jwt_required()
def listar_visitas():
    query = Visita.query

    desde = request.args.get("desde")
    if desde:
        query = query.filter(Visita.fecha >= desde)

    hasta = request.args.get("hasta")
    if hasta:
        query = query.filter(Visita.fecha <= hasta)

    asesor_id = request.args.get("asesor_id")
    if asesor_id:
        query = query.filter(Visita.asesor_id == int(asesor_id))

    estado = request.args.get("estado")
    if estado:
        query = query.filter(Visita.estado == estado)

    query = query.order_by(Visita.fecha.asc(), Visita.hora.asc())

    result = paginate(query)
    return jsonify(
        {
            "items": [v.to_dict() for v in result["items"]],
            "page": result["page"],
            "per_page": result["per_page"],
            "total": result["total"],
            "pages": result["pages"],
        }
    )


@visitas_bp.post("")
@jwt_required()
def crear_visita():
    try:
        data = visita_schema.load(request.get_json(force=True) or {})
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    if not db.session.get(Cliente, data["cliente_id"]):
        return jsonify({"error": "El cliente indicado no existe"}), 400
    if not db.session.get(Usuario, data["asesor_id"]):
        return jsonify({"error": "El asesor indicado no existe"}), 400

    visita = Visita(
        cliente_id=data["cliente_id"],
        asesor_id=data["asesor_id"],
        fecha=data["fecha"],
        hora=data["hora"],
        proposito=data.get("proposito"),
        direccion=data.get("direccion"),
        notas_previas=data.get("notas_previas"),
        estado="programada",
    )
    db.session.add(visita)
    db.session.commit()
    return jsonify(visita.to_dict()), 201


@visitas_bp.get("/<int:visita_id>")
@jwt_required()
def obtener_visita(visita_id):
    visita = Visita.query.get_or_404(visita_id)
    return jsonify(visita.to_dict())


@visitas_bp.put("/<int:visita_id>")
@jwt_required()
def actualizar_visita(visita_id):
    visita = Visita.query.get_or_404(visita_id)
    try:
        data = visita_update_schema.load(request.get_json(force=True) or {})
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    for key, value in data.items():
        setattr(visita, key, value)

    db.session.commit()
    return jsonify(visita.to_dict())


@visitas_bp.patch("/<int:visita_id>/resultado")
@jwt_required()
def registrar_resultado_visita(visita_id):
    visita = Visita.query.get_or_404(visita_id)
    try:
        data = visita_resultado_schema.load(request.get_json(force=True) or {})
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    for key, value in data.items():
        setattr(visita, key, value)
    visita.estado = "realizada"

    db.session.commit()
    return jsonify(visita.to_dict())


@visitas_bp.delete("/<int:visita_id>")
@jwt_required()
def eliminar_visita(visita_id):
    visita = Visita.query.get_or_404(visita_id)
    db.session.delete(visita)
    db.session.commit()
    return "", 204
