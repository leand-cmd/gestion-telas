import io

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

BRAND_PURPLE = colors.HexColor("#6C5DD1")
BRAND_PURPLE_DARK = colors.HexColor("#5A4FA8")
BRAND_GRAY = colors.HexColor("#F5F5F7")


def generate_pedido_pdf(pedido) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
    )
    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    title_style.textColor = BRAND_PURPLE_DARK
    normal = styles["Normal"]

    elements = [
        Paragraph("Gestión de Ventas — Telas", title_style),
        Paragraph(f"Pedido {pedido.nro_pedido}", styles["Heading2"]),
        Spacer(1, 8),
    ]

    cliente = pedido.cliente
    info_data = [
        ["Cliente:", cliente.razon_social if cliente else "-"],
        ["RUC:", cliente.ruc if cliente else "-"],
        ["Localidad:", cliente.localidad or "-" if cliente else "-"],
        ["Fecha pedido:", pedido.fecha_pedido.isoformat() if pedido.fecha_pedido else "-"],
        [
            "Entrega estimada:",
            pedido.fecha_entrega_estimada.isoformat() if pedido.fecha_entrega_estimada else "-",
        ],
        ["Tipo de compra:", pedido.tipo_compra or "-"],
        ["Estado:", pedido.estado],
    ]
    info_table = Table(info_data, colWidths=[45 * mm, 110 * mm])
    info_table.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    elements.append(info_table)
    elements.append(Spacer(1, 16))

    detalle_header = ["Cod Producto", "Descripción", "Cantidad", "Valor Unit.", "Subtotal"]
    detalle_rows = [detalle_header]
    for d in pedido.detalles:
        producto = d.producto
        detalle_rows.append(
            [
                producto.cod_producto if producto else "-",
                producto.descripcion if producto else "-",
                str(d.cantidad),
                f"{float(d.valor_unitario or 0):,.2f}",
                f"{float(d.subtotal or 0):,.2f}",
            ]
        )

    detalle_table = Table(
        detalle_rows, colWidths=[28 * mm, 62 * mm, 22 * mm, 28 * mm, 28 * mm], repeatRows=1
    )
    detalle_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), BRAND_PURPLE),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("ALIGN", (2, 0), (-1, -1), "RIGHT"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, BRAND_GRAY]),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E3E1F0")),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    elements.append(detalle_table)
    elements.append(Spacer(1, 12))

    total_data = [["Total", f"₲ {float(pedido.total or 0):,.2f}"]]
    total_table = Table(total_data, colWidths=[140 * mm, 28 * mm])
    total_table.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 11),
                ("TEXTCOLOR", (0, 0), (-1, -1), BRAND_PURPLE_DARK),
                ("ALIGN", (1, 0), (1, -1), "RIGHT"),
            ]
        )
    )
    elements.append(total_table)

    if pedido.observaciones:
        elements.append(Spacer(1, 16))
        elements.append(Paragraph("Observaciones", styles["Heading3"]))
        elements.append(Paragraph(pedido.observaciones, normal))

    doc.build(elements)
    return buffer.getvalue()


def generate_venta_pdf(venta) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
    )
    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    title_style.textColor = BRAND_PURPLE_DARK
    normal = styles["Normal"]

    elements = [
        Paragraph("Gestión de Ventas — Telas", title_style),
        Paragraph(f"Factura {venta.nro_factura}", styles["Heading2"]),
        Spacer(1, 8),
    ]

    cliente = venta.cliente
    info_data = [
        ["Cliente:", cliente.razon_social if cliente else "-"],
        ["RUC:", cliente.ruc if cliente else "-"],
        ["Fecha factura:", venta.fecha_factura.isoformat() if venta.fecha_factura else "-"],
        ["Fecha entrega:", venta.fecha_entrega.isoformat() if venta.fecha_entrega else "-"],
        ["Tipo de compra:", venta.tipo_compra or "-"],
        ["Estado de pago:", venta.estado_pago],
    ]
    info_table = Table(info_data, colWidths=[45 * mm, 110 * mm])
    info_table.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    elements.append(info_table)
    elements.append(Spacer(1, 16))

    total_data = [["Total", f"₲ {float(venta.total or 0):,.2f}"]]
    total_table = Table(total_data, colWidths=[140 * mm, 28 * mm])
    total_table.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 11),
                ("TEXTCOLOR", (0, 0), (-1, -1), BRAND_PURPLE_DARK),
                ("ALIGN", (1, 0), (1, -1), "RIGHT"),
            ]
        )
    )
    elements.append(total_table)

    if venta.observaciones:
        elements.append(Spacer(1, 16))
        elements.append(Paragraph("Observaciones", styles["Heading3"]))
        elements.append(Paragraph(venta.observaciones, normal))

    doc.build(elements)
    return buffer.getvalue()
