import { Fragment, useMemo, useState } from "react";
import { useQuery } from "@tanstack/react-query";

import type { Cliente, Venta } from "../../api/types";
import { colors } from "../../theme/colors";
import { VentasPorMesChart } from "../dashboard/VentasPorMesChart";
import { fetchVentas } from "../ventas/ventasApi";
import { ClienteAutocomplete } from "./ClienteAutocomplete";
import { ProductosExpandibles } from "./ProductosExpandibles";
import { VentaDetalleModal } from "./VentaDetalleModal";

function ventasPorMes(ventas: Venta[]) {
  const hoy = new Date();
  const inicio = new Date(hoy.getFullYear(), hoy.getMonth() - 11, 1);

  const totales = new Map<string, number>();
  for (const v of ventas) {
    if (!v.fecha_factura) continue;
    const fecha = new Date(v.fecha_factura);
    if (fecha < inicio) continue;
    const clave = `${fecha.getFullYear()}-${String(fecha.getMonth() + 1).padStart(2, "0")}`;
    totales.set(clave, (totales.get(clave) ?? 0) + v.total);
  }

  const meses = [];
  for (let i = 11; i >= 0; i--) {
    const mes = new Date(hoy.getFullYear(), hoy.getMonth() - i, 1);
    const clave = `${mes.getFullYear()}-${String(mes.getMonth() + 1).padStart(2, "0")}`;
    meses.push({ mes: clave, total: Math.round((totales.get(clave) ?? 0) * 100) / 100 });
  }
  return meses;
}

export function HistorialPage() {
  const [cliente, setCliente] = useState<Cliente | null>(null);
  const [desde, setDesde] = useState("");
  const [hasta, setHasta] = useState("");
  const [expandido, setExpandido] = useState<number | null>(null);
  const [detalle, setDetalle] = useState<Venta | null>(null);

  const { data, isLoading } = useQuery({
    queryKey: ["historial-ventas", cliente?.id, desde, hasta],
    queryFn: () =>
      fetchVentas({
        cliente_id: cliente!.id,
        desde: desde || undefined,
        hasta: hasta || undefined,
        per_page: 200,
      }),
    enabled: cliente != null,
  });

  const ventas = data?.items ?? [];
  const totalComprado = useMemo(() => ventas.reduce((acc, v) => acc + v.total, 0), [ventas]);
  const chartData = useMemo(() => ventasPorMes(ventas), [ventas]);

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 20 }}>
      <h2 style={{ margin: 0, color: colors.purpleDark }}>Historial de Compras</h2>

      <div className="card" style={{ display: "flex", gap: 16, flexWrap: "wrap", alignItems: "flex-end" }}>
        <ClienteAutocomplete selected={cliente} onSelect={setCliente} />
        <div>
          <label htmlFor="desde">Desde</label>
          <input id="desde" type="date" value={desde} onChange={(e) => setDesde(e.target.value)} />
        </div>
        <div>
          <label htmlFor="hasta">Hasta</label>
          <input id="hasta" type="date" value={hasta} onChange={(e) => setHasta(e.target.value)} />
        </div>
      </div>

      {!cliente ? (
        <div className="card">
          <p style={{ margin: 0, color: colors.grayNeutral, fontSize: 14 }}>
            Buscá un cliente para ver su historial de compras.
          </p>
        </div>
      ) : isLoading ? (
        <div style={{ padding: 40, textAlign: "center", color: colors.grayNeutral }}>Cargando...</div>
      ) : (
        <>
          <div className="dashboard-kpis">
            <div className="card">
              <div style={{ fontSize: 13, color: colors.grayNeutral }}>Cliente</div>
              <div style={{ fontSize: 18, fontWeight: 700, color: colors.purpleDark }}>
                {cliente.razon_social}
              </div>
              <div style={{ fontSize: 12, color: colors.grayNeutral }}>{cliente.ruc ?? "-"}</div>
            </div>
            <div className="card">
              <div style={{ fontSize: 13, color: colors.grayNeutral }}>Total comprado</div>
              <div style={{ fontSize: 28, fontWeight: 700, color: colors.purpleDark }}>
                ₲ {totalComprado.toLocaleString("es-PY")}
              </div>
            </div>
            <div className="card">
              <div style={{ fontSize: 13, color: colors.grayNeutral }}>Cantidad de ventas</div>
              <div style={{ fontSize: 28, fontWeight: 700, color: colors.purpleDark }}>{ventas.length}</div>
            </div>
          </div>

          <div className="card">
            <h3 style={{ margin: "0 0 8px", color: colors.purpleDark }}>
              Evolución de compras (últimos 12 meses)
            </h3>
            <VentasPorMesChart data={chartData} />
          </div>

          <div className="card">
            <h3 style={{ margin: "0 0 12px", color: colors.purpleDark }}>Ventas</h3>
            {ventas.length === 0 ? (
              <p style={{ margin: 0, color: colors.grayNeutral, fontSize: 14 }}>
                Este cliente todavía no tiene ventas registradas.
              </p>
            ) : (
              <div className="table-scroll">
                <table>
                  <thead>
                    <tr>
                      <th>Nro. Factura</th>
                      <th>Fecha</th>
                      <th>Total</th>
                      <th>Estado pago</th>
                      <th>Productos</th>
                      <th></th>
                    </tr>
                  </thead>
                  <tbody>
                    {ventas.map((v) => (
                      <Fragment key={v.id}>
                        <tr>
                          <td>{v.nro_factura}</td>
                          <td>{v.fecha_factura ?? "-"}</td>
                          <td>₲ {v.total.toLocaleString("es-PY")}</td>
                          <td>
                            <span className="badge badge-active">{v.estado_pago}</span>
                          </td>
                          <td>
                            <button
                              className="btn btn-secondary"
                              onClick={() => setExpandido(expandido === v.id ? null : v.id)}
                            >
                              {expandido === v.id ? "Ocultar" : "Ver productos"}
                            </button>
                          </td>
                          <td>
                            <button className="btn btn-primary" onClick={() => setDetalle(v)}>
                              Ver detalle
                            </button>
                          </td>
                        </tr>
                        {expandido === v.id && (
                          <tr>
                            <td colSpan={6} style={{ background: colors.grayLight }}>
                              <ProductosExpandibles pedidoId={v.pedido_id} />
                            </td>
                          </tr>
                        )}
                      </Fragment>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </>
      )}

      {detalle && <VentaDetalleModal venta={detalle} onClose={() => setDetalle(null)} />}
    </div>
  );
}
