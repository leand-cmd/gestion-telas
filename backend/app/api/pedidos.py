import csv
import io
from datetime import date

from flask import Blueprint, Response, current_app, jsonify, request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from app.extensions import db
from app.models.cliente import Cliente
from app.models.pedido import Pedido, PedidoDetalle
from app.models.producto import Producto
from app.models.venta import Venta
from app.schemas.pedido_schema import pedido_schema, pedido_update_schema
from app.utils.email import EmailNotConfiguredError, send_email_with_attachment
from app.utils.numbering import generate_correlative
from app.utils.pagination import paginate
from app.utils.pdf import generate_pedido_pdf

pedidos_bp = Blueprint("pedidos", __name__)

ESTADOS_TRANSICION = {
    "borrador": {"confirmado", "cancelado"},
    "confirmado": {"entregado", "cancelado"},
    "entregado": {"cancelado"},
    "facturado": set(),
    "cancelado": set(),
}

CSV_COLUMNS = [
    "nro_pedido",
    "cliente_id",
    "fecha_pedido",
    "fecha_entrega_estimada",
    "tipo_compra",
    "total",
    "estado",
]


def _build_detalles(detalles_data):
    detalles = []
    total = 0
    for item in detalles_data:
        producto = db.session.get(Producto, item["producto_id"])
        if not producto:
            raise ValueError(f"Producto {item['producto_id']} no existe")
        valor_unitario = item.get("valor_unitario")
        if valor_unitario is None:
            valor_unitario = float(producto.precio or 0)
        subtotal = valor_unitario * item["cantidad"]
        total += subtotal
        detalles.append(
            PedidoDetalle(
                producto_id=producto.id,
                cantidad=item["cantidad"],
                valor_unitario=valor_unitario,
                subtotal=subtotal,
            )
        )
    return detalles, total


@pedidos_bp.get("")
@jwt_required()
def listar_pedidos():
    query = Pedido.query

    estado = request.args.get("estado")
    if estado:
        query = query.filter(Pedido.estado == estado)

    cliente_id = request.args.get("cliente_id")
    if cliente_id:
        query = query.filter(Pedido.cliente_id == int(cliente_id))

    desde = request.args.get("desde")
    if desde:
        query = query.filter(Pedido.fecha_pedido >= desde)

    hasta = request.args.get("hasta")
    if hasta:
        query = query.filter(Pedido.fecha_pedido <= hasta)

    query = query.order_by(Pedido.created_at.desc())

    result = paginate(query)
    return jsonify(
        {
            "items": [p.to_dict(include_detalles=False) for p in result["items"]],
            "page": result["page"],
            "per_page": result["per_page"],
            "total": result["total"],
            "pages": result["pages"],
        }
    )


@pedidos_bp.post("")
@jwt_required()
def crear_pedido():
    try:
        data = pedido_schema.load(request.get_json(force=True) or {})
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    if not db.session.get(Cliente, data["cliente_id"]):
        return jsonify({"error": "El cliente indicado no existe"}), 400

    try:
        detalles, total = _build_detalles(data["detalles"])
    except ValueError as err:
        return jsonify({"error": str(err)}), 400

    if not detalles:
        return jsonify({"error": "El pedido debe tener al menos un detalle"}), 400

    pedido = Pedido(
        nro_pedido=generate_correlative(Pedido, "nro_pedido", "PED-"),
        cliente_id=data["cliente_id"],
        tipo_compra=data.get("tipo_compra"),
        fecha_pedido=data.get("fecha_pedido"),
        fecha_entrega_estimada=data.get("fecha_entrega_estimada"),
        observaciones=data.get("observaciones"),
        total=total,
        estado="borrador",
        detalles=detalles,
    )
    db.session.add(pedido)
    db.session.commit()
    return jsonify(pedido.to_dict()), 201


@pedidos_bp.get("/<int:pedido_id>")
@jwt_required()
def obtener_pedido(pedido_id):
    pedido = Pedido.query.get_or_404(pedido_id)
    return jsonify(pedido.to_dict())


@pedidos_bp.put("/<int:pedido_id>")
@jwt_required()
def actualizar_pedido(pedido_id):
    pedido = Pedido.query.get_or_404(pedido_id)
    if pedido.estado != "borrador":
        return jsonify({"error": "Solo se pueden editar pedidos en borrador"}), 409

    try:
        data = pedido_update_schema.load(request.get_json(force=True) or {})
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    if "cliente_id" in data and not db.session.get(Cliente, data["cliente_id"]):
        return jsonify({"error": "El cliente indicado no existe"}), 400

    if "detalles" in data:
        try:
            detalles, total = _build_detalles(data.pop("detalles"))
        except ValueError as err:
            return jsonify({"error": str(err)}), 400
        pedido.detalles = detalles
        pedido.total = total

    for key, value in data.items():
        setattr(pedido, key, value)

    db.session.commit()
    return jsonify(pedido.to_dict())


@pedidos_bp.patch("/<int:pedido_id>/estado")
@jwt_required()
def cambiar_estado_pedido(pedido_id):
    pedido = Pedido.query.get_or_404(pedido_id)
    nuevo_estado = (request.get_json(force=True) or {}).get("estado")

    if nuevo_estado not in ESTADOS_TRANSICION.get(pedido.estado, set()):
        return (
            jsonify({"error": f"No se puede pasar de '{pedido.estado}' a '{nuevo_estado}'"}),
            400,
        )

    pedido.estado = nuevo_estado
    db.session.commit()
    return jsonify(pedido.to_dict())


@pedidos_bp.delete("/<int:pedido_id>")
@jwt_required()
def eliminar_pedido(pedido_id):
    pedido = Pedido.query.get_or_404(pedido_id)
    if pedido.estado != "borrador":
        return jsonify({"error": "Solo se pueden eliminar pedidos en borrador"}), 409

    db.session.delete(pedido)
    db.session.commit()
    return "", 204


@pedidos_bp.get("/<int:pedido_id>/pdf")
@jwt_required()
def pdf_pedido(pedido_id):
    pedido = Pedido.query.get_or_404(pedido_id)
    pdf_bytes = generate_pedido_pdf(pedido)
    return Response(
        pdf_bytes,
        mimetype="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={pedido.nro_pedido}.pdf"},
    )


@pedidos_bp.post("/<int:pedido_id>/email")
@jwt_required()
def enviar_email_pedido(pedido_id):
    pedido = Pedido.query.get_or_404(pedido_id)
    destinatarios = current_app.config["EMAIL_COLABORADORES"]
    if not destinatarios:
        return jsonify({"error": "No hay destinatarios configurados (EMAIL_COLABORADORES)"}), 400

    pdf_bytes = generate_pedido_pdf(pedido)
    cliente_nombre = pedido.cliente.razon_social if pedido.cliente else "-"
    try:
        send_email_with_attachment(
            to=destinatarios,
            subject=f"Pedido {pedido.nro_pedido}",
            body=f"Se adjunta el pedido {pedido.nro_pedido} del cliente {cliente_nombre}.",
            attachment_bytes=pdf_bytes,
            attachment_filename=f"{pedido.nro_pedido}.pdf",
        )
    except (EmailNotConfiguredError, ValueError) as err:
        return jsonify({"error": str(err)}), 400

    return jsonify({"status": "enviado"})


@pedidos_bp.post("/<int:pedido_id>/convertir-a-venta")
@jwt_required()
def convertir_pedido_a_venta(pedido_id):
    pedido = Pedido.query.get_or_404(pedido_id)
    if pedido.estado not in ("confirmado", "entregado"):
        return (
            jsonify({"error": "Solo se pueden facturar pedidos confirmados o entregados"}),
            409,
        )

    venta = Venta(
        nro_factura=generate_correlative(Venta, "nro_factura", "FAC-"),
        pedido_id=pedido.id,
        cliente_id=pedido.cliente_id,
        fecha_factura=date.today(),
        fecha_entrega=pedido.fecha_entrega_estimada,
        total=pedido.total,
        tipo_compra=pedido.tipo_compra,
        estado_pago="pendiente",
    )
    pedido.estado = "facturado"
    db.session.add(venta)
    db.session.commit()
    return jsonify(venta.to_dict()), 201


@pedidos_bp.get("/export")
@jwt_required()
def exportar_pedidos():
    pedidos = Pedido.query.order_by(Pedido.created_at.desc()).all()

    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=CSV_COLUMNS)
    writer.writeheader()
    for pedido in pedidos:
        row = pedido.to_dict(include_detalles=False)
        writer.writerow({col: row.get(col, "") for col in CSV_COLUMNS})

    return Response(
        buffer.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=pedidos.csv"},
    )
