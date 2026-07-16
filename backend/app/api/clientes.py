import csv
import io

from flask import Blueprint, Response, jsonify, request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from sqlalchemy import or_

from app.extensions import db
from app.models.cliente import Cliente
from app.schemas.cliente_schema import cliente_schema, cliente_update_schema
from app.utils.importers import ImportError_, build_import_report, read_tabular_file
from app.utils.numbering import generate_next_numeric_code
from app.utils.pagination import paginate

clientes_bp = Blueprint("clientes", __name__)

CSV_COLUMNS = [
    "codigo_cliente",
    "ruc",
    "razon_social",
    "localidad",
    "barrio",
    "direccion",
    "telefono",
    "email",
    "canal",
    "sub_canal",
    "tipo_compra",
    "latitude",
    "longitude",
    "estado",
]


@clientes_bp.get("")
@jwt_required()
def listar_clientes():
    query = Cliente.query

    q = request.args.get("q", "").strip()
    if q:
        like = f"%{q}%"
        query = query.filter(
            or_(
                Cliente.ruc.ilike(like),
                Cliente.razon_social.ilike(like),
                Cliente.localidad.ilike(like),
            )
        )

    canal = request.args.get("canal")
    if canal:
        query = query.filter(Cliente.canal == canal)

    estado = request.args.get("estado")
    if estado is not None and estado != "":
        query = query.filter(Cliente.estado == (estado.lower() == "true"))

    query = query.order_by(Cliente.razon_social.asc())

    result = paginate(query)
    return jsonify(
        {
            "items": [c.to_dict() for c in result["items"]],
            "page": result["page"],
            "per_page": result["per_page"],
            "total": result["total"],
            "pages": result["pages"],
        }
    )


@clientes_bp.get("/next-id")
@jwt_required()
def sugerir_codigo_cliente():
    return jsonify({"next_id": generate_next_numeric_code(Cliente, "codigo_cliente")})


@clientes_bp.post("")
@jwt_required()
def crear_cliente():
    try:
        data = cliente_schema.load(request.get_json(force=True) or {})
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    data["ruc"] = data.get("ruc") or None
    if data["ruc"] and Cliente.query.filter_by(ruc=data["ruc"]).first():
        return jsonify({"error": "Ya existe un cliente con ese RUC"}), 409

    codigo_cliente = data.get("codigo_cliente")
    if codigo_cliente:
        if Cliente.query.filter_by(codigo_cliente=codigo_cliente).first():
            return jsonify({"error": f"El ID de cliente '{codigo_cliente}' ya esta en uso"}), 409
    else:
        codigo_cliente = generate_next_numeric_code(Cliente, "codigo_cliente")

    data["codigo_cliente"] = codigo_cliente
    cliente = Cliente(**data)
    db.session.add(cliente)
    db.session.commit()
    return jsonify(cliente.to_dict()), 201


@clientes_bp.get("/<int:cliente_id>")
@jwt_required()
def obtener_cliente(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    return jsonify(cliente.to_dict())


@clientes_bp.put("/<int:cliente_id>")
@jwt_required()
def actualizar_cliente(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    try:
        data = cliente_update_schema.load(request.get_json(force=True) or {})
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    if "ruc" in data:
        data["ruc"] = data.get("ruc") or None
        if data["ruc"] and data["ruc"] != cliente.ruc:
            if Cliente.query.filter_by(ruc=data["ruc"]).first():
                return jsonify({"error": "Ya existe un cliente con ese RUC"}), 409

    if (
        "codigo_cliente" in data
        and data["codigo_cliente"]
        and data["codigo_cliente"] != cliente.codigo_cliente
    ):
        if Cliente.query.filter_by(codigo_cliente=data["codigo_cliente"]).first():
            return (
                jsonify({"error": f"El ID de cliente '{data['codigo_cliente']}' ya esta en uso"}),
                409,
            )

    for key, value in data.items():
        setattr(cliente, key, value)

    db.session.commit()
    return jsonify(cliente.to_dict())


@clientes_bp.delete("/<int:cliente_id>")
@jwt_required()
def eliminar_cliente(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    db.session.delete(cliente)
    db.session.commit()
    return "", 204


@clientes_bp.post("/import")
@jwt_required()
def importar_clientes():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No se envio ningun archivo"}), 400

    try:
        rows = read_tabular_file(file)
    except ImportError_ as err:
        return jsonify({"error": str(err)}), 400

    errors = []
    inserted = 0
    for idx, row in enumerate(rows, start=2):  # fila 1 es encabezado
        try:
            data = cliente_schema.load(
                {
                    "codigo_cliente": row.get("codigo_cliente") or None,
                    "ruc": row.get("ruc", "").strip() or None,
                    "razon_social": row.get("razon_social", "").strip(),
                    "localidad": row.get("localidad") or None,
                    "barrio": row.get("barrio") or None,
                    "direccion": row.get("direccion") or None,
                    "telefono": row.get("telefono") or None,
                    "email": row.get("email") or None,
                    "canal": row.get("canal") or None,
                    "sub_canal": row.get("sub_canal") or None,
                    "tipo_compra": row.get("tipo_compra") or None,
                    "latitude": row.get("latitude") or None,
                    "longitude": row.get("longitude") or None,
                    "estado": (row.get("estado", "true") or "true").lower() != "false",
                }
            )
        except ValidationError as err:
            errors.append({"fila": idx, "error": err.messages})
            continue

        if data["ruc"] and Cliente.query.filter_by(ruc=data["ruc"]).first():
            errors.append({"fila": idx, "error": f"RUC {data['ruc']} ya existe"})
            continue

        if data.get("codigo_cliente"):
            if Cliente.query.filter_by(codigo_cliente=data["codigo_cliente"]).first():
                errors.append(
                    {"fila": idx, "error": f"ID de cliente '{data['codigo_cliente']}' ya existe"}
                )
                continue
        else:
            data["codigo_cliente"] = generate_next_numeric_code(Cliente, "codigo_cliente")

        db.session.add(Cliente(**data))
        inserted += 1

    db.session.commit()
    return jsonify(build_import_report(len(rows), inserted, errors))


@clientes_bp.get("/export")
@jwt_required()
def exportar_clientes():
    clientes = Cliente.query.order_by(Cliente.razon_social.asc()).all()

    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=CSV_COLUMNS)
    writer.writeheader()
    for cliente in clientes:
        row = cliente.to_dict()
        writer.writerow({col: row.get(col, "") for col in CSV_COLUMNS})

    return Response(
        buffer.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=clientes.csv"},
    )
