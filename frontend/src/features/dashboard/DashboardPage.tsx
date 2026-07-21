import { useQuery } from "@tanstack/react-query";

import { colors } from "../../theme/colors";
import { fetchResumen } from "./dashboardApi";
import { DonutChart } from "./DonutChart";
import { GestionesBarList } from "./GestionesBarList";
import { VentasPorMesChart } from "./VentasPorMesChart";

function KpiCard({ label, value }: { label: string; value: string | number }) {
  return (
    <div className="card">
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

      <div className="dashboard-kpis">
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

      <div className="dashboard-grid">
        <div className="card" style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 12 }}>
          <h3 style={{ margin: 0, alignSelf: "flex-start", color: colors.purpleDark }}>
            Cobertura de Clientes
          </h3>
          <DonutChart percentage={data.cobertura_porcentaje} />
          <div style={{ fontSize: 13, color: "#4a4a5a", textAlign: "center" }}>
            {data.clientes_visitados_mes} de {data.total_clientes_cartera} clientes visitados este mes
          </div>
        </div>

        <div className="card">
          <h3 style={{ margin: "0 0 12px", color: colors.purpleDark }}>Gestiones Realizadas</h3>
          <GestionesBarList data={data.gestiones_por_tipo} />
        </div>

        <div className="card" style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 12 }}>
          <h3 style={{ margin: 0, alignSelf: "flex-start", color: colors.purpleDark }}>
            Efectividad de Gestiones
          </h3>
          <DonutChart percentage={data.efectividad_gestiones_porcentaje} color={colors.pinkNeon} />
          <div style={{ fontSize: 13, color: "#4a4a5a", textAlign: "center" }}>
            de las gestiones de este mes resultaron en Venta Exitosa
          </div>
        </div>

        <div className="card">
          <h3 style={{ margin: "0 0 8px", color: colors.purpleDark }}>Stock más bajo</h3>
          {data.stock_bajo.length === 0 ? (
            <p style={{ fontSize: 13, color: colors.grayNeutral }}>Sin alertas de stock.</p>
          ) : (
            <ul style={{ margin: 0, paddingLeft: 18, fontSize: 13 }}>
              {data.stock_bajo.map((p) => (
                <li key={p.id}>
                  {p.cod_producto} — {p.descripcion ?? ""} ({p.stock_rollos ?? 0} rollos)
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
                  {v.fecha} {v.hora ?? ""} — {v.cliente?.razon_social ?? "-"}
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
                  {producto.cod_producto} — {cantidad_total} unidades
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  );
}
