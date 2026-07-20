import csv
import io

from flask import Blueprint, Response, jsonify, request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from sqlalchemy import or_

from app.extensions import db
from app.models.coleccion import Coleccion
from app.models.producto import Producto
from app.schemas.producto_schema import producto_schema, producto_update_schema
from app.utils.cloudinary_upload import CloudinaryNotConfiguredError, upload_imagen
from app.utils.importers import ImportError_, build_import_report, read_tabular_file
from app.utils.karretel_precios import buscar_precio_karretel
from app.utils.pagination import paginate

productos_bp = Blueprint("productos", __name__)

CSV_COLUMNS = [
    "cod_producto",
    "proveedor",
    "marca",
    "coleccion",
    "nombre_tejido",
    "cod_color",
    "color_general",
    "color_descripcion",
    "categoria",
    "sub_categoria",
    "tipo_diseno",
    "composicion",
    "linea_sugerida",
    "ancho_cm",
    "gramaje_gm2",
    "precio_rollo",
    "precio_media_rollo",
    "precio_corte",
    "stock_rollos",
    "activo",
    "fecha_creacion",
    "notas",
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
                Producto.cod_producto.ilike(like),
                Producto.nombre_tejido.ilike(like),
                Producto.color_general.ilike(like),
            )
        )

    categoria = request.args.get("categoria")
    if categoria:
        query = query.filter(Producto.categoria == categoria)

    activo = request.args.get("activo")
    if activo is not None and activo != "":
        query = query.filter(Producto.activo == (activo.lower() == "true"))

    query = query.order_by(Producto.cod_producto.asc())

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

    if Producto.query.filter_by(cod_producto=data["cod_producto"]).first():
        return jsonify({"error": "Ya existe un producto con ese Cod Producto"}), 409

    if data.get("coleccion_id") is not None and not db.session.get(Coleccion, data["coleccion_id"]):
        return jsonify({"error": "La colección indicada no existe"}), 400

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

    if "cod_producto" in data and data["cod_producto"] != producto.cod_producto:
        if Producto.query.filter_by(cod_producto=data["cod_producto"]).first():
            return jsonify({"error": "Ya existe un producto con ese Cod Producto"}), 409

    if data.get("coleccion_id") is not None and not db.session.get(Coleccion, data["coleccion_id"]):
        return jsonify({"error": "La colección indicada no existe"}), 400

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


@productos_bp.post("/upload")
@jwt_required()
def upload_imagen_producto():
    file = request.files.get("file")
    if not file or not file.filename:
        return jsonify({"error": "No se envio ninguna imagen"}), 400

    ext = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        return jsonify({"error": "Formato de imagen no soportado"}), 400

    try:
        url = upload_imagen(file)
    except CloudinaryNotConfiguredError as err:
        return jsonify({"error": str(err)}), 400

    return jsonify({"url": url})


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

    # Alias de columnas que en los maestros reales vienen con otro nombre
    # (ej. Maestro_Limpio.xlsx trae "Descripcion_Completa", "Stock" y
    # "Color (Inferido visualmente)" en vez de nuestros nombres de campo).
    # read_tabular_file ya normaliza mayusculas/espacios/acentos a
    # snake_case; esto cubre los casos donde el nombre de la columna origen
    # es directamente distinto al campo.
    COLUMN_ALIASES = {
        "descripcion_completa": "descripcion",
        "stock": "stock_rollos",
        "color_inferido_visualmente": "color_descripcion",
    }

    errors = []
    inserted = 0
    updated = 0
    for idx, row in enumerate(rows, start=2):
        for origen, destino in COLUMN_ALIASES.items():
            if row.get(destino) in (None, "") and row.get(origen) not in (None, ""):
                row[destino] = row[origen]

        nombre_tejido = (row.get("nombre_tejido") or "").strip()
        precio_karretel = buscar_precio_karretel(nombre_tejido) or {}

        def _precio(campo):
            valor = row.get(campo)
            if valor not in (None, ""):
                return valor
            return precio_karretel.get(campo)

        try:
            data = producto_schema.load(
                {
                    "cod_producto": (row.get("cod_producto") or "").strip(),
                    "proveedor": row.get("proveedor") or None,
                    "marca": row.get("marca") or None,
                    "coleccion": row.get("coleccion") or None,
                    "cod_color": row.get("cod_color") or None,
                    "nombre_tejido": nombre_tejido,
                    "color_general": row.get("color_general") or None,
                    "color_descripcion": row.get("color_descripcion") or None,
                    "categoria": (row.get("categoria") or "").strip(),
                    "sub_categoria": row.get("sub_categoria") or None,
                    "tipo_diseno": row.get("tipo_diseno") or None,
                    "composicion": row.get("composicion") or None,
                    "linea_sugerida": row.get("linea_sugerida") or None,
                    "ancho_cm": row.get("ancho_cm") or None,
                    "gramaje_gm2": row.get("gramaje_gm2") or None,
                    "precio_rollo": _precio("precio_rollo"),
                    "precio_media_rollo": _precio("precio_media_rollo"),
                    "precio_corte": _precio("precio_corte"),
                    "stock_rollos": row.get("stock_rollos") or 0,
                    "descripcion": row.get("descripcion") or None,
                    "fecha_creacion": row.get("fecha_creacion") or None,
                    "notas": row.get("notas") or None,
                    "activo": (row.get("activo", "true") or "true").lower() != "false",
                }
            )
        except ValidationError as err:
            errors.append({"fila": idx, "error": err.messages})
            continue

        existente = Producto.query.filter_by(cod_producto=data["cod_producto"]).first()
        if existente:
            for key, value in data.items():
                setattr(existente, key, value)
            updated += 1
        else:
            db.session.add(Producto(**data))
            inserted += 1

    db.session.commit()
    report = build_import_report(len(rows), inserted, errors)
    report["actualizados"] = updated
    return jsonify(report)


@productos_bp.get("/export")
@jwt_required()
def exportar_productos():
    productos = Producto.query.order_by(Producto.cod_producto.asc()).all()

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
