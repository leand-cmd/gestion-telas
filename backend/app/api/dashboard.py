from collections import defaultdict
from datetime import date, timedelta

from dateutil.relativedelta import relativedelta
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import func

from app.extensions import db
from app.models.cliente import Cliente
from app.models.pedido import PedidoDetalle
from app.models.producto import Producto
from app.models.venta import Venta
from app.models.pedido import Pedido
from app.models.visita import Visita

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.get("/resumen")
@jwt_required()
def resumen():
    hoy = date.today()
    inicio_mes = hoy.replace(day=1)
    inicio_rango = (inicio_mes - relativedelta(months=5))

    ventas_rango = (
        Venta.query.filter(Venta.fecha_factura.isnot(None))
        .filter(Venta.fecha_factura >= inicio_rango)
        .all()
    )

    ventas_por_mes_dict: dict[str, float] = defaultdict(float)
    ventas_mes_actual = 0.0
    for venta in ventas_rango:
        clave = venta.fecha_factura.strftime("%Y-%m")
        ventas_por_mes_dict[clave] += float(venta.total or 0)
        if venta.fecha_factura >= inicio_mes:
            ventas_mes_actual += float(venta.total or 0)

    ventas_por_mes = []
    for i in range(5, -1, -1):
        mes = inicio_mes - relativedelta(months=i)
        clave = mes.strftime("%Y-%m")
        ventas_por_mes.append({"mes": clave, "total": round(ventas_por_mes_dict.get(clave, 0), 2)})

    pedidos_pendientes = Pedido.query.filter(
        Pedido.estado.in_(["borrador", "confirmado"])
    ).count()

    stock_bajo = (
        Producto.query.filter(Producto.stock_actual < Producto.stock_minimo)
        .order_by(Producto.stock_actual.asc())
        .limit(10)
        .all()
    )

    proximas_visitas = (
        Visita.query.filter(
            Visita.fecha >= hoy,
            Visita.fecha <= hoy + timedelta(days=7),
            Visita.estado == "programada",
        )
        .order_by(Visita.fecha.asc(), Visita.hora.asc())
        .limit(10)
        .all()
    )

    top_clientes_query = (
        db.session.query(Cliente, func.sum(Venta.total).label("total_ventas"))
        .join(Venta, Venta.cliente_id == Cliente.id)
        .group_by(Cliente.id)
        .order_by(func.sum(Venta.total).desc())
        .limit(5)
        .all()
    )
    top_clientes = [
        {"cliente": cliente.to_dict(), "total_ventas": float(total or 0)}
        for cliente, total in top_clientes_query
    ]

    top_productos_query = (
        db.session.query(Producto, func.sum(PedidoDetalle.cantidad).label("cantidad_total"))
        .join(PedidoDetalle, PedidoDetalle.producto_id == Producto.id)
        .group_by(Producto.id)
        .order_by(func.sum(PedidoDetalle.cantidad).desc())
        .limit(5)
        .all()
    )
    top_productos = [
        {"producto": producto.to_dict(), "cantidad_total": int(cantidad or 0)}
        for producto, cantidad in top_productos_query
    ]

    return jsonify(
        {
            "ventas_mes_actual": round(ventas_mes_actual, 2),
            "ventas_por_mes": ventas_por_mes,
            "pedidos_pendientes": pedidos_pendientes,
            "stock_bajo": [p.to_dict() for p in stock_bajo],
            "proximas_visitas": [v.to_dict() for v in proximas_visitas],
            "top_clientes": top_clientes,
            "top_productos": top_productos,
        }
    )
