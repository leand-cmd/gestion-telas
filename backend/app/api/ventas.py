import csv
import io

from flask import Blueprint, Response, jsonify, request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from app.extensions import db
from app.models.cliente import Cliente
from app.models.venta import Venta
from app.schemas.venta_schema import (
    venta_estado_pago_schema,
    venta_schema,
    venta_update_schema,
)
from app.utils.numbering import generate_correlative
from app.utils.pagination import paginate
from app.utils.pdf import generate_venta_pdf

ventas_bp = Blueprint("ventas", __name__)

CSV_COLUMNS = [
    "nro_factura",
    "cliente_id",
    "fecha_factura",
    "fecha_entrega",
    "tipo_compra",
    "total",
    "estado_pago",
]


@ventas_bp.get("")
@jwt_required()
def listar_ventas():
    query = Venta.query

    estado_pago = request.args.get("estado_pago")
    if estado_pago:
        query = query.filter(Venta.estado_pago == estado_pago)

    cliente_id = request.args.get("cliente_id")
    if cliente_id:
        query = query.filter(Venta.cliente_id == int(cliente_id))

    desde = request.args.get("desde")
    if desde:
        query = query.filter(Venta.fecha_factura >= desde)

    hasta = request.args.get("hasta")
    if hasta:
        query = query.filter(Venta.fecha_factura <= hasta)

    query = query.order_by(Venta.created_at.desc())

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


@ventas_bp.post("")
@jwt_required()
def crear_venta():
    try:
        data = venta_schema.load(request.get_json(force=True) or {})
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    if not db.session.get(Cliente, data["cliente_id"]):
        return jsonify({"error": "El cliente indicado no existe"}), 400

    venta = Venta(
        nro_factura=generate_correlative(Venta, "nro_factura", "FAC-"),
        cliente_id=data["cliente_id"],
        fecha_factura=data.get("fecha_factura"),
        fecha_entrega=data.get("fecha_entrega"),
        total=data["total"],
        tipo_compra=data.get("tipo_compra"),
        observaciones=data.get("observaciones"),
        estado_pago="pendiente",
    )
    db.session.add(venta)
    db.session.commit()
    return jsonify(venta.to_dict()), 201


@ventas_bp.get("/<int:venta_id>")
@jwt_required()
def obtener_venta(venta_id):
    venta = Venta.query.get_or_404(venta_id)
    return jsonify(venta.to_dict())


@ventas_bp.put("/<int:venta_id>")
@jwt_required()
def actualizar_venta(venta_id):
    venta = Venta.query.get_or_404(venta_id)
    try:
        data = venta_update_schema.load(request.get_json(force=True) or {})
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    for key, value in data.items():
        setattr(venta, key, value)

    db.session.commit()
    return jsonify(venta.to_dict())


@ventas_bp.patch("/<int:venta_id>/estado-pago")
@jwt_required()
def cambiar_estado_pago(venta_id):
    venta = Venta.query.get_or_404(venta_id)
    try:
        data = venta_estado_pago_schema.load(request.get_json(force=True) or {})
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    venta.estado_pago = data["estado_pago"]
    db.session.commit()
    return jsonify(venta.to_dict())


@ventas_bp.delete("/<int:venta_id>")
@jwt_required()
def eliminar_venta(venta_id):
    venta = Venta.query.get_or_404(venta_id)
    if venta.movimientos_stock:
        return (
            jsonify({"error": "No se puede eliminar una venta con movimientos de stock asociados"}),
            409,
        )
    db.session.delete(venta)
    db.session.commit()
    return "", 204


@ventas_bp.get("/<int:venta_id>/pdf")
@jwt_required()
def pdf_venta(venta_id):
    venta = Venta.query.get_or_404(venta_id)
    pdf_bytes = generate_venta_pdf(venta)
    return Response(
        pdf_bytes,
        mimetype="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={venta.nro_factura}.pdf"},
    )


@ventas_bp.get("/export")
@jwt_required()
def exportar_ventas():
    ventas = Venta.query.order_by(Venta.created_at.desc()).all()

    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=CSV_COLUMNS)
    writer.writeheader()
    for venta in ventas:
        row = venta.to_dict()
        writer.writerow({col: row.get(col, "") for col in CSV_COLUMNS})

    return Response(
        buffer.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=ventas.csv"},
    )
