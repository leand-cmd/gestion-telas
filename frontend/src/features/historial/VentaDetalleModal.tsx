import { useQuery } from "@tanstack/react-query";
import toast from "react-hot-toast";

import type { Venta } from "../../api/types";
import { colors } from "../../theme/colors";
import { fetchPedido } from "../pedidos/pedidosApi";
import { descargarPdfVenta } from "../ventas/ventasApi";

interface VentaDetalleModalProps {
  venta: Venta;
  onClose: () => void;
}

export function VentaDetalleModal({ venta, onClose }: VentaDetalleModalProps) {
  const { data: pedido, isLoading } = useQuery({
    queryKey: ["pedido", venta.pedido_id],
    queryFn: () => fetchPedido(venta.pedido_id as number),
    enabled: venta.pedido_id != null,
  });

  return (
    <div
      style={{
        position: "fixed",
        inset: 0,
        background: "rgba(43,43,56,0.4)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        zIndex: 1000,
        padding: 24,
      }}
    >
      <div
        className="card"
        style={{ width: "100%", maxWidth: 560, display: "flex", flexDirection: "column", gap: 12 }}
      >
        <h3 style={{ margin: 0, color: colors.purpleDark }}>Venta {venta.nro_factura}</h3>

        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10, fontSize: 13 }}>
          <div>
            <div style={{ color: colors.grayNeutral, fontSize: 11, fontWeight: 700 }}>FECHA FACTURA</div>
            <div>{venta.fecha_factura ?? "-"}</div>
          </div>
          <div>
            <div style={{ color: colors.grayNeutral, fontSize: 11, fontWeight: 700 }}>FECHA ENTREGA</div>
            <div>{venta.fecha_entrega ?? "-"}</div>
          </div>
          <div>
            <div style={{ color: colors.grayNeutral, fontSize: 11, fontWeight: 700 }}>TIPO DE COMPRA</div>
            <div>{venta.tipo_compra ?? "-"}</div>
          </div>
          <div>
            <div style={{ color: colors.grayNeutral, fontSize: 11, fontWeight: 700 }}>ESTADO DE PAGO</div>
            <div>{venta.estado_pago}</div>
          </div>
          {venta.observaciones && (
            <div style={{ gridColumn: "1 / -1" }}>
              <div style={{ color: colors.grayNeutral, fontSize: 11, fontWeight: 700 }}>OBSERVACIONES</div>
              <div>{venta.observaciones}</div>
            </div>
          )}
        </div>

        <div>
          <div style={{ color: colors.grayNeutral, fontSize: 11, fontWeight: 700, marginBottom: 6 }}>
            PRODUCTOS
          </div>
          {venta.pedido_id == null ? (
            <p style={{ fontSize: 13, color: colors.grayNeutral, margin: 0 }}>
              Venta cargada directamente, sin detalle de productos.
            </p>
          ) : isLoading ? (
            <p style={{ fontSize: 13, color: colors.grayNeutral, margin: 0 }}>Cargando productos...</p>
          ) : (
            <div className="table-scroll">
              <table>
                <thead>
                  <tr>
                    <th>SKU</th>
                    <th>Descripción</th>
                    <th>Cantidad</th>
                    <th>Subtotal</th>
                  </tr>
                </thead>
                <tbody>
                  {(pedido?.detalles ?? []).map((d) => (
                    <tr key={d.id}>
                      <td>{d.producto?.cod_sku ?? "-"}</td>
                      <td>{d.producto?.descripcion ?? "-"}</td>
                      <td>{d.cantidad}</td>
                      <td>₲ {(d.subtotal ?? 0).toLocaleString("es-PY")}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>

        <div style={{ textAlign: "right", fontWeight: 700, color: colors.purpleDark }}>
          Total: ₲ {venta.total.toLocaleString("es-PY")}
        </div>

        <div style={{ display: "flex", justifyContent: "flex-end", gap: 8, marginTop: 8 }}>
          <button type="button" className="btn btn-secondary" onClick={onClose}>
            Cerrar
          </button>
          <button
            type="button"
            className="btn btn-primary"
            onClick={() =>
              descargarPdfVenta(venta.id, venta.nro_factura).catch(() =>
                toast.error("Error al generar PDF")
              )
            }
          >
            Descargar PDF
          </button>
        </div>
      </div>
    </div>
  );
}
