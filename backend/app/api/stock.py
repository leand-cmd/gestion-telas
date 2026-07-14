from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from sqlalchemy import or_

from app.extensions import db
from app.models.producto import Producto
from app.models.stock import StockMovimiento
from app.schemas.stock_schema import stock_movimiento_schema
from app.utils.pagination import paginate

stock_bp = Blueprint("stock", __name__)


def _producto_stock_dict(producto: Producto) -> dict:
    data = producto.to_dict()
    data["bajo_minimo"] = (
        producto.stock_minimo is not None and producto.stock_actual < producto.stock_minimo
    )
    return data


@stock_bp.get("")
@jwt_required()
def listar_stock():
    query = Producto.query

    q = request.args.get("q", "").strip()
    if q:
        like = f"%{q}%"
        query = query.filter(or_(Producto.cod_sku.ilike(like), Producto.descripcion.ilike(like)))

    if (request.args.get("bajo_minimo") or "").lower() == "true":
        query = query.filter(Producto.stock_actual < Producto.stock_minimo)

    query = query.order_by(Producto.cod_sku.asc())

    result = paginate(query)
    return jsonify(
        {
            "items": [_producto_stock_dict(p) for p in result["items"]],
            "page": result["page"],
            "per_page": result["per_page"],
            "total": result["total"],
            "pages": result["pages"],
        }
    )


@stock_bp.get("/movimientos")
@jwt_required()
def listar_movimientos():
    query = StockMovimiento.query

    producto_id = request.args.get("producto_id")
    if producto_id:
        query = query.filter(StockMovimiento.producto_id == int(producto_id))

    query = query.order_by(StockMovimiento.created_at.desc())

    result = paginate(query)
    return jsonify(
        {
            "items": [m.to_dict() for m in result["items"]],
            "page": result["page"],
            "per_page": result["per_page"],
            "total": result["total"],
            "pages": result["pages"],
        }
    )


@stock_bp.post("/movimientos")
@jwt_required()
def crear_movimiento():
    try:
        data = stock_movimiento_schema.load(request.get_json(force=True) or {})
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    producto = db.session.get(Producto, data["producto_id"])
    if not producto:
        return jsonify({"error": "El producto indicado no existe"}), 400

    delta = data["cantidad"] if data["tipo"] in ("entrada", "ajuste") else -data["cantidad"]
    if producto.stock_actual + delta < 0:
        return jsonify({"error": "El movimiento dejaria el stock en negativo"}), 400

    producto.stock_actual += delta
    movimiento = StockMovimiento(
        producto_id=producto.id,
        tipo=data["tipo"],
        cantidad=data["cantidad"],
        motivo=data.get("motivo"),
    )
    db.session.add(movimiento)
    db.session.commit()
    return jsonify(movimiento.to_dict()), 201
