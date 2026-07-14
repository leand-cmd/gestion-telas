import csv
import io
import os
import uuid

from flask import Blueprint, Response, current_app, jsonify, request, send_from_directory
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from sqlalchemy import or_
from werkzeug.utils import secure_filename

from app.extensions import db
from app.models.producto import Producto
from app.schemas.producto_schema import producto_schema, producto_update_schema
from app.utils.importers import ImportError_, build_import_report, read_tabular_file
from app.utils.pagination import paginate

productos_bp = Blueprint("productos", __name__)

CSV_COLUMNS = [
    "cod_sku",
    "nro_producto",
    "descripcion",
    "clase",
    "categoria",
    "origen",
    "metros",
    "kilogramos",
    "piezas",
    "color",
    "marca",
    "precio",
    "costo",
    "stock_actual",
    "stock_minimo",
    "estado",
]

ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}


@productos_bp.get("")
@jwt_required()
def listar_productos():
    query = Producto.query

    q = request.args.get("q", "").strip()
    if q:
        like = f"%{q}%"
        query = query.filter(
            or_(
                Producto.cod_sku.ilike(like),
                Producto.descripcion.ilike(like),
                Producto.color.ilike(like),
            )
        )

    categoria = request.args.get("categoria")
    if categoria:
        query = query.filter(Producto.categoria == categoria)

    estado = request.args.get("estado")
    if estado is not None and estado != "":
        query = query.filter(Producto.estado == (estado.lower() == "true"))

    query = query.order_by(Producto.cod_sku.asc())

    result = paginate(query)
    return jsonify(
        {
            "items": [p.to_dict() for p in result["items"]],
            "page": result["page"],
            "per_page": result["per_page"],
            "total": result["total"],
            "pages": result["pages"],
        }
    )


@productos_bp.post("")
@jwt_required()
def crear_producto():
    try:
        data = producto_schema.load(request.get_json(force=True) or {})
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    if Producto.query.filter_by(cod_sku=data["cod_sku"]).first():
        return jsonify({"error": "Ya existe un producto con ese SKU"}), 409

    producto = Producto(**data)
    db.session.add(producto)
    db.session.commit()
    return jsonify(producto.to_dict()), 201


@productos_bp.get("/<int:producto_id>")
@jwt_required()
def obtener_producto(producto_id):
    producto = Producto.query.get_or_404(producto_id)
    return jsonify(producto.to_dict())


@productos_bp.put("/<int:producto_id>")
@jwt_required()
def actualizar_producto(producto_id):
    producto = Producto.query.get_or_404(producto_id)
    try:
        data = producto_update_schema.load(request.get_json(force=True) or {})
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    if "cod_sku" in data and data["cod_sku"] != producto.cod_sku:
        if Producto.query.filter_by(cod_sku=data["cod_sku"]).first():
            return jsonify({"error": "Ya existe un producto con ese SKU"}), 409

    for key, value in data.items():
        setattr(producto, key, value)

    db.session.commit()
    return jsonify(producto.to_dict())


@productos_bp.delete("/<int:producto_id>")
@jwt_required()
def eliminar_producto(producto_id):
    producto = Producto.query.get_or_404(producto_id)
    db.session.delete(producto)
    db.session.commit()
    return "", 204


@productos_bp.post("/<int:producto_id>/imagen")
@jwt_required()
def subir_imagen_producto(producto_id):
    producto = Producto.query.get_or_404(producto_id)

    file = request.files.get("file")
    if not file or not file.filename:
        return jsonify({"error": "No se envio ninguna imagen"}), 400

    ext = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        return jsonify({"error": "Formato de imagen no soportado"}), 400

    filename = secure_filename(f"{producto.cod_sku}-{uuid.uuid4().hex[:8]}.{ext}")
    folder = os.path.join(current_app.config["UPLOAD_FOLDER"], "productos")
    os.makedirs(folder, exist_ok=True)
    file.save(os.path.join(folder, filename))

    producto.imagen_url = f"/api/productos/imagenes/{filename}"
    db.session.commit()
    return jsonify(producto.to_dict())


@productos_bp.get("/imagenes/<path:filename>")
def servir_imagen_producto(filename):
    folder = os.path.join(current_app.config["UPLOAD_FOLDER"], "productos")
    return send_from_directory(folder, filename)


@productos_bp.post("/import")
@jwt_required()
def importar_productos():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No se envio ningun archivo"}), 400

    try:
        rows = read_tabular_file(file)
    except ImportError_ as err:
        return jsonify({"error": str(err)}), 400

    errors = []
    inserted = 0
    for idx, row in enumerate(rows, start=2):
        try:
            data = producto_schema.load(
                {
                    "cod_sku": row.get("cod_sku", "").strip(),
                    "nro_producto": row.get("nro_producto") or None,
                    "descripcion": row.get("descripcion") or None,
                    "clase": row.get("clase") or None,
                    "categoria": row.get("categoria") or None,
                    "origen": row.get("origen") or None,
                    "metros": row.get("metros") or None,
                    "kilogramos": row.get("kilogramos") or None,
                    "piezas": row.get("piezas") or None,
                    "color": row.get("color") or None,
                    "marca": row.get("marca") or None,
                    "precio": row.get("precio") or None,
                    "costo": row.get("costo") or None,
                    "stock_actual": row.get("stock_actual") or 0,
                    "stock_minimo": row.get("stock_minimo") or 0,
                    "estado": (row.get("estado", "true") or "true").lower() != "false",
                }
            )
        except ValidationError as err:
            errors.append({"fila": idx, "error": err.messages})
            continue

        if Producto.query.filter_by(cod_sku=data["cod_sku"]).first():
            errors.append({"fila": idx, "error": f"SKU {data['cod_sku']} ya existe"})
            continue

        db.session.add(Producto(**data))
        inserted += 1

    db.session.commit()
    return jsonify(build_import_report(len(rows), inserted, errors))


@productos_bp.get("/export")
@jwt_required()
def exportar_productos():
    productos = Producto.query.order_by(Producto.cod_sku.asc()).all()

    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=CSV_COLUMNS)
    writer.writeheader()
    for producto in productos:
        row = producto.to_dict()
        writer.writerow({col: row.get(col, "") for col in CSV_COLUMNS})

    return Response(
        buffer.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=productos.csv"},
    )
