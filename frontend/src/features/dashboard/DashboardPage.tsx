import { useQuery } from "@tanstack/react-query";

import { colors } from "../../theme/colors";
import { fetchResumen } from "./dashboardApi";
import { VentasPorMesChart } from "./VentasPorMesChart";

function KpiCard({ label, value }: { label: string; value: string | number }) {
  return (
    <div className="card" style={{ flex: 1, minWidth: 180 }}>
      <div style={{ fontSize: 13, color: colors.grayNeutral }}>{label}</div>
      <div style={{ fontSize: 28, fontWeight: 700, color: colors.purpleDark }}>{value}</div>
    </div>
  );
}

export function DashboardPage() {
  const { data, isLoading } = useQuery({ queryKey: ["dashboard"], queryFn: fetchResumen });

  if (isLoading || !data) {
    return <div style={{ padding: 40, textAlign: "center", color: colors.grayNeutral }}>Cargando...</div>;
  }

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 20 }}>
      <h2 style={{ margin: 0, color: colors.purpleDark }}>Dashboard</h2>

      <div style={{ display: "flex", gap: 16, flexWrap: "wrap" }}>
        <KpiCard
          label="Ventas del mes"
          value={`₲ ${data.ventas_mes_actual.toLocaleString("es-PY")}`}
        />
        <KpiCard label="Pedidos pendientes" value={data.pedidos_pendientes} />
        <KpiCard label="Productos bajo stock mínimo" value={data.stock_bajo.length} />
        <KpiCard label="Visitas próximas (7 días)" value={data.proximas_visitas.length} />
      </div>

      <div className="card">
        <h3 style={{ margin: "0 0 8px", color: colors.purpleDark }}>Ventas por mes</h3>
        <VentasPorMesChart data={data.ventas_por_mes} />
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
        <div className="card">
          <h3 style={{ margin: "0 0 8px", color: colors.purpleDark }}>Stock bajo mínimo</h3>
          {data.stock_bajo.length === 0 ? (
            <p style={{ fontSize: 13, color: colors.grayNeutral }}>Sin alertas de stock.</p>
          ) : (
            <ul style={{ margin: 0, paddingLeft: 18, fontSize: 13 }}>
              {data.stock_bajo.map((p) => (
                <li key={p.id}>
                  {p.cod_sku} — {p.descripcion ?? ""} ({p.stock_actual}/{p.stock_minimo})
                </li>
              ))}
            </ul>
          )}
        </div>

        <div className="card">
          <h3 style={{ margin: "0 0 8px", color: colors.purpleDark }}>Próximas visitas</h3>
          {data.proximas_visitas.length === 0 ? (
            <p style={{ fontSize: 13, color: colors.grayNeutral }}>No hay visitas programadas.</p>
          ) : (
            <ul style={{ margin: 0, paddingLeft: 18, fontSize: 13 }}>
              {data.proximas_visitas.map((v) => (
                <li key={v.id}>
                  {v.fecha} {v.hora} — {v.cliente?.razon_social ?? "-"}
                </li>
              ))}
            </ul>
          )}
        </div>

        <div className="card">
          <h3 style={{ margin: "0 0 8px", color: colors.purpleDark }}>Top clientes</h3>
          {data.top_clientes.length === 0 ? (
            <p style={{ fontSize: 13, color: colors.grayNeutral }}>Sin ventas registradas.</p>
          ) : (
            <ul style={{ margin: 0, paddingLeft: 18, fontSize: 13 }}>
              {data.top_clientes.map(({ cliente, total_ventas }) => (
                <li key={cliente.id}>
                  {cliente.razon_social} — ₲ {total_ventas.toLocaleString("es-PY")}
                </li>
              ))}
            </ul>
          )}
        </div>

        <div className="card">
          <h3 style={{ margin: "0 0 8px", color: colors.purpleDark }}>Top productos</h3>
          {data.top_productos.length === 0 ? (
            <p style={{ fontSize: 13, color: colors.grayNeutral }}>Sin pedidos registrados.</p>
          ) : (
            <ul style={{ margin: 0, paddingLeft: 18, fontSize: 13 }}>
              {data.top_productos.map(({ producto, cantidad_total }) => (
                <li key={producto.id}>
                  {producto.cod_sku} — {cantidad_total} unidades
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  );
}
